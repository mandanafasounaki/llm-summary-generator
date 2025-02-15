import logging
from pydantic import Field, BaseModel, validator
from typing import Dict, List, Optional, Literal
from pathlib import Path
from ..config.settings import settings

logger = logging.getLogger(__name__)

class DocumentClass(BaseModel):
    """
    Input validation document processing.
    """
    file_path: Path
    
    @validator("file_path")
    def validate_file_path(cls, v: Path):
        if not v.exists():
            raise ValueError(f"File not found: {v}")
        if v.stat().st_size > settings.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds limit: {v}")
        return v
    

class SummaryRequest(BaseModel):
    """
    Input validation for summary generation
    """
    text: str = Field(..., min_length=1)
    provider: Literal["openai", "anthropic", 'gemma'] = "anthropic"

class SummaryResponse(BaseModel):
    """
    Summary output format
    """
    provider: str
    summary: Optional[str] = None
    error: Optional[str] = None
    partial_summary: Optional[str] = None

class SummaryCompareReq(BaseModel):
    text: str 
    summaries: List[SummaryResponse]
    provider: Optional[str] = 'anthropic'

class SummaryCompareResp(BaseModel):
    """
    Summary compare output format
    """
    provider: str
    evaluation_of_summaries: str




