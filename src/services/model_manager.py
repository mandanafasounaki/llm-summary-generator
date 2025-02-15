import os
from typing import List, Dict
import logging
from ..config.settings import settings
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage


# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        if os.getenv("OPENAI_KEY"):
            self.models['openai'] = ChatOpenAI(
                model='gpt-4o',
                temperatire=0,
                timeout=30,
                max_retries=3
            )

        if os.getenv('ANTHROPIC_KEY'):
            self.models['anthropic'] = ChatAnthropic(
                model='claude-3-5-sonnet-20241022',
                temperature=0,
                timeout=30,
                max_retries=3,
                max_tokens=2048
                )
    
    def get_completion(self, model: str, prompt: str):
        """
        Get chat completion from specified model.
        """
        if model not in self.models:
            raise ValueError(f"The model {model} is not supported.")
        
        try:
            response = self.models[model].invoke(HumanMessage(content=prompt))
            return response.content
        except Exception as e:
            logger.error(f"Error getting completion from {model}: {e}")
            raise