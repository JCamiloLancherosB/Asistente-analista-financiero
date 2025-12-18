"""Configuration module for the financial assistant application."""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Google Cloud & Vertex AI
    project_id: str = Field(..., description="GCP Project ID")
    location: str = Field(default="us-central1", description="GCP Location")
    gemini_model: str = Field(default="gemini-1.5-pro", description="Gemini model name")
    google_application_credentials: str = Field(..., description="Path to service account JSON")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    frontend_url: str = Field(default="http://localhost:5173", description="Frontend URL for CORS")

    # Model parameters
    default_temperature: float = Field(default=0.7, description="Default temperature")
    max_output_tokens: int = Field(default=2048, description="Max output tokens")

    # DIAN E-Invoicing Configuration
    e_invoice_provider: str = Field(
        default="stub", description="E-invoice provider: stub, dian_api, pac_provider"
    )
    e_invoice_api_key: Optional[str] = Field(None, description="E-invoice provider API key")
    e_invoice_api_url: Optional[str] = Field(None, description="E-invoice provider API URL")
    e_invoice_cert_path: Optional[str] = Field(None, description="Path to e-invoice certificate")
    e_invoice_cert_password: Optional[str] = Field(None, description="Certificate password")
    e_invoice_nit_emisor: Optional[str] = Field(None, description="NIT of the invoice issuer")
    e_invoice_storage_dir: str = Field(
        default="/tmp/einvoices", description="Directory for storing invoice XML/PDF files"
    )

    # Techaura Sales Sync Configuration
    techaura_api_key: Optional[str] = Field(None, description="Techaura API key")
    techaura_api_url: Optional[str] = Field(None, description="Techaura API base URL")
    techaura_company_id: Optional[str] = Field(None, description="Techaura company ID")


# Global settings instance
settings = Settings()  # type: ignore[call-arg]
