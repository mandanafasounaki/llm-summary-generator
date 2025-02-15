import logging
import shutil
import tempfile
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile

from src.processors.document import DocumentProcessor

from ..config.settings import settings
from ..models.schemas import (
    DocumentClass,
    SummaryCompareReq,
    SummaryCompareResp,
    SummaryRequest,
    SummaryResponse,
)
from ..services import ModelManager, SummaryGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_TYPES = {
    "text/plain",  # .txt
    "application/pdf",  # .pdf
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
}

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


@app.post("/summarize", response_model=SummaryResponse)
async def generate_summary(
    file: UploadFile = File(...),
    summary_type: str = "brief",
    provider: str = "anthropic",
):
    """
    Generate a summary from an uploaded document file (txt, pdf, or docx).
    """
    try:
        logger.info(file.content_type)
        # Validate file format
        # if file.content_type not in ALLOWED_TYPES:
        #     raise HTTPException(
        #         status_code=400,
        #         detail=f"Unsupported format: {file.content_type}. Allowed formats: .txt, .docx, .pdf"
        #     )
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = Path(temp_file.name)
        logger.info(temp_path)
        try:
            # Validate file using DocumentClass
            doc = DocumentClass(file_path=temp_path)

            # Extract text from document
            text = doc_processor.extract_text(str(doc.file_path))

            # Generate summary
            summary_req = SummaryRequest(
                text=text, summary_type=summary_type, provider=provider
            )
            summary = summary_generator.generate_summary(summary_req)

            return summary

        finally:
            # Clean up temporary file
            temp_path.unlink()

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare-summaries", response_model=SummaryCompareResp)
async def compare_summaries(
    file: UploadFile = File(...),
    providers: List[str] = ["anthropic", "gemma"],
    summary_type: str = "brief",
):
    """
    Generate and compare summaries from different providers for an uploaded document.
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = Path(temp_file.name)

        try:
            # Validate file using DocumentClass
            doc = DocumentClass(file_path=temp_path)

            # Extract text from document
            text = doc_processor.extract_text(str(doc.file_path))

            # Generate summaries from all requested providers
            summaries = []
            for provider in providers:
                summary_req = SummaryRequest(
                    text=text, provider=provider, summary_type=summary_type
                )
                summary = summary_generator.generate_summary(summary_req)
                summaries.append(summary)

            # Compare the generated summaries
            compare_req = SummaryCompareReq(
                text=text,
                summaries=summaries,
                provider="anthropic",  # Using anthropic as default comparison provider
            )
            evaluation = summary_generator.compare_summaries(compare_req)

            return evaluation

        finally:
            # Clean up temporary file
            temp_path.unlink()

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
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
