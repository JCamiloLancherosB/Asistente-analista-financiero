"""Financial analysis tools for the AI assistant."""

from typing import Any, Dict, List, Optional

import pandas as pd


class FinancialTools:
    """Collection of financial analysis tools exposed to the AI model."""

    def __init__(self):
        """Initialize financial tools."""
        self.data_store: Dict[str, pd.DataFrame] = {}

    def store_financial_data(self, data: List[Dict[str, Any]], dataset_name: str = "main") -> str:
        """
        Store financial data for analysis.

        Args:
            data: List of dictionaries containing financial data
            dataset_name: Name to identify this dataset

        Returns:
            Confirmation message
        """
        df = pd.DataFrame(data)
        self.data_store[dataset_name] = df
        return f"Stored {len(df)} rows of financial data as '{dataset_name}'. Columns: {list(df.columns)}"

    def calculate_liquidity_ratios(
        self,
        activos_corrientes: float,
        pasivos_corrientes: float,
        inventarios: Optional[float] = None,
    ) -> Dict[str, float]:
        """
        Calculate liquidity ratios.

        Args:
            activos_corrientes: Current assets
            pasivos_corrientes: Current liabilities
            inventarios: Inventory (optional, for quick ratio)

        Returns:
            Dictionary with liquidity ratios
        """
        ratios = {}

        # Current ratio (razón corriente)
        if pasivos_corrientes > 0:
            ratios["liquidez_corriente"] = activos_corrientes / pasivos_corrientes
        else:
            ratios["liquidez_corriente"] = None

        # Quick ratio (prueba ácida)
        if inventarios is not None and pasivos_corrientes > 0:
            ratios["prueba_acida"] = (activos_corrientes - inventarios) / pasivos_corrientes
        else:
            ratios["prueba_acida"] = None

        return ratios

    def calculate_leverage_ratios(
        self, pasivos_totales: float, activos_totales: float, patrimonio: float
    ) -> Dict[str, float]:
        """
        Calculate leverage/debt ratios.

        Args:
            pasivos_totales: Total liabilities
            activos_totales: Total assets
            patrimonio: Equity

        Returns:
            Dictionary with leverage ratios
        """
        ratios = {}

        # Debt ratio (razón de endeudamiento)
        if activos_totales > 0:
            ratios["razon_endeudamiento"] = pasivos_totales / activos_totales
        else:
            ratios["razon_endeudamiento"] = None

        # Debt to equity
        if patrimonio > 0:
            ratios["deuda_patrimonio"] = pasivos_totales / patrimonio
        else:
            ratios["deuda_patrimonio"] = None

        return ratios

    def calculate_profitability_ratios(
        self, utilidad_neta: float, ingresos: float, activos_totales: float, patrimonio: float
    ) -> Dict[str, float]:
        """
        Calculate profitability ratios.

        Args:
            utilidad_neta: Net income
            ingresos: Revenue/sales
            activos_totales: Total assets
            patrimonio: Equity

        Returns:
            Dictionary with profitability ratios
        """
        ratios = {}

        # Net profit margin (margen de utilidad neta)
        if ingresos > 0:
            ratios["margen_neto"] = (utilidad_neta / ingresos) * 100
        else:
            ratios["margen_neto"] = None

        # Return on Assets (ROA)
        if activos_totales > 0:
            ratios["roa"] = (utilidad_neta / activos_totales) * 100
        else:
            ratios["roa"] = None

        # Return on Equity (ROE)
        if patrimonio > 0:
            ratios["roe"] = (utilidad_neta / patrimonio) * 100
        else:
            ratios["roe"] = None

        return ratios

    def analyze_trend(self, dataset_name: str = "main", column: str = "ingresos") -> Dict[str, Any]:
        """
        Analyze trend for a specific column.

        Args:
            dataset_name: Name of the dataset to analyze
            column: Column name to analyze

        Returns:
            Dictionary with trend analysis
        """
        if dataset_name not in self.data_store:
            return {"error": f"Dataset '{dataset_name}' not found"}

        df = self.data_store[dataset_name]

        if column not in df.columns:
            return {"error": f"Column '{column}' not found in dataset"}

        try:
            values = pd.to_numeric(df[column], errors="coerce").dropna()
            if len(values) < 2:
                return {"error": "Not enough data points for trend analysis"}

            trend = {
                "column": column,
                "data_points": len(values),
                "mean": float(values.mean()),
                "median": float(values.median()),
                "std": float(values.std()),
                "min": float(values.min()),
                "max": float(values.max()),
                "growth_rate": None,
            }

            # Calculate simple growth rate if data is sequential
            if len(values) >= 2:
                first_value = values.iloc[0]
                last_value = values.iloc[-1]
                if first_value > 0:
                    growth_rate = ((last_value - first_value) / first_value) * 100
                    trend["growth_rate"] = float(growth_rate)

            return trend

        except Exception as e:
            return {"error": f"Error analyzing trend: {str(e)}"}

    def simple_dcf_projection(
        self,
        flujo_caja_actual: float,
        tasa_crecimiento: float,
        tasa_descuento: float,
        periodos: int = 5,
    ) -> Dict[str, Any]:
        """
        Simple DCF (Discounted Cash Flow) projection.

        Args:
            flujo_caja_actual: Current cash flow
            tasa_crecimiento: Growth rate (as percentage, e.g., 5 for 5%)
            tasa_descuento: Discount rate (as percentage, e.g., 10 for 10%)
            periodos: Number of periods to project

        Returns:
            Dictionary with DCF projection
        """
        g = tasa_crecimiento / 100
        r = tasa_descuento / 100

        proyecciones = []
        vp_total = 0

        for i in range(1, periodos + 1):
            flujo = flujo_caja_actual * ((1 + g) ** i)
            vp = flujo / ((1 + r) ** i)
            vp_total += vp
            proyecciones.append(
                {"periodo": i, "flujo_proyectado": round(flujo, 2), "valor_presente": round(vp, 2)}
            )

        # Simple terminal value (perpetuity)
        if r > g:
            flujo_terminal = flujo_caja_actual * ((1 + g) ** periodos) * (1 + g)
            valor_terminal = flujo_terminal / (r - g)
            vp_terminal = valor_terminal / ((1 + r) ** periodos)
        else:
            vp_terminal = 0

        return {
            "proyecciones": proyecciones,
            "vp_flujos": round(vp_total, 2),
            "vp_terminal": round(vp_terminal, 2),
            "valor_total": round(vp_total + vp_terminal, 2),
            "tasa_crecimiento": tasa_crecimiento,
            "tasa_descuento": tasa_descuento,
        }

    def generate_risk_alerts(self, ratios: Dict[str, float]) -> List[Dict[str, str]]:
        """
        Generate risk alerts based on financial ratios.

        Args:
            ratios: Dictionary of calculated ratios

        Returns:
            List of risk alerts
        """
        alerts = []

        # Liquidity alerts
        if "liquidez_corriente" in ratios and ratios["liquidez_corriente"] is not None:
            if ratios["liquidez_corriente"] < 1.0:
                alerts.append(
                    {
                        "severity": "high",
                        "category": "liquidez",
                        "message": f"Razón corriente baja ({ratios['liquidez_corriente']:.2f}). La empresa puede tener dificultades para cumplir obligaciones de corto plazo.",
                        "recommendation": "Evaluar opciones para mejorar liquidez: reducir gastos, acelerar cobranza, o conseguir financiamiento.",
                    }
                )
            elif ratios["liquidez_corriente"] < 1.5:
                alerts.append(
                    {
                        "severity": "medium",
                        "category": "liquidez",
                        "message": f"Razón corriente moderada ({ratios['liquidez_corriente']:.2f}). Monitorear de cerca.",
                        "recommendation": "Mantener un colchón de liquidez adecuado.",
                    }
                )

        # Leverage alerts
        if "razon_endeudamiento" in ratios and ratios["razon_endeudamiento"] is not None:
            if ratios["razon_endeudamiento"] > 0.7:
                alerts.append(
                    {
                        "severity": "high",
                        "category": "endeudamiento",
                        "message": f"Nivel de endeudamiento alto ({ratios['razon_endeudamiento']:.2%}). La empresa está altamente apalancada.",
                        "recommendation": "Considerar reducir deuda o aumentar capital propio.",
                    }
                )
            elif ratios["razon_endeudamiento"] > 0.5:
                alerts.append(
                    {
                        "severity": "medium",
                        "category": "endeudamiento",
                        "message": f"Nivel de endeudamiento moderado-alto ({ratios['razon_endeudamiento']:.2%}).",
                        "recommendation": "Monitorear capacidad de servicio de deuda.",
                    }
                )

        # Profitability alerts
        if "margen_neto" in ratios and ratios["margen_neto"] is not None:
            if ratios["margen_neto"] < 0:
                alerts.append(
                    {
                        "severity": "critical",
                        "category": "rentabilidad",
                        "message": f"Margen neto negativo ({ratios['margen_neto']:.2f}%). La empresa está operando con pérdidas.",
                        "recommendation": "Analizar estructura de costos y buscar eficiencias operativas urgentemente.",
                    }
                )
            elif ratios["margen_neto"] < 5:
                alerts.append(
                    {
                        "severity": "medium",
                        "category": "rentabilidad",
                        "message": f"Margen neto bajo ({ratios['margen_neto']:.2f}%). Rentabilidad limitada.",
                        "recommendation": "Buscar oportunidades para mejorar márgenes o reducir costos.",
                    }
                )

        return alerts


# Global instance
financial_tools = FinancialTools()
