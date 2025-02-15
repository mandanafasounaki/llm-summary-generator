import logging
from .model_manager import ModelManager
from typing import List

logger = logging.getLogger(__name__)


class SummaryGenerator:
    """Generate summaries from text using different LLMs"""

    CHUNK_SIZE = 3000
    DEFAULT_PROMPT = "Provide a brief summary of the following text: "

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
                current_length = len(word) + 1
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks


    def generate_summary(self, text: str, provider: str = "llama"):
        """
        Generate summary from the text.

        Args:
            text: text to be summarized
            provider: LLM provider

        Returns:
            A dictionary containing the provider info and the summary
        """
        chunks = self._chunk_text(text)
        summaries = []
        try:
            for chunk in chunks:
                prompt = f"{self.DEFAULT_PROMPT} \n{chunk}"
                summary = self.model_manager.get_completion(provider=provider, prompt=prompt)
                summaries.append(summary)

            final_summary = "\n\n".join(summaries)

            return {
                "provider": provider,
                "summary": final_summary
            }
        except Exception as e:
            logger.error(f"An error occured in generating summary: {e}")
            return {
                "provider": provider,
                "error": str(e),
                "partial_summary": "\n\n".join(summaries) if summaries else None
            }



