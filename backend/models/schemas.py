"""Data models for the financial assistant API."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    messages: List[Message] = Field(..., description="Conversation history")
    model: Optional[str] = Field(None, description="Model to use (overrides default)")
    temperature: Optional[float] = Field(None, description="Temperature (0-1)")
    max_tokens: Optional[int] = Field(None, description="Max output tokens")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    model_config = {"protected_namespaces": ()}

    response: str = Field(..., description="Assistant response")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(
        None, description="Tool calls made during generation"
    )
    model_used: str = Field(..., description="Model used for generation")


class FinancialData(BaseModel):
    """Financial data from CSV upload."""

    data: List[Dict[str, Any]] = Field(..., description="Parsed financial data")
    columns: List[str] = Field(..., description="Column names")
    row_count: int = Field(..., description="Number of rows")


class UploadResponse(BaseModel):
    """Response for CSV upload."""

    message: str = Field(..., description="Status message")
    data_summary: FinancialData = Field(..., description="Summary of uploaded data")


class FinancialRatios(BaseModel):
    """Financial ratios calculated from statements."""

    liquidez_corriente: Optional[float] = Field(
        None, description="Current ratio (activos corrientes / pasivos corrientes)"
    )
    prueba_acida: Optional[float] = Field(None, description="Quick ratio (acid test)")
    razon_endeudamiento: Optional[float] = Field(
        None, description="Debt ratio (pasivos totales / activos totales)"
    )
    roe: Optional[float] = Field(None, description="Return on equity (utilidad neta / patrimonio)")
    roa: Optional[float] = Field(
        None, description="Return on assets (utilidad neta / activos totales)"
    )
    margen_neto: Optional[float] = Field(
        None, description="Net profit margin (utilidad neta / ingresos)"
    )


class RiskAlert(BaseModel):
    """Risk alert from financial analysis."""

    severity: str = Field(..., description="Severity: low, medium, high, critical")
    category: str = Field(..., description="Risk category")
    message: str = Field(..., description="Alert message")
    recommendation: Optional[str] = Field(None, description="Recommended action")
