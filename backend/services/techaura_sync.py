"""Techaura sales synchronization service stub.

This module provides a stub connector for syncing sales data from Techaura.
In production, replace the stub methods with actual API calls to Techaura.

Environment variables:
- TECHAURA_API_KEY: API key for Techaura
- TECHAURA_API_URL: Base URL for Techaura API
- TECHAURA_COMPANY_ID: Company ID in Techaura system
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TechauraClient:
    """Client for Techaura sales system integration."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        company_id: Optional[str] = None,
    ):
        """
        Initialize Techaura client.

        Args:
            api_key: API key for authentication
            api_url: Base URL for Techaura API
            company_id: Company identifier in Techaura
        """
        self.api_key = api_key or os.getenv("TECHAURA_API_KEY", "stub_api_key")
        self.api_url = api_url or os.getenv("TECHAURA_API_URL", "https://api.techaura.example.com")
        self.company_id = company_id or os.getenv("TECHAURA_COMPANY_ID", "stub_company")

        self.is_stub = self.api_key == "stub_api_key"

        if self.is_stub:
            logger.info("Techaura client initialized in STUB mode (no real API calls)")
        else:
            logger.info(f"Techaura client initialized for company {self.company_id}")

    def _make_request(
        self, endpoint: str, method: str = "GET", data: Optional[dict] = None
    ) -> Dict:
        """
        Make HTTP request to Techaura API.

        In stub mode, returns mock data. In production, implement actual HTTP calls.

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            data: Request payload

        Returns:
            Response data as dictionary
        """
        if self.is_stub:
            logger.debug(f"STUB: Would call {method} {self.api_url}{endpoint}")
            return {"status": "stub", "data": []}

        # Real implementation would use requests or httpx
        # Example:
        # import httpx
        # headers = {"Authorization": f"Bearer {self.api_key}"}
        # response = httpx.request(method, f"{self.api_url}{endpoint}",
        #                         json=data, headers=headers)
        # return response.json()

        raise NotImplementedError("Real API integration not implemented. Use stub mode.")

    def get_sales(
        self,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve sales data from Techaura.

        Args:
            fecha_inicio: Start date for sales query (default: 30 days ago)
            fecha_fin: End date for sales query (default: now)
            limit: Maximum number of records to retrieve

        Returns:
            List of sale records
        """
        if fecha_inicio is None:
            fecha_inicio = datetime.now() - timedelta(days=30)
        if fecha_fin is None:
            fecha_fin = datetime.now()

        logger.info(
            f"Fetching sales from {fecha_inicio.date()} to {fecha_fin.date()} (limit: {limit})"
        )

        if self.is_stub:
            # Return mock data in stub mode
            return self._generate_mock_sales(fecha_inicio, fecha_fin, limit)

        # Real implementation
        endpoint = f"/api/v1/companies/{self.company_id}/sales"
        params = {
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "limit": limit,
        }

        # Would make actual API call here
        response = self._make_request(endpoint, "GET", params)
        return response.get("data", [])

    def _generate_mock_sales(
        self, fecha_inicio: datetime, fecha_fin: datetime, limit: int
    ) -> List[Dict[str, Any]]:
        """
        Generate mock sales data for testing.

        Args:
            fecha_inicio: Start date
            fecha_fin: End date
            limit: Number of records to generate

        Returns:
            List of mock sale records
        """
        mock_sales = []
        days_diff = (fecha_fin - fecha_inicio).days
        records_to_generate = min(limit, max(1, days_diff))

        for i in range(records_to_generate):
            date = fecha_inicio + timedelta(days=i * (days_diff / records_to_generate))
            sale = {
                "id": f"SALE-{i+1:05d}",
                "fecha": date.isoformat(),
                "cliente_nit": f"900{i:06d}-{i % 10}",
                "cliente_nombre": f"Cliente {i+1}",
                "productos": [
                    {
                        "codigo": f"PROD-{(i % 10) + 1:03d}",
                        "nombre": f"Producto {(i % 10) + 1}",
                        "cantidad": 1 + (i % 5),
                        "precio_unitario": 50000 + (i * 1000),
                        "subtotal": (1 + (i % 5)) * (50000 + (i * 1000)),
                    }
                ],
                "subtotal": (1 + (i % 5)) * (50000 + (i * 1000)),
                "impuestos": (1 + (i % 5)) * (50000 + (i * 1000)) * 0.19,
                "total": (1 + (i % 5)) * (50000 + (i * 1000)) * 1.19,
                "metodo_pago": "Tarjeta" if i % 2 == 0 else "Efectivo",
                "estado": "Completada",
            }
            mock_sales.append(sale)

        logger.info(f"Generated {len(mock_sales)} mock sales records")
        return mock_sales

    def get_sale_details(self, sale_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific sale.

        Args:
            sale_id: Sale identifier

        Returns:
            Sale details or None if not found
        """
        logger.info(f"Fetching details for sale {sale_id}")

        if self.is_stub:
            # Return mock sale detail
            return {
                "id": sale_id,
                "fecha": datetime.now().isoformat(),
                "cliente_nit": "900123456-7",
                "cliente_nombre": "Cliente Ejemplo",
                "cliente_email": "cliente@example.com",
                "cliente_telefono": "+57 300 1234567",
                "cliente_direccion": "Calle 123 #45-67, Bogotá",
                "productos": [
                    {
                        "codigo": "PROD-001",
                        "nombre": "Producto Ejemplo",
                        "cantidad": 2,
                        "precio_unitario": 100000,
                        "descuento": 0,
                        "subtotal": 200000,
                        "iva": 38000,
                        "total": 238000,
                    }
                ],
                "subtotal": 200000,
                "descuentos": 0,
                "impuestos": 38000,
                "total": 238000,
                "metodo_pago": "Tarjeta de Crédito",
                "estado": "Completada",
                "vendedor": "Juan Pérez",
                "notas": "Venta de prueba",
            }

        endpoint = f"/api/v1/sales/{sale_id}"
        response = self._make_request(endpoint, "GET")
        return response.get("data")

    def sync_sales_to_financial_data(
        self, fecha_inicio: Optional[datetime] = None, fecha_fin: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Sync sales data and convert to financial data format.

        This method retrieves sales from Techaura and formats them for
        financial analysis tools.

        Args:
            fecha_inicio: Start date for sync
            fecha_fin: End date for sync

        Returns:
            Dictionary with sync summary and formatted data
        """
        sales = self.get_sales(fecha_inicio, fecha_fin)

        # Convert to financial data format
        financial_data = []
        total_ventas = 0
        total_impuestos = 0

        for sale in sales:
            total_ventas += sale.get("subtotal", 0)
            total_impuestos += sale.get("impuestos", 0)

            financial_record = {
                "fecha": sale.get("fecha"),
                "venta_id": sale.get("id"),
                "cliente": sale.get("cliente_nombre"),
                "subtotal": sale.get("subtotal", 0),
                "impuestos": sale.get("impuestos", 0),
                "total": sale.get("total", 0),
                "metodo_pago": sale.get("metodo_pago"),
            }
            financial_data.append(financial_record)

        summary = {
            "total_registros": len(sales),
            "periodo_inicio": fecha_inicio.isoformat() if fecha_inicio else None,
            "periodo_fin": fecha_fin.isoformat() if fecha_fin else None,
            "total_ventas": total_ventas,
            "total_impuestos": total_impuestos,
            "total_general": total_ventas + total_impuestos,
        }

        logger.info(f"Synced {len(sales)} sales records. Total sales: ${total_ventas:,.2f}")

        return {"summary": summary, "data": financial_data}


def get_techaura_client() -> TechauraClient:
    """
    Get Techaura client instance configured from environment.

    Environment variables:
    - TECHAURA_API_KEY: API key (default: stub mode)
    - TECHAURA_API_URL: API base URL
    - TECHAURA_COMPANY_ID: Company ID

    Returns:
        Configured TechauraClient instance
    """
    return TechauraClient(
        api_key=os.getenv("TECHAURA_API_KEY"),
        api_url=os.getenv("TECHAURA_API_URL"),
        company_id=os.getenv("TECHAURA_COMPANY_ID"),
    )
