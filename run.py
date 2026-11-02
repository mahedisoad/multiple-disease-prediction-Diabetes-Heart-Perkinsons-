"""
Application launcher for Multiple Disease Prediction System.
Run this directly with:
    python run.py
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("==================================================")
    print(f" Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f" Open your browser: http://localhost:{settings.PORT}")
    print(f" API documentation: http://localhost:{settings.PORT}/docs")
    print("==================================================")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
