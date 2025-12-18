# 💰 Asistente Analista Financiero

AI-powered financial analysis assistant using Google Vertex AI Gemini and modern web technologies.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│                    (React + Vite Frontend)                       │
│  ┌────────────┬──────────────┬───────────────┬────────────┐    │
│  │ Chat UI    │ File Upload  │ Model Select  │  Controls  │    │
│  └────────────┴──────────────┴───────────────┴────────────┘    │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/REST API
┌─────────────────────────────▼───────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                         │  │
│  │  /api/chat  │  /api/upload  │  /api/health              │  │
│  └────────────┬─────────────┬──────────────────────────────┘  │
│               │             │                                   │
│  ┌────────────▼─────────┐  ┌▼──────────────────────────────┐  │
│  │  Vertex AI Service   │  │   Financial Tools             │  │
│  │  - Gemini Model      │  │   - Ratio Calculators         │  │
│  │  - Function Calling  │  │   - Trend Analysis            │  │
│  │  - System Prompt     │  │   - DCF Projections           │  │
│  └──────────┬───────────┘  │   - Risk Alerts               │  │
│             │              └───────────────────────────────┘  │
│             │                                                   │
│  ┌──────────▼───────────┐  ┌───────────────────────────────┐  │
│  │  DIAN E-Invoicing    │  │   Techaura Sales Sync         │  │
│  │  - Invoice Emission  │  │   - Sales Retrieval           │  │
│  │  - Credit Notes      │  │   - Data Transformation       │  │
│  │  - Status Query      │  │   - Financial Integration     │  │
│  │  - XML/PDF Gen       │  │   - Mock Data (Stub)          │  │
│  └──────────┬───────────┘  └───────────┬───────────────────┘  │
└─────────────┼──────────────────────────┼───────────────────────┘
              │                          │
    ┌─────────▼───────────┐   ┌──────────▼──────────┐
    │ DIAN API / PAC      │   │ Techaura API        │
    │ Provider            │   │ (External System)   │
    └─────────────────────┘   └─────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────────────┐
│              Google Cloud Vertex AI                              │
│                    Gemini Models                                 │
│         (gemini-1.5-pro / gemini-1.5-flash)                     │
└──────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Core Capabilities
- **AI-Powered Analysis**: Leverages Google Gemini models for intelligent financial analysis
- **Financial Ratios**: Calculate liquidity, leverage, and profitability ratios
- **Trend Analysis**: Analyze historical data trends and growth rates
- **DCF Projections**: Simple discounted cash flow projections
- **Risk Detection**: Automated alerts for financial risks
- **CSV Upload**: Easy data ingestion from CSV files
- **Conversational Interface**: Natural language interaction with chat history
- **🇨🇴 DIAN E-Invoicing**: Colombian electronic invoicing (factura electrónica) with stub integration
- **📊 Sales Sync**: Integration with Techaura sales system (stub implementation ready for production)

### Technical Features
- **Function Calling**: AI model can invoke financial tools automatically
- **Configurable Models**: Switch between Gemini Pro and Flash models
- **Temperature Control**: Adjust response creativity
- **Type-Safe**: Full type hints and validation with Pydantic
- **Tested**: Comprehensive test suite with pytest (39 tests)
- **Linted**: Code quality with ruff and black
- **E-Invoice Flow**: Complete DIAN integration with CUFE generation, XML/PDF storage, and validation

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Google Cloud Project with Vertex AI API enabled
- Service Account with Vertex AI permissions

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/JCamiloLancherosB/Asistente-analista-financiero.git
cd Asistente-analista-financiero
```

### 2. Google Cloud Setup

#### Enable Vertex AI API

```bash
gcloud services enable aiplatform.googleapis.com
```

#### Create Service Account

```bash
# Create service account
gcloud iam service-accounts create financial-assistant \
    --display-name="Financial Assistant Service Account"

# Grant Vertex AI User role
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:financial-assistant@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create credentials.json \
    --iam-account=financial-assistant@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

**Note**: Keep `credentials.json` secure and never commit it to version control.

#### Alternative: Use Application Default Credentials (ADC)

For local development, you can use ADC instead of a service account key:

```bash
gcloud auth application-default login
```

### 3. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install

# Or manually:
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your values
nano .env
```

Required environment variables:

```bash
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
GEMINI_MODEL=gemini-1.5-pro
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### 5. Frontend Setup

```bash
# Install frontend dependencies
make frontend-install

# Or manually:
cd frontend
npm install
cd ..
```

## 🏃 Running Locally

### Start Backend

```bash
# Using Make
make dev

# Or manually
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

### Start Frontend

In a new terminal:

```bash
# Using Make
make frontend-dev

# Or manually
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 🧪 Testing

### Run Tests

```bash
# Run all tests
make test

# Run with coverage
pytest -v --cov=backend tests/

# Run specific test file
pytest tests/test_financial_tools.py -v
```

### Linting and Formatting

```bash
# Check code quality
make lint

# Format code
make format
```

## 📊 Usage Examples

### Using the Web UI

1. Open `http://localhost:5173` in your browser
2. Upload a CSV file with financial data (optional)
3. Ask questions like:
   - "Calcula la razón corriente con activos corrientes de 150000 y pasivos corrientes de 100000"
   - "Analiza las tendencias de ingresos en los datos"
   - "Dame una proyección DCF con flujo de caja de 100000, crecimiento del 5% y descuento del 10%"

### Using the API (curl)

#### Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Calcula ratios de liquidez con activos corrientes 200000 y pasivos corrientes 100000"
      }
    ],
    "temperature": 0.7
  }'
```

#### Upload CSV

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@financial_data.csv"
```

### Sample CSV Format

Create a `financial_data.csv`:

```csv
periodo,ingresos,utilidad_neta,activos_totales,pasivos_totales,patrimonio
2021,1000000,100000,2000000,800000,1200000
2022,1200000,150000,2500000,900000,1600000
2023,1500000,200000,3000000,1000000,2000000
```

## 🇨🇴 DIAN Colombia E-Invoicing Integration

The system includes a complete framework for Colombian electronic invoicing (factura electrónica) compliance with DIAN regulations.

### E-Invoicing Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Invoice Creation                                              │
│    - Build FacturaElectronica with emisor, cliente, line items  │
│    - Validate NIT formats, calculations, required fields         │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ 2. CUFE Generation                                               │
│    - Generate Código Único de Factura Electrónica               │
│    - SHA-384 hash of invoice components                         │
│    - Ensures invoice uniqueness and integrity                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ 3. XML Generation                                                │
│    - Create UBL 2.1 compliant XML                               │
│    - Include all required DIAN fields                           │
│    - Format according to Colombian regulations                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ 4. Digital Signature (Production)                               │
│    - Sign XML with digital certificate (.p12)                   │
│    - Timestamp signature                                        │
│    - Validate certificate authority                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ 5. Transmission to DIAN                                         │
│    - Option A: Direct DIAN API (requires certification)         │
│    - Option B: PAC Provider (Proveedor Autorizado)              │
│    - Receive acceptance/rejection response                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ 6. Storage & Distribution                                       │
│    - Store XML and PDF locally or in cloud storage              │
│    - Send to client via email                                   │
│    - Update invoice status in system                            │
└─────────────────────────────────────────────────────────────────┘
```

### Configuration

The system supports three provider modes configured via environment variables:

1. **stub** (default): Testing mode with mock responses, no external API calls
2. **dian_api**: Direct integration with DIAN API (requires certification and credentials)
3. **pac_provider**: Integration via authorized PAC provider

Required environment variables (add to `.env`):

```bash
# E-Invoicing Provider Configuration
E_INVOICE_PROVIDER=stub                    # stub | dian_api | pac_provider
E_INVOICE_API_KEY=your-provider-api-key   # API key for PAC provider
E_INVOICE_API_URL=https://api.provider.com # Provider API URL
E_INVOICE_CERT_PATH=/path/to/cert.p12     # Digital certificate path
E_INVOICE_CERT_PASSWORD=cert-password      # Certificate password
E_INVOICE_NIT_EMISOR=900123456-7          # Your company NIT
E_INVOICE_STORAGE_DIR=/tmp/einvoices      # Storage for XML/PDF files
```

### Usage Examples

#### Creating and Emitting an Invoice

```python
from backend.services.dian_einvoicing import get_dian_service
from backend.models.dian_schemas import (
    FacturaElectronica, EmisorInfo, ClienteInfo,
    InvoiceLineItem, TaxDetail, EInvoiceRequest
)

# Initialize service
dian_service = get_dian_service()

# Create invoice
factura = FacturaElectronica(
    numero_factura="FE-001",
    emisor=EmisorInfo(
        nit="900123456-7",
        razon_social="Mi Empresa SAS",
        direccion="Calle 100 #20-30",
        ciudad="Bogotá",
        departamento="Cundinamarca"
    ),
    cliente=ClienteInfo(
        nit="900654321-8",
        razon_social="Cliente Ejemplo SAS",
        direccion="Carrera 50 #30-40",
        ciudad="Medellín",
        departamento="Antioquia",
        email="cliente@example.com"
    ),
    items=[
        InvoiceLineItem(
            line_number=1,
            description="Servicio de consultoría",
            quantity=1,
            unit_price=1000000,
            subtotal=1000000,
            taxes=[TaxDetail(tax_type="IVA", rate=19, amount=190000)],
            total=1190000
        )
    ],
    subtotal=1000000,
    total_impuestos=190000,
    total=1190000
)

# Emit invoice
request = EInvoiceRequest(factura=factura, generar_pdf=True)
response = dian_service.emitir_factura(request)

print(f"CUFE: {response.cufe}")
print(f"Status: {response.estado}")
print(f"XML: {response.xml_path}")
```

#### Issuing a Credit Note

```python
from backend.models.dian_schemas import NotaCredito

nota = NotaCredito(
    numero_nota="NC-001",
    factura_afectada="FE-001",
    cufe_factura="original-invoice-cufe",
    emisor=emisor_info,
    cliente=cliente_info,
    motivo="Devolución de mercancía",
    concepto_correccion="Devolucion",
    subtotal=100000,
    total_impuestos=19000,
    total=119000
)

response = dian_service.emitir_nota_credito(nota)
```

#### Querying Invoice Status

```python
status = dian_service.consultar_estado("FE-001", "cufe-value")
print(f"DIAN Status: {status.estado_dian}")
```

### Validation

The system includes comprehensive validation:

- **NIT Format**: Validates Colombian tax ID format (minimum 9 digits)
- **Calculation Consistency**: Ensures subtotals, taxes, and totals match
- **Required Fields**: Validates all mandatory DIAN fields
- **Currency Codes**: Validates allowed currency codes (COP, USD, EUR)

```python
# Validate before submission
validation = dian_service.validar_factura(factura)
if not validation["valido"]:
    print(f"Errors: {validation['errores']}")
```

### Integration with Real Providers

To integrate with production DIAN or a PAC provider:

1. **Obtain Credentials**:
   - Register with DIAN or choose a PAC provider (e.g., Carvajal, Andes SCD, FacturaElectronica.com)
   - Obtain API credentials and digital certificate
   - Complete certification process if using direct DIAN integration

2. **Update Configuration**:
   ```bash
   E_INVOICE_PROVIDER=pac_provider
   E_INVOICE_API_KEY=your_real_api_key
   E_INVOICE_API_URL=https://api.your-pac-provider.com
   E_INVOICE_CERT_PATH=/secure/path/to/certificate.p12
   E_INVOICE_CERT_PASSWORD=your_cert_password
   ```

3. **Implement Provider-Specific Logic**:
   - Replace stub methods in `backend/services/dian_einvoicing.py`
   - Implement `_make_request()` method for actual HTTP calls
   - Add provider-specific XML formatting if required
   - Implement proper certificate handling for signing

4. **Testing**:
   - Use provider's test/sandbox environment first
   - Validate with sample invoices
   - Get certification approval before production use

### File Storage

Generated XML and PDF files are stored in the directory specified by `E_INVOICE_STORAGE_DIR`. 

For production, consider:
- Using cloud storage (Google Cloud Storage, AWS S3)
- Implementing backup strategies
- Setting up retention policies according to DIAN regulations (5 years minimum)

### Recommended PAC Providers for Colombia

- **Carvajal Tecnología y Servicios**: https://www.carvajaltecnologiayservicios.com/
- **Andes SCD**: https://www.andesscd.com.co/
- **FacturaElectronica.com**: https://www.facturaelectronica.com/
- **Serti**: https://www.serti.co/

## 📊 Techaura Sales Sync

The system includes integration with Techaura sales system to automatically sync sales data for financial analysis.

### Configuration

```bash
TECHAURA_API_KEY=your-techaura-api-key
TECHAURA_API_URL=https://api.techaura.com
TECHAURA_COMPANY_ID=your-company-id
```

### Usage

```python
from backend.services.techaura_sync import get_techaura_client
from datetime import datetime, timedelta

# Initialize client
techaura = get_techaura_client()

# Sync sales from last 30 days
result = techaura.sync_sales_to_financial_data(
    fecha_inicio=datetime.now() - timedelta(days=30),
    fecha_fin=datetime.now()
)

print(f"Synced {result['summary']['total_registros']} sales")
print(f"Total sales: ${result['summary']['total_ventas']:,.2f}")

# Access formatted financial data
financial_data = result['data']
```

The stub implementation generates realistic mock data for testing. Replace with actual API calls in production.

## 🚀 Deployment to Cloud Run

### Build and Deploy

```bash
# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/financial-assistant

# Deploy to Cloud Run
gcloud run deploy financial-assistant \
  --image gcr.io/YOUR_PROJECT_ID/financial-assistant \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=YOUR_PROJECT_ID \
  --set-env-vars LOCATION=us-central1 \
  --set-env-vars GEMINI_MODEL=gemini-1.5-pro
```

### Using the Deploy Script

```bash
chmod +x deploy.sh
./deploy.sh YOUR_PROJECT_ID
```

## 🎯 System Prompt Design

The assistant is configured with a comprehensive system prompt that:

1. **Defines Role**: Expert financial analyst specializing in ratio analysis
2. **Lists Capabilities**: All available financial tools and functions
3. **Provides Workflow**: Step-by-step analysis approach
4. **Sets Tone**: Professional, clear, and actionable in Spanish
5. **Emphasizes Context**: Always explain calculations and their significance

The prompt is designed to:
- Encourage use of function calling for calculations
- Provide contextual explanations with numbers
- Generate actionable recommendations
- Use proper Spanish financial terminology

## 🛠️ Tool Functions Exposed to AI

The AI can call these Python functions automatically:

| Function | Purpose | Parameters |
|----------|---------|------------|
| `store_financial_data` | Store CSV data | data, dataset_name |
| `calculate_liquidity_ratios` | Liquidity analysis | activos_corrientes, pasivos_corrientes, inventarios |
| `calculate_leverage_ratios` | Debt analysis | pasivos_totales, activos_totales, patrimonio |
| `calculate_profitability_ratios` | Profitability metrics | utilidad_neta, ingresos, activos_totales, patrimonio |
| `analyze_trend` | Trend analysis | dataset_name, column |
| `simple_dcf_projection` | DCF valuation | flujo_caja_actual, tasa_crecimiento, tasa_descuento, periodos |
| `generate_risk_alerts` | Risk detection | ratios |

## 📝 Project Structure

```
.
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                # API endpoints
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Configuration & env validation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py               # Pydantic models for API
│   │   └── dian_schemas.py          # DIAN e-invoicing schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── vertex_ai.py             # Vertex AI integration
│   │   ├── dian_einvoicing.py       # DIAN e-invoicing service
│   │   └── techaura_sync.py         # Techaura sales sync
│   ├── tools/
│   │   ├── __init__.py
│   │   └── financial_tools.py       # Financial analysis functions
│   ├── __init__.py
│   └── main.py                 # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatMessage.css
│   │   │   ├── FileUpload.jsx
│   │   │   └── FileUpload.css
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_financial_tools.py
│   ├── test_dian_einvoicing.py     # DIAN e-invoicing tests
│   └── test_techaura_sync.py       # Techaura sync tests
├── .env.example
├── .gitignore
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 🔒 Security Notes

1. **Never commit credentials**: The `.gitignore` excludes all `.json` files except specific frontend configs
2. **Use environment variables**: All secrets are loaded from `.env`
3. **Rotate keys regularly**: Service account keys should be rotated periodically
4. **Principle of least privilege**: Grant only necessary IAM roles
5. **CORS configuration**: Adjust allowed origins for production

## 🐛 Troubleshooting

### Import Errors

If you get import errors, ensure you're in the project root and using the virtual environment:

```bash
source venv/bin/activate  # Activate venv
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Add to Python path
```

### Vertex AI Authentication Errors

1. Verify credentials file exists and path is correct in `.env`
2. Check service account has `roles/aiplatform.user` role
3. Ensure Vertex AI API is enabled in your project
4. Try using ADC: `gcloud auth application-default login`

### Frontend Connection Issues

1. Verify backend is running on port 8000
2. Check CORS settings in `backend/main.py`
3. Ensure `.env` has correct `FRONTEND_URL`

## 📚 Additional Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)

## 🤝 Contributing

This is a demonstration project. For production use, consider:

- Adding authentication and authorization
- Implementing persistent storage (PostgreSQL, BigQuery)
- Adding rate limiting and quotas
- Enhanced error handling and logging
- Monitoring and observability
- CI/CD pipelines

## 📄 License

MIT License - Feel free to use this as a template for your own projects.

## 🙏 Acknowledgments

- Google Cloud Vertex AI team for the Gemini models
- FastAPI community for the excellent framework
- React and Vite teams for modern frontend tools
