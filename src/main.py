from .processors.document import DocumentProcessor
from .services.model_manager import ModelManager
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def main():
    model_manager = ModelManager()
    doc_processor = DocumentProcessor()

    # pdf_text = doc_processor.extract_text('sample_data/Agents_chuyan.pdf')
    # logger.info(f"Example PDF output: {pdf_text[:900]}")

    # txt_text = doc_processor.extract_text('sample_data/hnsw.txt')
    # logger.info(f"Example txt output: {txt_text}")

    # docx_text = doc_processor.extract_text('sample_data/file-sample_100kB.docx')
    # logger.info(f"Example docx output: {docx_text}")

    logger.info(model_manager.models)
    

if __name__ == "__main__":
    main()