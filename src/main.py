from .processors.document import DocumentProcessor
from .services import ModelManager, SummaryGenerator
from .config.settings import settings
from .models.schemas import SummaryRequest, SummaryCompareReq
import logging


logger = logging.getLogger(__name__)

def main():
    model_manager = ModelManager()
    doc_processor = DocumentProcessor()

    pdf_text = doc_processor.extract_text('sample_data/CV.pdf')
    
    summary_generator = SummaryGenerator(model_manager)
    gemma_summary_req = SummaryRequest(text=pdf_text, provider='gemma')
    gemma_summary = summary_generator.generate_summary(gemma_summary_req)
    logger.info(gemma_summary)

    claude_summary_req = SummaryRequest(text=pdf_text, provider='anthropic')
    claude_summary = summary_generator.generate_summary(claude_summary_req)
    logger.info(claude_summary)
    
    compare_req = SummaryCompareReq(text=pdf_text, summaries=[claude_summary, gemma_summary]) 
    evaluation = summary_generator.compare_summaries(compare_req)
    logger.info(evaluation)


if __name__ == "__main__":
    main()