from typing import ClassVar, Literal, Optional

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings and configuration
    """

    model_config = ConfigDict(env_file=".env", case_sensitive=True)

    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACEHUB_API_TOKEN: Optional[str] = None
    DEFAULT_MODEL: str = "anthropic"
    USE_GEMMA: bool = True
    OPENAI_MODEL: str = "gpt-4o"
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    GOOGLE_MODEL: str = "google/gemma-2-9b-it"

    # Documents
    MAX_FILE_SIZE: int = 10 * 1024 * 1024

    CHUNK_SIZE: int = 4000
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3


settings = Settings()
