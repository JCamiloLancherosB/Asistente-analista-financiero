"""Tests for financial tools."""

import pytest
from backend.tools.financial_tools import FinancialTools


@pytest.fixture
def financial_tools():
    """Create a fresh instance of financial tools for each test."""
    return FinancialTools()


class TestLiquidityRatios:
    """Test liquidity ratio calculations."""

    def test_current_ratio(self, financial_tools):
        """Test current ratio calculation."""
        ratios = financial_tools.calculate_liquidity_ratios(
            activos_corrientes=150000, pasivos_corrientes=100000
        )
        assert ratios["liquidez_corriente"] == 1.5

    def test_quick_ratio(self, financial_tools):
        """Test quick ratio calculation."""
        ratios = financial_tools.calculate_liquidity_ratios(
            activos_corrientes=150000, pasivos_corrientes=100000, inventarios=30000
        )
        assert ratios["prueba_acida"] == 1.2

    def test_zero_liabilities(self, financial_tools):
        """Test with zero liabilities."""
        ratios = financial_tools.calculate_liquidity_ratios(
            activos_corrientes=150000, pasivos_corrientes=0
        )
        assert ratios["liquidez_corriente"] is None


class TestLeverageRatios:
    """Test leverage ratio calculations."""

    def test_debt_ratio(self, financial_tools):
        """Test debt ratio calculation."""
        ratios = financial_tools.calculate_leverage_ratios(
            pasivos_totales=500000, activos_totales=1000000, patrimonio=500000
        )
        assert ratios["razon_endeudamiento"] == 0.5

    def test_debt_to_equity(self, financial_tools):
        """Test debt to equity ratio."""
        ratios = financial_tools.calculate_leverage_ratios(
            pasivos_totales=400000, activos_totales=1000000, patrimonio=600000
        )
        assert abs(ratios["deuda_patrimonio"] - 0.6667) < 0.001


class TestProfitabilityRatios:
    """Test profitability ratio calculations."""

    def test_net_margin(self, financial_tools):
        """Test net profit margin calculation."""
        ratios = financial_tools.calculate_profitability_ratios(
            utilidad_neta=50000, ingresos=500000, activos_totales=1000000, patrimonio=600000
        )
        assert ratios["margen_neto"] == 10.0

    def test_roa(self, financial_tools):
        """Test return on assets calculation."""
        ratios = financial_tools.calculate_profitability_ratios(
            utilidad_neta=100000, ingresos=500000, activos_totales=1000000, patrimonio=600000
        )
        assert ratios["roa"] == 10.0

    def test_roe(self, financial_tools):
        """Test return on equity calculation."""
        ratios = financial_tools.calculate_profitability_ratios(
            utilidad_neta=120000, ingresos=500000, activos_totales=1000000, patrimonio=600000
        )
        assert ratios["roe"] == 20.0


class TestDCFProjection:
    """Test DCF projection."""

    def test_simple_dcf(self, financial_tools):
        """Test simple DCF calculation."""
        result = financial_tools.simple_dcf_projection(
            flujo_caja_actual=100000, tasa_crecimiento=5, tasa_descuento=10, periodos=3
        )
        assert "proyecciones" in result
        assert len(result["proyecciones"]) == 3
        assert "vp_flujos" in result
        assert result["vp_flujos"] > 0


class TestRiskAlerts:
    """Test risk alert generation."""

    def test_low_liquidity_alert(self, financial_tools):
        """Test alert for low liquidity."""
        ratios = {"liquidez_corriente": 0.8}
        alerts = financial_tools.generate_risk_alerts(ratios)
        assert len(alerts) > 0
        assert any(a["severity"] == "high" for a in alerts)

    def test_high_leverage_alert(self, financial_tools):
        """Test alert for high leverage."""
        ratios = {"razon_endeudamiento": 0.75}
        alerts = financial_tools.generate_risk_alerts(ratios)
        assert len(alerts) > 0
        assert any(a["category"] == "endeudamiento" for a in alerts)

    def test_negative_margin_alert(self, financial_tools):
        """Test alert for negative margin."""
        ratios = {"margen_neto": -5.0}
        alerts = financial_tools.generate_risk_alerts(ratios)
        assert len(alerts) > 0
        assert any(a["severity"] == "critical" for a in alerts)


class TestDataStorage:
    """Test financial data storage."""

    def test_store_data(self, financial_tools):
        """Test storing financial data."""
        data = [
            {"periodo": "2023", "ingresos": 100000, "utilidad": 10000},
            {"periodo": "2024", "ingresos": 120000, "utilidad": 15000},
        ]
        result = financial_tools.store_financial_data(data, "test_data")
        assert "test_data" in financial_tools.data_store
        assert len(financial_tools.data_store["test_data"]) == 2

    def test_trend_analysis(self, financial_tools):
        """Test trend analysis."""
        data = [
            {"ingresos": 100000},
            {"ingresos": 120000},
            {"ingresos": 150000},
        ]
        financial_tools.store_financial_data(data, "trend_test")
        result = financial_tools.analyze_trend("trend_test", "ingresos")
        assert "growth_rate" in result
        assert result["growth_rate"] == 50.0  # (150000 - 100000) / 100000 * 100
