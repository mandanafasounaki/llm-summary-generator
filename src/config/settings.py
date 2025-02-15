from pydantic_settings import BaseSettings
from typing import Optional, Literal

class Settings(BaseSettings):
    """
    Application settings and configuration
    """

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = 'anthropic'

    # Documents
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()