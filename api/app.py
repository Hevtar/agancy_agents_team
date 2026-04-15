"""
FastAPI application factory for the Agency system.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import prometheus_client

from core.config import settings
from api.routes import router
from api.metrics import MetricsMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    # Startup
    print("Agency API starting up...")
    yield
    # Shutdown
    print("Agency API shutting down...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="Agency Agents Team API",
        description="REST API for the multi-agent marketing agency system",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Metrics middleware
    app.add_middleware(MetricsMiddleware)
    
    # Include routers
    app.include_router(router, prefix="/api/v1")
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "version": "1.0.0"}
    
    # Metrics endpoint for Prometheus
    @app.get("/metrics")
    async def metrics():
        return prometheus_client.generate_latest(prometheus_client.CONTENT_TYPE_LATEST)
    
    return app