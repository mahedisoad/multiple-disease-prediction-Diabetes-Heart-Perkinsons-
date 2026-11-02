# Multiple Disease Prediction System 🏥

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.0+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com/)

An end-to-end, production-grade **Multiple Disease Prediction Web Application** built with **FastAPI**, **Scikit-learn**, **Pydantic v2**, and a modern **Vanilla JavaScript / CSS** frontend. The system provides real-time risk assessment for:

- 🩸 **Diabetes** (PIMA Indian Diabetes Dataset — SVM Linear Classifier)
- ❤️ **Heart Disease** (Cleveland Heart Disease Dataset — Logistic Regression)
- 🧠 **Parkinson's Disease** (Oxford Parkinson's Voice Biomarkers — SVM Linear Classifier)

---

## 🌟 Key Features

- **Trained ML Models Loaded at Startup**: Models are deserialized once in FastAPI's `lifespan` manager for zero-overhead inference.
- **Strict Data Validation**: Pydantic v2 schemas validate input types, boundary limits, and physical medical constraints.
- **RESTful API**: OpenAPI 3.0 / Swagger UI documentation automatically generated at `/docs`.
- **Health Checks & Monitoring**: `/api/health` endpoint for uptime monitoring and model verification.
- **Modern Responsive UI**: Dark glassmorphic design, micro-animations, and dynamic form generation without external JS framework bloat.
- **Automated Test Suite**: 100% test pass rate with `pytest` and `httpx`.
- **Cloud-Ready**: Native configuration for Render.com deployment via `render.yaml`.

---

## 🧬 Supported Diseases & Models

| Disease | Model Algorithm | Features | Accuracy | Endpoint |
|---|---|:---:|:---:|---|
| **Diabetes** | Support Vector Machine (Linear Kernel) | 8 | 77.27% | `POST /api/predict/diabetes` |
| **Heart Disease** | Logistic Regression | 13 | 81.97% | `POST /api/predict/heart` |
| **Parkinson's** | Support Vector Machine (Linear Kernel) | 22 | 87.18% | `POST /api/predict/parkinsons` |

---

## 📁 Project Structure

```text
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── prediction.py         # Prediction & health check routes
│   ├── core/
│   │   ├── __init__.py
│   │   └── logging_config.py         # Structured logging configuration
│   ├── models/                       # Active serialized .sav model artifacts
│   │   ├── diabetes_model.sav
│   │   ├── heart_disease_model.sav
│   │   └── parkinsons_model.sav
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── prediction.py             # Pydantic v2 request/response schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_loader.py           # Model singleton loader & cache
│   │   └── prediction_service.py     # Inference logic & confidence scoring
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css             # Glassmorphism design system
│   │   ├── js/
│   │   │   └── app.js                # Dynamic frontend client logic
│   │   ├── index.html                # Responsive web dashboard
│   │   ├── robots.txt                # Search engine crawler instructions
│   │   └── sitemap.xml               # SEO XML sitemap
│   ├── config.py                     # Environment settings (HOST, PORT, etc.)
│   └── main.py                       # FastAPI application & lifespan
├── tests/
│   ├── __init__.py
│   ├── test_health.py                # Health & metadata endpoint tests
│   └── test_predictions.py           # ML prediction, validation, edge cases
├── .env.example                      # Sample environment variables
├── .gitignore                        # Git ignore rules
├── README.md                         # Project documentation
├── render.yaml                       # Render.com infrastructure as code
├── requirements.txt                  # Pinned Python dependencies
└── run.py                            # Application entry point script
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/mahedisoad/multiple-disease-prediction-Diabetes-Heart-Perkinsons-.git
cd multiple-disease-prediction-Diabetes-Heart-Perkinsons-
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python run.py
```
Or run directly using Uvicorn:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser:
- **Web Dashboard**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Running Tests

Execute the automated test suite with `pytest`:
```bash
pytest -v tests/
```

---

## ☁️ Deployment on Render

This project includes a native `render.yaml` blueprint:

1. Sign in to [Render.com](https://render.com).
2. Click **New +** > **Blueprint**.
3. Connect your GitHub repository: `https://github.com/mahedisoad/multiple-disease-prediction-Diabetes-Heart-Perkinsons-`.
4. Render will automatically detect `render.yaml`:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/api/health`
   - **Plan**: Free
5. Click **Apply** to deploy.

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `Multiple Disease Prediction System` | Title of the application |
| `APP_VERSION` | `1.0.0` | API version |
| `DEBUG` | `False` | Enable reload/debug mode |
| `HOST` | `0.0.0.0` | Server listen address |
| `PORT` | `8000` | Port number (dynamically assigned by Render) |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins |

---

## ⚠️ Medical Disclaimer

This application is designed for **educational and screening support purposes only**. Predictions generated by machine learning models should not replace professional medical diagnosis, advice, or treatment. Always consult a qualified healthcare provider for any health-related concerns.

---

## 📄 License

MIT License. Free to use, adapt, and build upon.
>>>>>>> 02247a3 (feat: complete production-ready multiple disease prediction web app with FastAPI, ML models, and tests)
