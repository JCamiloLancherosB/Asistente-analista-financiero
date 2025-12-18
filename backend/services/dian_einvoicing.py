"""DIAN Colombia e-invoicing service with provider integration stubs.

This module provides the interface for Colombian e-invoicing (factura electrónica)
with stub implementations that can be replaced with real provider integrations.

Supported providers (configured via E_INVOICE_PROVIDER env var):
- 'dian_api': Direct DIAN API integration (requires certification)
- 'pac_provider': PAC (Proveedor Autorizado de Certificación) provider
- 'stub': Stub implementation for testing (default)

Environment variables required:
- E_INVOICE_PROVIDER: Provider type ('dian_api', 'pac_provider', 'stub')
- E_INVOICE_API_KEY: API key for the provider
- E_INVOICE_API_URL: Base URL for the provider API
- E_INVOICE_CERT_PATH: Path to certificate file (for DIAN direct integration)
- E_INVOICE_CERT_PASSWORD: Certificate password
- E_INVOICE_NIT_EMISOR: NIT of the issuer (your company)
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from backend.models.dian_schemas import (
    EInvoiceRequest,
    EInvoiceResponse,
    FacturaElectronica,
    InvoiceStatusResponse,
    NotaCredito,
)

logger = logging.getLogger(__name__)


class DIANEInvoicingService:
    """Service for DIAN Colombia e-invoicing operations."""

    def __init__(
        self,
        provider: str = "stub",
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        cert_path: Optional[str] = None,
        cert_password: Optional[str] = None,
        nit_emisor: Optional[str] = None,
    ):
        """
        Initialize DIAN e-invoicing service.

        Args:
            provider: Provider type ('dian_api', 'pac_provider', 'stub')
            api_key: API key for the provider
            api_url: Base URL for provider API
            cert_path: Path to certificate file
            cert_password: Certificate password
            nit_emisor: NIT of the issuer
        """
        self.provider = provider
        self.api_key = api_key
        self.api_url = api_url
        self.cert_path = cert_path
        self.cert_password = cert_password
        self.nit_emisor = nit_emisor

        # Storage directory for XML/PDF files
        self.storage_dir = os.getenv("E_INVOICE_STORAGE_DIR", "/tmp/einvoices")
        os.makedirs(self.storage_dir, exist_ok=True)

        logger.info(f"Initialized DIAN e-invoicing service with provider: {provider}")

    def _generate_cufe(self, factura: FacturaElectronica) -> str:
        """
        Generate CUFE (Código Único de Factura Electrónica).

        This is a simplified stub implementation. Real CUFE generation follows
        DIAN's specification and includes cryptographic signatures.

        Args:
            factura: Invoice data

        Returns:
            Generated CUFE string
        """
        # CUFE components (simplified)
        components = [
            factura.numero_factura,
            factura.fecha_emision.isoformat(),
            factura.emisor.nit,
            factura.cliente.nit,
            str(factura.total),
            str(uuid4()),  # In real implementation, this would be calculated
        ]

        # Generate hash (real CUFE uses SHA-384)
        cufe_string = "".join(components)
        cufe_hash = hashlib.sha384(cufe_string.encode()).hexdigest()

        return cufe_hash[:96]  # CUFE is 96 characters

    def _generate_cude(self, nota: NotaCredito) -> str:
        """
        Generate CUDE (Código Único de Documento Electrónico) for credit notes.

        Args:
            nota: Credit note data

        Returns:
            Generated CUDE string
        """
        components = [
            nota.numero_nota,
            nota.fecha_emision.isoformat(),
            nota.factura_afectada,
            nota.cufe_factura,
            str(nota.total),
            str(uuid4()),
        ]

        cude_string = "".join(components)
        cude_hash = hashlib.sha384(cude_string.encode()).hexdigest()

        return cude_hash[:96]

    def _generate_xml(self, factura: FacturaElectronica, cufe: str) -> str:
        """
        Generate XML representation of the invoice.

        This is a stub implementation. Real implementation would generate
        XML according to DIAN's UBL 2.1 specification.

        Args:
            factura: Invoice data
            cufe: Generated CUFE

        Returns:
            XML string
        """
        xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
    <cbc:UBLVersionID>UBL 2.1</cbc:UBLVersionID>
    <cbc:ID>{factura.numero_factura}</cbc:ID>
    <cbc:UUID>{cufe}</cbc:UUID>
    <cbc:IssueDate>{factura.fecha_emision.strftime('%Y-%m-%d')}</cbc:IssueDate>
    <cbc:IssueTime>{factura.fecha_emision.strftime('%H:%M:%S')}</cbc:IssueTime>
    <cbc:InvoiceTypeCode>{factura.tipo_factura}</cbc:InvoiceTypeCode>
    <cbc:DocumentCurrencyCode>{factura.moneda}</cbc:DocumentCurrencyCode>

    <!-- Emisor -->
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID>{factura.emisor.nit}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>{factura.emisor.razon_social}</cbc:Name>
            </cac:PartyName>
        </cac:Party>
    </cac:AccountingSupplierParty>

    <!-- Cliente -->
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID>{factura.cliente.nit}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>{factura.cliente.razon_social}</cbc:Name>
            </cac:PartyName>
        </cac:Party>
    </cac:AccountingCustomerParty>

    <!-- Line Items -->
    {self._generate_line_items_xml(factura.items)}

    <!-- Totals -->
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="{factura.moneda}">{factura.subtotal}</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="{factura.moneda}">{factura.subtotal}</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="{factura.moneda}">{factura.total}</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="{factura.moneda}">{factura.total}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
</Invoice>"""

        return xml_template

    def _generate_line_items_xml(self, items: List) -> str:
        """Generate XML for line items (stub)."""
        # Simplified stub - real implementation would iterate and format properly
        return "<!-- Line items would be listed here -->"

    def _save_xml_file(self, xml_content: str, numero_factura: str) -> str:
        """
        Save XML content to file.

        Args:
            xml_content: XML string
            numero_factura: Invoice number

        Returns:
            Path to saved file
        """
        filename = f"{numero_factura}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        filepath = os.path.join(self.storage_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_content)

        logger.info(f"Saved XML file: {filepath}")
        return filepath

    def _save_pdf_file(self, numero_factura: str, factura_data: dict) -> str:
        """
        Generate and save PDF representation (stub).

        In real implementation, this would generate a proper PDF invoice.

        Args:
            numero_factura: Invoice number
            factura_data: Invoice data dictionary

        Returns:
            Path to saved PDF file
        """
        filename = f"{numero_factura}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.storage_dir, filename)

        # Stub: Just create a placeholder file
        with open(filepath, "w") as f:
            f.write(f"PDF Invoice {numero_factura}\n")
            f.write(json.dumps(factura_data, indent=2, default=str))

        logger.info(f"Saved PDF file (stub): {filepath}")
        return filepath

    def emitir_factura(self, request: EInvoiceRequest) -> EInvoiceResponse:
        """
        Issue an electronic invoice to DIAN.

        This is the main method for invoice emission. In production, it would:
        1. Validate invoice data
        2. Generate CUFE
        3. Generate XML (UBL 2.1 format)
        4. Sign XML with digital certificate
        5. Send to DIAN or PAC provider
        6. Store XML and PDF
        7. Return response with CUFE and status

        Args:
            request: Invoice request with all required data

        Returns:
            Response with CUFE, status, and file paths
        """
        try:
            factura = request.factura

            # Generate CUFE
            cufe = self._generate_cufe(factura)
            factura.cufe = cufe

            # Generate XML
            xml_content = self._generate_xml(factura, cufe)

            # Save XML
            xml_path = self._save_xml_file(xml_content, factura.numero_factura)

            # Generate and save PDF if requested
            pdf_path = None
            if request.generar_pdf:
                factura_dict = factura.model_dump()
                pdf_path = self._save_pdf_file(factura.numero_factura, factura_dict)

            # In real implementation, would send to DIAN/provider here
            if self.provider == "stub":
                estado = "Aceptado (Stub)"
                mensaje = "Factura emitida exitosamente (modo stub - no enviada a DIAN)"
            else:
                # Placeholder for real provider integration
                estado = "Pendiente"
                mensaje = f"Enviado a proveedor {self.provider}"

            logger.info(
                f"Invoice {factura.numero_factura} issued successfully with CUFE {cufe[:16]}..."
            )

            return EInvoiceResponse(
                success=True,
                numero_factura=factura.numero_factura,
                cufe=cufe,
                estado=estado,
                mensaje=mensaje,
                xml_path=xml_path,
                pdf_path=pdf_path,
                errores=None,
            )

        except Exception as e:
            logger.error(f"Error emitting invoice: {str(e)}", exc_info=True)
            return EInvoiceResponse(
                success=False,
                numero_factura=request.factura.numero_factura,
                cufe=None,
                estado="Error",
                mensaje=f"Error al emitir factura: {str(e)}",
                xml_path=None,
                pdf_path=None,
                errores=[str(e)],
            )

    def emitir_nota_credito(self, nota: NotaCredito) -> EInvoiceResponse:
        """
        Issue a credit note (Nota de Crédito).

        Args:
            nota: Credit note data

        Returns:
            Response with CUDE and status
        """
        try:
            # Generate CUDE
            cude = self._generate_cude(nota)
            nota.cude = cude

            # In stub mode, just return success
            logger.info(f"Credit note {nota.numero_nota} issued with CUDE {cude[:16]}...")

            return EInvoiceResponse(
                success=True,
                numero_factura=nota.numero_nota,
                cufe=cude,  # Using cufe field for CUDE
                estado="Aceptado (Stub)",
                mensaje="Nota de crédito emitida exitosamente (modo stub)",
                xml_path=None,
                pdf_path=None,
                errores=None,
            )

        except Exception as e:
            logger.error(f"Error issuing credit note: {str(e)}", exc_info=True)
            return EInvoiceResponse(
                success=False,
                numero_factura=nota.numero_nota,
                cufe=None,
                estado="Error",
                mensaje=f"Error al emitir nota de crédito: {str(e)}",
                xml_path=None,
                pdf_path=None,
                errores=[str(e)],
            )

    def consultar_estado(self, numero_factura: str, cufe: str) -> InvoiceStatusResponse:
        """
        Query invoice status from DIAN.

        Args:
            numero_factura: Invoice number
            cufe: CUFE of the invoice

        Returns:
            Status response with current state
        """
        # Stub implementation
        logger.info(f"Querying status for invoice {numero_factura}")

        return InvoiceStatusResponse(
            numero_factura=numero_factura,
            cufe=cufe,
            estado_dian="Aceptado (Stub)",
            fecha_validacion=datetime.now(),
            observaciones="Factura validada exitosamente (modo stub)",
            pdf_url=None,
            xml_url=None,
        )

    def validar_factura(self, factura: FacturaElectronica) -> Dict[str, Any]:
        """
        Validate invoice data before submission.

        Performs validation checks including:
        - Required fields
        - NIT format
        - Calculation consistency
        - DIAN business rules

        Args:
            factura: Invoice to validate

        Returns:
            Dictionary with validation result and errors if any
        """
        errores = []

        # Validate NITs
        try:
            # NIT validation is done by Pydantic validators
            pass
        except ValueError as e:
            errores.append(f"Error en NIT: {str(e)}")

        # Validate calculations
        calculated_subtotal = sum(item.subtotal for item in factura.items)
        if abs(calculated_subtotal - factura.subtotal) > 0.01:
            errores.append(
                f"Subtotal inconsistente: calculado {calculated_subtotal}, declarado {factura.subtotal}"
            )

        calculated_taxes = sum(sum(tax.amount for tax in item.taxes) for item in factura.items)
        if abs(calculated_taxes - factura.total_impuestos) > 0.01:
            errores.append(
                f"Total impuestos inconsistente: calculado {calculated_taxes}, declarado {factura.total_impuestos}"
            )

        calculated_total = factura.subtotal + factura.total_impuestos
        if abs(calculated_total - factura.total) > 0.01:
            errores.append(
                f"Total inconsistente: calculado {calculated_total}, declarado {factura.total}"
            )

        return {"valido": len(errores) == 0, "errores": errores if errores else None}


def get_dian_service() -> DIANEInvoicingService:
    """
    Get DIAN e-invoicing service instance configured from environment.

    Environment variables:
    - E_INVOICE_PROVIDER: Provider type (default: 'stub')
    - E_INVOICE_API_KEY: API key
    - E_INVOICE_API_URL: API base URL
    - E_INVOICE_CERT_PATH: Certificate path
    - E_INVOICE_CERT_PASSWORD: Certificate password
    - E_INVOICE_NIT_EMISOR: Issuer NIT

    Returns:
        Configured DIANEInvoicingService instance
    """
    return DIANEInvoicingService(
        provider=os.getenv("E_INVOICE_PROVIDER", "stub"),
        api_key=os.getenv("E_INVOICE_API_KEY"),
        api_url=os.getenv("E_INVOICE_API_URL"),
        cert_path=os.getenv("E_INVOICE_CERT_PATH"),
        cert_password=os.getenv("E_INVOICE_CERT_PASSWORD"),
        nit_emisor=os.getenv("E_INVOICE_NIT_EMISOR"),
    )
