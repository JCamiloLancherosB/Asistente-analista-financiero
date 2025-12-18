# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Prerequisites Check
```bash
python --version  # Should be 3.11+
node --version    # Should be 18+
```

### 2. Clone and Setup
```bash
git clone https://github.com/JCamiloLancherosB/Asistente-analista-financiero.git
cd Asistente-analista-financiero
```

### 3. Configure Environment
```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your values
# You need:
# - PROJECT_ID: Your GCP project ID
# - GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON
```

### 4. Install Dependencies
```bash
# Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend (in a new terminal)
cd frontend
npm install
cd ..
```

### 5. Run the Application
```bash
# Terminal 1: Start Backend
source venv/bin/activate
make dev
# Or: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Frontend
make frontend-dev
# Or: cd frontend && npm run dev
```

### 6. Open Your Browser
Navigate to `http://localhost:5173`

## 🎯 Try It Out

1. **Upload Sample Data**: Use the "📁 Cargar CSV" button and upload `sample_financial_data.csv`

2. **Ask Questions**:
   - "Calcula los ratios de liquidez para el año 2023"
   - "Analiza las tendencias de ingresos"
   - "Genera una proyección DCF con flujo de caja de 200000, crecimiento del 8% y descuento del 12%"
   - "Identifica riesgos financieros en los datos"

3. **Experiment**:
   - Switch between Gemini models (Pro vs Flash)
   - Adjust temperature slider (lower = more focused, higher = more creative)
   - Watch the tool calls to see which functions the AI uses

## 🐛 Common Issues

**"Vertex AI API not enabled"**
```bash
gcloud services enable aiplatform.googleapis.com
```

**"Authentication error"**
- Check your service account JSON file exists
- Verify the path in `.env` is correct
- Try: `gcloud auth application-default login`

**"Import errors"**
- Make sure you activated the virtual environment
- Run: `source venv/bin/activate`

**"Port already in use"**
- Backend: Change `API_PORT` in `.env`
- Frontend: Vite will automatically try the next available port

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check the [API docs](http://localhost:8000/docs) when backend is running
- Explore financial tool functions in `backend/tools/financial_tools.py`
- Customize the system prompt in `backend/services/vertex_ai.py`

## 🔒 Security Note

Never commit your `.env` file or service account JSON to version control!
