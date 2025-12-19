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
│  ┌──────────▼───────────────────────────────────────────────┐  │
│  │            Techaura Sales Sync                           │  │
│  │            - Sales Retrieval                             │  │
│  │            - Data Transformation                         │  │
│  │            - Financial Integration                       │  │
│  │            - Mock Data (Stub)                            │  │
│  └──────────┬───────────────────────────────────────────────┘  │
└─────────────┼───────────────────────────────────────────────────┘
              │
   ┌──────────▼──────────┐
   │ Techaura API        │
   │ (External System)   │
   └──────────┬──────────┘
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
- **📊 Sales Sync**: Integration with Techaura sales system (stub implementation ready for production)

### Technical Features
- **Function Calling**: AI model can invoke financial tools automatically
- **Configurable Models**: Switch between Gemini Pro and Flash models
- **Temperature Control**: Adjust response creativity
- **Type-Safe**: Full type hints and validation with Pydantic
- **Tested**: Comprehensive test suite with pytest
- **Linted**: Code quality with ruff and black

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
│   │   └── schemas.py               # Pydantic models for API
│   ├── services/
│   │   ├── __init__.py
│   │   ├── vertex_ai.py             # Vertex AI integration
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
