"""Tests for DIAN e-invoicing service."""

import pytest
from datetime import datetime
from backend.services.dian_einvoicing import DIANEInvoicingService, get_dian_service
from backend.models.dian_schemas import (
    FacturaElectronica,
    EmisorInfo,
    ClienteInfo,
    InvoiceLineItem,
    TaxDetail,
    EInvoiceRequest,
    NotaCredito,
)


@pytest.fixture
def dian_service():
    """Create DIAN service instance in stub mode."""
    return DIANEInvoicingService(provider="stub")


@pytest.fixture
def sample_factura():
    """Create a sample invoice for testing."""
    return FacturaElectronica(
        numero_factura="FE-001",
        fecha_emision=datetime.now(),
        tipo_factura="01",
        moneda="COP",
        emisor=EmisorInfo(
            nit="900123456-7",
            razon_social="Mi Empresa SAS",
            direccion="Calle 100 #20-30",
            ciudad="Bogotá",
            departamento="Cundinamarca",
        ),
        cliente=ClienteInfo(
            nit="900654321-8",
            razon_social="Cliente Ejemplo SAS",
            direccion="Carrera 50 #30-40",
            ciudad="Medellín",
            departamento="Antioquia",
            email="cliente@example.com",
        ),
        items=[
            InvoiceLineItem(
                line_number=1,
                description="Servicio de consultoría",
                quantity=1,
                unit_price=1000000,
                subtotal=1000000,
                taxes=[TaxDetail(tax_type="IVA", rate=19, amount=190000)],
                total=1190000,
            )
        ],
        subtotal=1000000,
        total_impuestos=190000,
        total=1190000,
    )


class TestDIANService:
    """Test DIAN e-invoicing service."""

    def test_generate_cufe(self, dian_service, sample_factura):
        """Test CUFE generation."""
        cufe = dian_service._generate_cufe(sample_factura)
        assert cufe is not None
        assert len(cufe) == 96
        assert isinstance(cufe, str)

    def test_emitir_factura_success(self, dian_service, sample_factura):
        """Test successful invoice emission."""
        request = EInvoiceRequest(factura=sample_factura, generar_pdf=True, enviar_email=False)
        response = dian_service.emitir_factura(request)

        assert response.success is True
        assert response.numero_factura == "FE-001"
        assert response.cufe is not None
        assert len(response.cufe) == 96
        assert response.xml_path is not None
        assert response.pdf_path is not None
        assert "stub" in response.estado.lower()

    def test_emitir_factura_generates_xml(self, dian_service, sample_factura):
        """Test that XML is generated."""
        xml = dian_service._generate_xml(sample_factura, "test-cufe-123")
        assert xml is not None
        assert "Invoice" in xml
        assert sample_factura.numero_factura in xml
        assert sample_factura.emisor.nit in xml

    def test_validar_factura_valid(self, dian_service, sample_factura):
        """Test invoice validation with valid data."""
        result = dian_service.validar_factura(sample_factura)
        assert result["valido"] is True
        assert result["errores"] is None

    def test_validar_factura_invalid_totals(self, dian_service, sample_factura):
        """Test invoice validation with invalid totals."""
        # Modify total to be incorrect
        sample_factura.total = 999999
        result = dian_service.validar_factura(sample_factura)
        assert result["valido"] is False
        assert result["errores"] is not None
        assert len(result["errores"]) > 0

    def test_emitir_nota_credito(self, dian_service):
        """Test credit note emission."""
        nota = NotaCredito(
            numero_nota="NC-001",
            factura_afectada="FE-001",
            cufe_factura="test-cufe-original",
            emisor=EmisorInfo(
                nit="900123456-7",
                razon_social="Mi Empresa SAS",
                direccion="Calle 100 #20-30",
                ciudad="Bogotá",
                departamento="Cundinamarca",
            ),
            cliente=ClienteInfo(
                nit="900654321-8",
                razon_social="Cliente Ejemplo SAS",
                direccion="Carrera 50 #30-40",
                ciudad="Medellín",
                departamento="Antioquia",
                email="cliente@example.com",
            ),
            motivo="Devolución de mercancía",
            concepto_correccion="Devolucion",
            subtotal=100000,
            total_impuestos=19000,
            total=119000,
        )

        response = dian_service.emitir_nota_credito(nota)
        assert response.success is True
        assert response.numero_factura == "NC-001"
        assert response.cufe is not None  # CUDE in this case

    def test_consultar_estado(self, dian_service):
        """Test invoice status query."""
        status = dian_service.consultar_estado("FE-001", "test-cufe-123")
        assert status.numero_factura == "FE-001"
        assert status.cufe == "test-cufe-123"
        assert status.estado_dian is not None
        assert "stub" in status.estado_dian.lower()

    def test_get_dian_service(self):
        """Test service factory function."""
        service = get_dian_service()
        assert service is not None
        assert isinstance(service, DIANEInvoicingService)


class TestDIANSchemas:
    """Test DIAN schema validation."""

    def test_nit_validation_valid(self):
        """Test valid NIT."""
        emisor = EmisorInfo(
            nit="900123456-7",
            razon_social="Test Company",
            direccion="Test Address",
            ciudad="Bogotá",
            departamento="Cundinamarca",
        )
        assert emisor.nit == "900123456-7"

    def test_nit_validation_invalid(self):
        """Test invalid NIT (too short)."""
        with pytest.raises(ValueError, match="NIT must be at least 9 digits"):
            EmisorInfo(
                nit="123",
                razon_social="Test Company",
                direccion="Test Address",
                ciudad="Bogotá",
                departamento="Cundinamarca",
            )

    def test_currency_validation(self):
        """Test currency validation."""
        with pytest.raises(ValueError, match="Currency must be"):
            FacturaElectronica(
                numero_factura="FE-001",
                moneda="XXX",  # Invalid currency
                emisor=EmisorInfo(
                    nit="900123456-7",
                    razon_social="Test",
                    direccion="Test",
                    ciudad="Bogotá",
                    departamento="Cundinamarca",
                ),
                cliente=ClienteInfo(
                    nit="900654321-8",
                    razon_social="Test",
                    direccion="Test",
                    ciudad="Medellín",
                    departamento="Antioquia",
                    email="test@example.com",
                ),
                items=[],
                subtotal=0,
                total_impuestos=0,
                total=0,
            )
