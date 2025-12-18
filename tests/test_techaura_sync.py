"""Tests for Techaura sales sync service."""

import pytest
from datetime import datetime, timedelta
from backend.services.techaura_sync import TechauraClient, get_techaura_client


@pytest.fixture
def techaura_client():
    """Create Techaura client in stub mode."""
    return TechauraClient(api_key="stub_api_key")


class TestTechauraClient:
    """Test Techaura sales sync client."""

    def test_client_initialization_stub(self):
        """Test client initialization in stub mode."""
        client = TechauraClient(api_key="stub_api_key")
        assert client.is_stub is True
        assert client.api_key == "stub_api_key"

    def test_get_sales(self, techaura_client):
        """Test fetching sales data."""
        fecha_inicio = datetime.now() - timedelta(days=7)
        fecha_fin = datetime.now()

        sales = techaura_client.get_sales(fecha_inicio, fecha_fin, limit=10)

        assert isinstance(sales, list)
        assert len(sales) > 0
        assert len(sales) <= 10

        # Check structure of first sale
        sale = sales[0]
        assert "id" in sale
        assert "fecha" in sale
        assert "cliente_nit" in sale
        assert "cliente_nombre" in sale
        assert "productos" in sale
        assert "subtotal" in sale
        assert "impuestos" in sale
        assert "total" in sale

    def test_get_sales_default_dates(self, techaura_client):
        """Test fetching sales with default date range."""
        sales = techaura_client.get_sales()
        assert isinstance(sales, list)
        # Should get data for last 30 days by default

    def test_get_sale_details(self, techaura_client):
        """Test fetching details for a specific sale."""
        sale_detail = techaura_client.get_sale_details("SALE-00001")

        assert sale_detail is not None
        assert "id" in sale_detail
        assert "cliente_nit" in sale_detail
        assert "productos" in sale_detail
        assert isinstance(sale_detail["productos"], list)

    def test_sync_sales_to_financial_data(self, techaura_client):
        """Test syncing sales to financial data format."""
        fecha_inicio = datetime.now() - timedelta(days=7)
        fecha_fin = datetime.now()

        result = techaura_client.sync_sales_to_financial_data(fecha_inicio, fecha_fin)

        assert "summary" in result
        assert "data" in result

        summary = result["summary"]
        assert "total_registros" in summary
        assert "total_ventas" in summary
        assert "total_impuestos" in summary
        assert "total_general" in summary

        assert summary["total_registros"] > 0
        assert summary["total_ventas"] >= 0
        assert summary["total_impuestos"] >= 0

        # Check financial data format
        data = result["data"]
        assert isinstance(data, list)
        if len(data) > 0:
            record = data[0]
            assert "fecha" in record
            assert "venta_id" in record
            assert "cliente" in record
            assert "subtotal" in record
            assert "impuestos" in record
            assert "total" in record

    def test_generate_mock_sales(self, techaura_client):
        """Test mock sales generation."""
        fecha_inicio = datetime(2024, 1, 1)
        fecha_fin = datetime(2024, 1, 10)

        mock_sales = techaura_client._generate_mock_sales(fecha_inicio, fecha_fin, 5)

        assert len(mock_sales) > 0
        assert len(mock_sales) <= 5

        # Verify data structure
        for sale in mock_sales:
            assert "id" in sale
            assert "fecha" in sale
            assert "total" in sale
            assert sale["total"] > 0

    def test_get_techaura_client_factory(self):
        """Test client factory function."""
        client = get_techaura_client()
        assert client is not None
        assert isinstance(client, TechauraClient)

    def test_financial_data_calculations(self, techaura_client):
        """Test that financial calculations are correct."""
        result = techaura_client.sync_sales_to_financial_data()

        summary = result["summary"]
        data = result["data"]

        # Verify totals match
        calculated_subtotal = sum(record["subtotal"] for record in data)
        calculated_impuestos = sum(record["impuestos"] for record in data)

        assert abs(calculated_subtotal - summary["total_ventas"]) < 0.01
        assert abs(calculated_impuestos - summary["total_impuestos"]) < 0.01

    def test_sales_data_types(self, techaura_client):
        """Test that sales data has correct types."""
        sales = techaura_client.get_sales(limit=1)

        if len(sales) > 0:
            sale = sales[0]
            assert isinstance(sale["id"], str)
            assert isinstance(sale["subtotal"], (int, float))
            assert isinstance(sale["impuestos"], (int, float))
            assert isinstance(sale["total"], (int, float))
            assert isinstance(sale["productos"], list)
