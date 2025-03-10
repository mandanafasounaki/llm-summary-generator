import logging
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile

from src.config.settings import settings
from src.models.schemas import (
    PathSummaryReq,
    SummaryCompareReq,
    SummaryCompareResp,
    SummaryRequest
)
from src.processors.document import DocumentProcessor
from src.services import ModelManager, SummaryGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="Document Summary API",
    description="API for generating and comparing document summaries using different LLMs",
    version="1.0.0",
)


# Initialize services
model_manager = ModelManager()
doc_processor = DocumentProcessor()
summary_generator = SummaryGenerator(model_manager)


@app.post("/summarize", response_model=Dict)
async def generate_summary(file_path: str, summary_type: str = "brief", providers: List[str] = ["anthropic"]):
    """
    Generate a summary from a file path
    """
    try:

        # Extract text from file_path
        text = doc_processor.extract_text(summary_req.file_path)
                                    
        # Generate summary
        summaries = []
        for provider in providers:
            summary_req = SummaryRequest(
                text=text, summary_type=summary_type, provider=provider
            )
            summaries.append(summary_generator.generate_summary(summary_req))
            
        return {"summaries": summaries}

    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare-summaries", response_model=SummaryCompareResp)
async def compare_summaries(file_path: str, summaries: List[SummaryResponse], provider: str = "anthropic"):
    """
    Generate and compare summaries from different providers for
    """

    try:
        # Validate file using DocumentClass
        doc = DocumentClass(file_path=file_path)

        # Extract text from document
        text = doc_processor.extract_text(doc)

        # Generate summaries from all requested providers
        summaries = []
        
        compare_req = SummaryCompareReq(text=text, summaries=summaries, provider=provider)
        evaluation = summary_generator.compare_summaries(compare_req)

        return evaluation

    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
