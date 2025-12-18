"""Vertex AI service for Gemini model interaction."""

import os
from typing import Any, Dict, List, Optional

import vertexai
from vertexai.preview import generative_models

from backend.config import settings
from backend.models.schemas import Message


class VertexAIService:
    """Service for interacting with Vertex AI Gemini models."""

    def __init__(self):
        """Initialize Vertex AI service."""
        # Set credentials environment variable
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

        # Initialize Vertex AI
        vertexai.init(project=settings.project_id, location=settings.location)

        # Define financial analysis tools for function calling
        self.tools = self._create_tools()

        # Initialize model
        self.model_name = settings.gemini_model
        self.model = generative_models.GenerativeModel(
            self.model_name,
            tools=[self.tools] if self.tools else None,
            system_instruction=self._get_system_instruction(),
        )

    def _get_system_instruction(self) -> str:
        """Get system instruction for the financial analyst."""
        return """Eres un asistente analista financiero experto. Tu rol es ayudar a analizar estados financieros,
calcular ratios financieros clave, identificar tendencias, proyectar flujos de caja y alertar sobre riesgos potenciales.

Capacidades:
- Analizar estados financieros (balance general, estado de resultados, flujo de caja)
- Calcular ratios de liquidez (razón corriente, prueba ácida)
- Calcular ratios de endeudamiento (razón de endeudamiento, deuda/patrimonio)
- Calcular ratios de rentabilidad (ROE, ROA, margen neto)
- Analizar tendencias en datos financieros
- Realizar proyecciones simples de flujo de caja descontado (DCF)
- Identificar alertas de riesgo basadas en los indicadores financieros

Cuando recibas datos financieros:
1. Primero almacena los datos usando la función correspondiente
2. Calcula los ratios relevantes según la información disponible
3. Analiza tendencias si hay datos históricos
4. Genera alertas de riesgo basadas en los ratios
5. Proporciona recomendaciones claras y accionables

Siempre explica tus cálculos y proporciona contexto sobre qué significan los ratios y por qué son importantes.
Usa terminología financiera en español y sé preciso en tus análisis."""

    def _create_tools(self) -> Optional[generative_models.Tool]:
        """Create function declarations for financial tools."""
        # Tool for storing financial data
        store_data_func = generative_models.FunctionDeclaration(
            name="store_financial_data",
            description="Almacena datos financieros para análisis posterior. Usar cuando se recibe un CSV o datos tabulares.",
            parameters={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "description": "Lista de objetos con datos financieros",
                        "items": {"type": "object"},
                    },
                    "dataset_name": {
                        "type": "string",
                        "description": "Nombre para identificar este conjunto de datos",
                        "default": "main",
                    },
                },
                "required": ["data"],
            },
        )

        # Tool for liquidity ratios
        liquidity_func = generative_models.FunctionDeclaration(
            name="calculate_liquidity_ratios",
            description="Calcula ratios de liquidez (razón corriente y prueba ácida)",
            parameters={
                "type": "object",
                "properties": {
                    "activos_corrientes": {
                        "type": "number",
                        "description": "Activos corrientes o circulantes",
                    },
                    "pasivos_corrientes": {
                        "type": "number",
                        "description": "Pasivos corrientes o circulantes",
                    },
                    "inventarios": {
                        "type": "number",
                        "description": "Inventarios (opcional, para prueba ácida)",
                    },
                },
                "required": ["activos_corrientes", "pasivos_corrientes"],
            },
        )

        # Tool for leverage ratios
        leverage_func = generative_models.FunctionDeclaration(
            name="calculate_leverage_ratios",
            description="Calcula ratios de endeudamiento (razón de endeudamiento y deuda/patrimonio)",
            parameters={
                "type": "object",
                "properties": {
                    "pasivos_totales": {"type": "number", "description": "Pasivos totales"},
                    "activos_totales": {"type": "number", "description": "Activos totales"},
                    "patrimonio": {
                        "type": "number",
                        "description": "Patrimonio o capital contable",
                    },
                },
                "required": ["pasivos_totales", "activos_totales", "patrimonio"],
            },
        )

        # Tool for profitability ratios
        profitability_func = generative_models.FunctionDeclaration(
            name="calculate_profitability_ratios",
            description="Calcula ratios de rentabilidad (ROE, ROA, margen neto)",
            parameters={
                "type": "object",
                "properties": {
                    "utilidad_neta": {
                        "type": "number",
                        "description": "Utilidad neta o ganancia neta",
                    },
                    "ingresos": {"type": "number", "description": "Ingresos totales o ventas"},
                    "activos_totales": {"type": "number", "description": "Activos totales"},
                    "patrimonio": {
                        "type": "number",
                        "description": "Patrimonio o capital contable",
                    },
                },
                "required": ["utilidad_neta", "ingresos", "activos_totales", "patrimonio"],
            },
        )

        # Tool for trend analysis
        trend_func = generative_models.FunctionDeclaration(
            name="analyze_trend",
            description="Analiza tendencias en datos financieros almacenados",
            parameters={
                "type": "object",
                "properties": {
                    "dataset_name": {
                        "type": "string",
                        "description": "Nombre del conjunto de datos",
                        "default": "main",
                    },
                    "column": {
                        "type": "string",
                        "description": "Nombre de la columna a analizar (ej: ingresos, utilidad_neta)",
                        "default": "ingresos",
                    },
                },
                "required": [],
            },
        )

        # Tool for DCF projection
        dcf_func = generative_models.FunctionDeclaration(
            name="simple_dcf_projection",
            description="Realiza una proyección simple de flujo de caja descontado (DCF)",
            parameters={
                "type": "object",
                "properties": {
                    "flujo_caja_actual": {
                        "type": "number",
                        "description": "Flujo de caja actual o del último periodo",
                    },
                    "tasa_crecimiento": {
                        "type": "number",
                        "description": "Tasa de crecimiento esperada (porcentaje, ej: 5 para 5%)",
                    },
                    "tasa_descuento": {
                        "type": "number",
                        "description": "Tasa de descuento o costo de capital (porcentaje, ej: 10 para 10%)",
                    },
                    "periodos": {
                        "type": "integer",
                        "description": "Número de periodos a proyectar",
                        "default": 5,
                    },
                },
                "required": ["flujo_caja_actual", "tasa_crecimiento", "tasa_descuento"],
            },
        )

        # Tool for risk alerts
        risk_func = generative_models.FunctionDeclaration(
            name="generate_risk_alerts",
            description="Genera alertas de riesgo basadas en ratios financieros",
            parameters={
                "type": "object",
                "properties": {
                    "ratios": {
                        "type": "object",
                        "description": "Diccionario con ratios calculados (liquidez_corriente, razon_endeudamiento, margen_neto, etc.)",
                    }
                },
                "required": ["ratios"],
            },
        )

        # Combine all tools
        return generative_models.Tool(
            function_declarations=[
                store_data_func,
                liquidity_func,
                leverage_func,
                profitability_func,
                trend_func,
                dcf_func,
                risk_func,
            ]
        )

    def _convert_messages_to_contents(
        self, messages: List[Message]
    ) -> List[generative_models.Content]:
        """Convert API messages to Vertex AI Content format."""
        contents = []
        for msg in messages:
            if msg.role == "user":
                contents.append(
                    generative_models.Content(
                        role="user", parts=[generative_models.Part.from_text(msg.content)]
                    )
                )
            elif msg.role == "assistant":
                # Skip system messages, they're handled separately
                contents.append(
                    generative_models.Content(
                        role="model", parts=[generative_models.Part.from_text(msg.content)]
                    )
                )
        return contents

    async def generate_response(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate a response using Gemini model.

        Args:
            messages: Conversation history
            temperature: Temperature for generation
            max_tokens: Maximum output tokens

        Returns:
            Dictionary with response and metadata
        """
        # Convert messages
        contents = self._convert_messages_to_contents(messages)

        # Configure generation
        generation_config = generative_models.GenerationConfig(
            temperature=temperature or settings.default_temperature,
            max_output_tokens=max_tokens or settings.max_output_tokens,
        )

        # Start chat session
        chat = self.model.start_chat(history=contents[:-1] if len(contents) > 1 else [])

        # Generate response
        response = await chat.send_message_async(
            contents[-1].parts if contents else [],
            generation_config=generation_config,
        )

        # Extract response text and function calls
        response_text = response.text if hasattr(response, "text") else ""
        tool_calls = []

        # Check for function calls
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, "content") and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        fc = part.function_call
                        tool_calls.append(
                            {"name": fc.name, "arguments": dict(fc.args) if fc.args else {}}
                        )

        return {
            "response": response_text,
            "tool_calls": tool_calls if tool_calls else None,
            "model_used": self.model_name,
        }


# Create service lazily
_vertex_service = None


def get_vertex_service() -> VertexAIService:
    """Get or create the Vertex AI service instance."""
    global _vertex_service
    if _vertex_service is None:
        _vertex_service = VertexAIService()
    return _vertex_service
