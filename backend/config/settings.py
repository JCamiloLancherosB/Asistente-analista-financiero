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

    # Techaura Sales Sync Configuration
    techaura_api_key: Optional[str] = Field(None, description="Techaura API key")
    techaura_api_url: Optional[str] = Field(None, description="Techaura API base URL")
    techaura_company_id: Optional[str] = Field(None, description="Techaura company ID")


# Global settings instance
# Note: Pydantic Settings loads values from environment at runtime,
# so mypy can't verify the required arguments at type-check time
settings = Settings()  # type: ignore[call-arg]
