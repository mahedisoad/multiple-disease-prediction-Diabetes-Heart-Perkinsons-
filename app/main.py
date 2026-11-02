"""
FastAPI application entry point.
Loads models at startup via lifespan context manager, mounts static files,
and registers API routes.
"""
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add project root directory to sys.path so running directly works without ModuleNotFoundError
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.logging_config import logger
from app.api.routes.prediction import router as prediction_router
from app.services.model_loader import model_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: load models on startup, cleanup on shutdown."""
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("Loading ML models from: %s", settings.MODEL_DIR)

    model_store.load_all(settings.MODEL_DIR)

    logger.info("Application ready — models loaded successfully")
    yield
    logger.info("Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(prediction_router)

# Static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the main frontend HTML page."""
    return FileResponse("app/static/index.html")


@app.get("/robots.txt", include_in_schema=False)
async def serve_robots():
    """Serve robots.txt for search engines."""
    return FileResponse("app/static/robots.txt", media_type="text/plain")


@app.get("/sitemap.xml", include_in_schema=False)
async def serve_sitemap():
    """Serve sitemap.xml for search engines."""
    return FileResponse("app/static/sitemap.xml", media_type="application/xml")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
