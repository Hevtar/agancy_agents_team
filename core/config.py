"""
Application configuration using Pydantic Settings.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Application
    app_env: str = "development"
    app_debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    secret_key: str = "change-me-in-production"
    
    # Polza.Ai Configuration
    polza_ai_api_key: str = ""
    polza_ai_base_url: str = "https://polza.ai/api/v1"
    
    # Database Configuration
    postgres_db: str = "agency_db"
    postgres_user: str = "agency_user"
    postgres_password: str = "agency_password"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    
    @property
    def database_url(self) -> str:
        """Get SQLAlchemy database URL."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def sync_database_url(self) -> str:
        """Get synchronous database URL for Alembic."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # Redis Configuration
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    @property
    def redis_url(self) -> str:
        """Get Redis URL for Celery."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # ChromaDB Configuration
    chromadb_host: str = "chromadb"
    chromadb_port: int = 8000
    chromadb_collection_agency: str = "agency_team_kb"
    chromadb_collection_processes: str = "agency_processes_kb"
    
    # Celery Configuration
    celery_broker_url: Optional[str] = None
    celery_result_backend: Optional[str] = None
    
    @property
    def effective_celery_broker_url(self) -> str:
        """Get effective Celery broker URL."""
        return self.celery_broker_url or self.redis_url
    
    @property
    def effective_celery_result_backend(self) -> str:
        """Get effective Celery result backend."""
        return self.celery_result_backend or f"redis://{self.redis_host}:{self.redis_port}/1"
    
    # Monitoring
    prometheus_port: int = 9090
    grafana_port: int = 3000
    
    # Token Budget
    daily_token_budget: int = 100000
    token_budget_warning_threshold: float = 0.80
    
    # Sandbox Configuration
    sandbox_mock_polza: bool = False
    sandbox_token_limit: int = 10000
    sandbox_max_agents: int = 5
    
    # Knowledge Base
    knowledge_base_path: str = "./knowledge_base"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/agency.log"


# Singleton instance
settings = Settings()