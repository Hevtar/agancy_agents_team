"""
REST API module for the Agency system.
"""
from api.app import create_app
from api.routes import router

__all__ = ["create_app", "router"]