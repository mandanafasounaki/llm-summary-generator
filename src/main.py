import logging

from .config.settings import settings
from .models.schemas import SummaryCompareReq, SummaryRequest
from .processors.document import DocumentProcessor
from .services import ModelManager, SummaryGenerator

logger = logging.getLogger(__name__)


def main():
    model_manager = ModelManager()
    doc_processor = DocumentProcessor()

    # text = doc_processor.extract_text('sample_data/CV.pdf')
    text = doc_processor.extract_text("sample_data/hnsw.txt")

    summary_generator = SummaryGenerator(model_manager)
    gemma_summary_req = SummaryRequest(
        text=text, provider="gemma", summary_type="bullets"
    )
    gemma_summary = summary_generator.generate_summary(gemma_summary_req)
    logger.info(gemma_summary)

    claude_summary_req = SummaryRequest(
        text=text, provider="anthropic", summary_type="bullets"
    )
    claude_summary = summary_generator.generate_summary(claude_summary_req)
    logger.info(claude_summary)

    compare_req = SummaryCompareReq(
        text=text, summaries=[claude_summary, gemma_summary]
    )
    evaluation = summary_generator.compare_summaries(compare_req)
    logger.info(evaluation)


if __name__ == "__main__":
    main()
