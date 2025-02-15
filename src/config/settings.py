from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, Literal, ClassVar

class Settings(BaseSettings):
    """
    Application settings and configuration
    """
    model_config = ConfigDict(env_file = ".env", case_sensitive = True)

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACEHUB_API_TOKEN: str  
    DEFAULT_MODEL: str = 'anthropic'
    USE_GEMMA: str = True

    # Documents
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    
    CHUNK_SIZE: int = 4000
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
settings = Settings()