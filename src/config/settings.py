from pydantic_settings import BaseSettings
from typing import Optional, Literal, ClassVar

class Settings(BaseSettings):
    """
    Application settings and configuration
    """

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACEHUB_API_TOKEN: str  
    DEFAULT_MODEL: str = 'anthropic'
    USE_GEMMA: str = True

    # Documents
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()