from .processors.document import DocumentProcessor
from .services.model_manager import ModelManager
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def main():
    model_manager = ModelManager()
    doc_processor = DocumentProcessor()

    pdf_text = doc_processor.extract_text('Agents_chuyan.pdf')
    logger.info(f"Example PDF output: {pdf_text[:900]}")

    txt_text = doc_processor.extract_text('hnsw.txt')
    logger.info(f"Example txt output: {txt_text}")

    docx_text = doc_processor.extract_text('file-sample_100kB.docx')
    logger.info(f"Example docx output: {docx_text}")

    

if __name__ == "__main__":
    main()