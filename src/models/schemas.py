import logging
from pathlib import Path
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from ..config.settings import settings

logger = logging.getLogger(__name__)


class DocumentClass(BaseModel):
    """
    Input validation document processing.
    """

    file_path: str

    @field_validator("file_path")
    def validate_file_path(cls, v: str) -> str:
        path = Path(v)
        if not path.exists():
            raise ValueError(f"File not found: {v}")
        if path.stat().st_size > settings.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds limit: {v}")
        return v


class SummaryRequest(BaseModel):
    """
    Input validation for summary generation
    """

    text: str = Field(..., min_length=1)
    summary_type: Literal["brief", "detailed", "bullets"] = "brief"
    provider: Literal["openai", "anthropic", "gemma"] = "anthropic"


class SummaryResponse(BaseModel):
    """
    Summary output format
    """

    provider: str
    summary: Optional[str] = None
    summary_type: str
    error: Optional[str] = None
    partial_summary: Optional[str] = None


class SummaryCompareReq(BaseModel):
    """
    Input for comparing a list of summaries.
    """

    text: Optional[str] = None
    summaries: List[SummaryResponse]
    provider: str = "anthropic"


class SummaryCompareResp(BaseModel):
    """
    Summary compare output format
    """

    provider: str
    evaluation_of_summaries: str
