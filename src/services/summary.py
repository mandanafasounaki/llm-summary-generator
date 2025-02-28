import logging
from typing import Dict, List

from ..config.settings import settings
from ..models.schemas import (
    SummaryCompareReq,
    SummaryCompareResp,
    SummaryRequest,
    SummaryResponse,
)
from .model_manager import ModelManager

logger = logging.getLogger(__name__)


class SummaryGenerator:
    """Generate summaries from text using different LLMs"""

    CHUNK_SIZE = settings.CHUNK_SIZE
    SUMMARY_TYPES = {
        "brief": "Provide a brief 2-3 sentence summary of the following text:",
        "detailed": "Provide a detailed summary of the following text, including main points and key details:",
        "bullets": "Summarize the following text in bullet points, highlighting key information:",
    }
    COMPARE_PROMPT = """
    You are an editor that examines the provided summaries of a text and compares and evaluates the provided summaries.

    These are the summaries: {summaries}
    """

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager

    def _chunk_text(self, text: str) -> list[str]:
        """
        Split text into smaller chunks.
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            if len(word) + current_length > self.CHUNK_SIZE:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def generate_summary(self, summary_request: SummaryRequest) -> SummaryResponse:
        """
        Generate summary from the text.

        Args:
            text: text to be summarized
            provider: LLM provider

        Returns:
            A dictionary containing the provider info and the summary
        """
        text = summary_request.text
        provider = summary_request.provider
        summary_type = summary_request.summary_type
        summaries = []

        try:
            if len(text) < 10000:
                prompt = f"{self.SUMMARY_TYPES.get(summary_type)}\n{text}"
                final_summary = self.model_manager.get_completion(
                    provider=provider, prompt=prompt
                )
            else:
                chunks = self._chunk_text(text)

                for chunk in chunks:
                    prompt = f"{self.SUMMARY_TYPES.get(summary_type)}\n{chunk}"
                    summary = self.model_manager.get_completion(
                        provider=provider, prompt=prompt
                    )
                    summaries.append(summary)

                final_summary = "\n\n".join(summaries)

            return SummaryResponse(
                provider=provider, summary=final_summary, summary_type=summary_type
            )

        except Exception as e:
            logger.error(f"An error occured in generating summary: {e}")
            return SummaryResponse(
                provider=provider,
                summary_type=summary_type,
                error=str(e),
                partial_summary="\n\n".join(summaries) if summaries else None,
            )

    def compare_summaries(self, compare_req: SummaryCompareReq) -> SummaryCompareResp:
        """
        Receives a list of summaries, compares and evaluates them.

        Args:
            text: raw text that was summarized
            summaries: the list of generated summaries to be compared
        Returns:
            A dictionary containig provider info and the evaluation of summaries
        """
        try:
            text = compare_req.text
            summaries = compare_req.summaries
            provider = compare_req.provider
            

            prompt = self.COMPARE_PROMPT.format(text=text, summaries=summaries)
            
            evaluation = self.model_manager.get_completion(provider, prompt)
            return SummaryCompareResp(
                provider=provider, evaluation_of_summaries=evaluation
            )
        except Exception as e:
            logger.error(f"An error occured during comparison: {e}")
            raise
