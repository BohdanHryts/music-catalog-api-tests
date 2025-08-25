import os
from typing import List, Optional
from pydantic import BaseSettings, validator


class APISettings(BaseSettings):
    """API Configuration Settings"""
    
    # Base Configuration
    BASE_URL: str = "https://api.example.com"
    API_VERSION: str = "v1"
    TIMEOUT: int = 30
    
    # Authentication
    API_KEY: Optional[str] = None
    
    # Test Configuration
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    # Catalog Settings
    DEFAULT_CATALOG_IDS: List[str] = ["nugs", "playDead"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @validator('BASE_URL')
    def validate_base_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('BASE_URL must start with http:// or https://')
        return v.rstrip('/')

    @property
    def search_endpoint(self) -> str:
        return f"{self.BASE_URL}/{self.API_VERSION}/search"
    
    @property
    def release_changes_endpoint(self) -> str:
        return f"{self.BASE_URL}/{self.API_VERSION}/release-changes"


# Global settings instance
settings = APISettings()