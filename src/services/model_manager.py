import logging
import os
# from typing import Dict, List, Optional

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config.settings import settings

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


class ModelManager:
    """
    Model manager to switch between Anthropic and OpenAI models.
    """

    def __init__(self):
        self.models = {}
        self._setup_models()

    def _setup_models(self):
        """
        Initialize models
        """

        if os.getenv("OPENAI_API_KEY"):
            self.models["openai"] = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=0,
                # timeout=30,
                max_retries=settings.MAX_RETRIES,
            )

        if os.getenv("ANTHROPIC_API_KEY"):
            self.models["anthropic"] = ChatAnthropic(
                model=settings.ANTHROPIC_MODEL,
                temperature=0,
                # timeout=30,
                max_retries=settings.MAX_RETRIES,
                max_tokens=2048,
            )

        # Open source models
        hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not hf_token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set")

        if os.getenv("USE_GEMMA") == 'True':
            hf_neo = HuggingFaceEndpoint(
                repo_id=settings.GOOGLE_MODEL,
                task="text-generation",
                huggingfacehub_api_token=hf_token,
            )
            self.models["gemma"] = ChatHuggingFace(llm=hf_neo)

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def get_completion(self, provider: str, prompt: str):
        """
        Get chat completion from specified model.
        """
        if provider not in self.models:
            raise ValueError(f"The provider {provider} is not supported.")

        try:
            response = self.models[provider].invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error getting completion from {provider}: {e}")
            raise
