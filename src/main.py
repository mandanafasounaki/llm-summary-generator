from .processors.document import DocumentProcessor
from .services import ModelManager, SummaryGenerator
from .config.settings import settings
import logging
from huggingface_hub import login, hf_api


logger = logging.getLogger(__name__)

def main():
    model_manager = ModelManager()
    doc_processor = DocumentProcessor()

    pdf_text = doc_processor.extract_text('sample_data/CV.pdf')
    # logger.info(f"Example PDF output: {pdf_text[:900]}")

    # txt_text = doc_processor.extract_text('sample_data/hnsw.txt')
    # logger.info(f"Example txt output: {txt_text}")

    # docx_text = doc_processor.extract_text('sample_data/file-sample_100kB.docx')
    # logger.info(f"Example docx output: {docx_text}")

    # logger.info(f"LLAMA: {model_manager.get_completion('llama', 'tell me a joke')}")
    # logger.info(f"CLAUDE: {model_manager.get_completion('anthropic', 'tell me a brief joke')}")
    summary_generator = SummaryGenerator(model_manager)
    summary = summary_generator.generate_summary(pdf_text, provider='anthropic')
    logger.info(summary)


if __name__ == "__main__":
    main()