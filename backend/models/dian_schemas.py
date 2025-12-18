"""Data models and validation schemas for DIAN Colombia e-invoicing."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class TaxDetail(BaseModel):
    """Tax detail for invoice line item."""

    tax_type: str = Field(..., description="Tax type (IVA, INC, etc.)")
    rate: float = Field(..., description="Tax rate percentage")
    amount: float = Field(..., description="Tax amount")


class InvoiceLineItem(BaseModel):
    """Line item in an invoice."""

    line_number: int = Field(..., description="Line number")
    description: str = Field(..., description="Product/service description")
    quantity: float = Field(..., description="Quantity")
    unit_price: float = Field(..., description="Unit price")
    subtotal: float = Field(..., description="Subtotal before taxes")
    taxes: List[TaxDetail] = Field(default_factory=list, description="Taxes applied")
    total: float = Field(..., description="Line total including taxes")


class ClienteInfo(BaseModel):
    """Client information for invoice."""

    nit: str = Field(..., description="NIT (Tax ID) of the client")
    razon_social: str = Field(..., description="Legal name")
    direccion: str = Field(..., description="Address")
    ciudad: str = Field(..., description="City")
    departamento: str = Field(..., description="Department/State")
    email: str = Field(..., description="Email address")
    telefono: Optional[str] = Field(None, description="Phone number")

    @field_validator("nit")
    @classmethod
    def validate_nit(cls, v: str) -> str:
        """Validate NIT format (basic validation)."""
        # Remove spaces and hyphens
        nit_clean = v.replace(" ", "").replace("-", "")
        if not nit_clean.isdigit() or len(nit_clean) < 9:
            raise ValueError("NIT must be at least 9 digits")
        return v


class EmisorInfo(BaseModel):
    """Issuer information for invoice."""

    nit: str = Field(..., description="NIT (Tax ID) of the issuer")
    razon_social: str = Field(..., description="Legal name")
    direccion: str = Field(..., description="Address")
    ciudad: str = Field(..., description="City")
    departamento: str = Field(..., description="Department/State")
    regimen_fiscal: str = Field(
        default="Responsable de IVA", description="Tax regime (Responsable de IVA, etc.)"
    )

    @field_validator("nit")
    @classmethod
    def validate_nit(cls, v: str) -> str:
        """Validate NIT format (basic validation)."""
        nit_clean = v.replace(" ", "").replace("-", "")
        if not nit_clean.isdigit() or len(nit_clean) < 9:
            raise ValueError("NIT must be at least 9 digits")
        return v


class FacturaElectronica(BaseModel):
    """Colombian electronic invoice (Factura Electrónica)."""

    numero_factura: str = Field(..., description="Invoice number")
    fecha_emision: datetime = Field(default_factory=datetime.now, description="Issue date and time")
    tipo_factura: str = Field(default="01", description="Invoice type (01=Factura de venta, etc.)")
    moneda: str = Field(default="COP", description="Currency code (COP for Colombian Peso)")

    # Parties
    emisor: EmisorInfo = Field(..., description="Issuer information")
    cliente: ClienteInfo = Field(..., description="Client information")

    # Line items
    items: List[InvoiceLineItem] = Field(..., description="Invoice line items")

    # Totals
    subtotal: float = Field(..., description="Subtotal before taxes")
    total_impuestos: float = Field(..., description="Total taxes")
    total: float = Field(..., description="Invoice total")

    # Payment terms
    medio_pago: str = Field(default="10", description="Payment method code")
    forma_pago: str = Field(default="1", description="Payment form (1=Contado, 2=Credito)")

    # DIAN specific fields
    cufe: Optional[str] = Field(None, description="CUFE (Unique code for electronic invoice)")
    qr_code: Optional[str] = Field(None, description="QR code for invoice verification")
    xml_content: Optional[str] = Field(None, description="XML content of the invoice")

    @field_validator("moneda")
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Validate currency code."""
        if v not in ["COP", "USD", "EUR"]:
            raise ValueError("Currency must be COP, USD, or EUR")
        return v


class NotaCredito(BaseModel):
    """Credit note (Nota de Crédito) for invoice corrections."""

    numero_nota: str = Field(..., description="Credit note number")
    fecha_emision: datetime = Field(default_factory=datetime.now, description="Issue date and time")
    factura_afectada: str = Field(..., description="Original invoice number being credited")
    cufe_factura: str = Field(..., description="CUFE of the original invoice")

    # Parties
    emisor: EmisorInfo = Field(..., description="Issuer information")
    cliente: ClienteInfo = Field(..., description="Client information")

    # Reason for credit note
    motivo: str = Field(..., description="Reason for the credit note")
    concepto_correccion: str = Field(
        ..., description="Correction concept (Devolucion, Descuento, etc.)"
    )

    # Amounts
    subtotal: float = Field(..., description="Subtotal to credit")
    total_impuestos: float = Field(..., description="Total taxes to credit")
    total: float = Field(..., description="Total amount to credit")

    # DIAN specific fields
    cude: Optional[str] = Field(None, description="CUDE (Unique code for electronic credit note)")
    xml_content: Optional[str] = Field(None, description="XML content of the credit note")


class InvoiceStatusResponse(BaseModel):
    """Response for invoice status query."""

    numero_factura: str = Field(..., description="Invoice number")
    cufe: str = Field(..., description="CUFE of the invoice")
    estado_dian: str = Field(..., description="DIAN status (Aceptado, Rechazado, En proceso, etc.)")
    fecha_validacion: Optional[datetime] = Field(None, description="DIAN validation timestamp")
    observaciones: Optional[str] = Field(None, description="DIAN observations or errors")
    pdf_url: Optional[str] = Field(None, description="URL to download PDF representation")
    xml_url: Optional[str] = Field(None, description="URL to download XML file")


class EInvoiceRequest(BaseModel):
    """Request to issue an electronic invoice."""

    factura: FacturaElectronica = Field(..., description="Invoice data")
    generar_pdf: bool = Field(
        default=True, description="Generate PDF representation of the invoice"
    )
    enviar_email: bool = Field(default=True, description="Send invoice to client email")


class EInvoiceResponse(BaseModel):
    """Response after issuing an electronic invoice."""

    success: bool = Field(..., description="Whether the operation was successful")
    numero_factura: str = Field(..., description="Invoice number")
    cufe: Optional[str] = Field(None, description="Generated CUFE")
    estado: str = Field(..., description="Current status")
    mensaje: str = Field(..., description="Status message")
    xml_path: Optional[str] = Field(None, description="Path to generated XML file")
    pdf_path: Optional[str] = Field(None, description="Path to generated PDF file")
    errores: Optional[List[str]] = Field(None, description="List of errors if any")
