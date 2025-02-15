import os
from typing import List, Dict
import logging
from ..config.settings import settings
from langchain.chat_models import ChatOpenAI, ChatAnthropic


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
            self.models['openai'] = ChatOpenAI()

        if os.getenv('ANTHROPIC_KEY'):
            self.models['anthropic'] = ChatAnthropic()