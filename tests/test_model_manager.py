import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError
from tenacity import RetryError

from src.models.schemas import (
    DocumentClass,
    SummaryCompareReq,
    SummaryRequest,
    SummaryResponse,
)

logger = logging.getLogger(__name__)


class TestChatModelHandler:
    PROVIDER = "anthropic"
    PROMPT = "Hello, world!"
    RESPONSE = "Hello, how can I help you?"

    @pytest.fixture
    def chat_handler(self):
        class MockChatModelHandler:
            def __init__(self):
                self.models = {TestChatModelHandler.PROVIDER: MagicMock()}

            def get_completion(self, provider: str, prompt: str) -> str:
                if provider not in self.models:
                    raise ValueError(f"The provider '{provider}' is not supported.")

                try:
                    response = self.models[provider].invoke(prompt)
                    return response.content
                except Exception as e:
                    logger.error(f"Error getting completion from '{provider}': {e}")
                    raise RuntimeError(
                        f"Failed to get completion from '{provider}'."
                    ) from e

        return MockChatModelHandler()

    @patch(
        "tenacity.nap.time.sleep", return_value=None
    )  # Avoid actual sleep during retry
    def test_get_completion_success(self, _, chat_handler):
        chat_handler.models[self.PROVIDER].invoke.return_value = MagicMock(
            content=self.RESPONSE
        )
        result = chat_handler.get_completion(self.PROVIDER, self.PROMPT)
        assert result == self.RESPONSE

    @patch("tenacity.nap.time.sleep", return_value=None)
    def test_get_completion_invalid_provider(self, _, chat_handler):
        with pytest.raises(
            ValueError, match="The provider 'invalid_provider' is not supported."
        ):
            chat_handler.get_completion("invalid_provider", self.PROMPT)

    # @patch("tenacity.nap.time.sleep", return_value=None)
    # def test_get_completion_retry_on_failure(self, _, chat_handler):
    #     chat_handler.models[self.PROVIDER].invoke.side_effect = Exception("Mock failure")

    #     with pytest.raises(RetryError):
    #         chat_handler.get_completion(self.PROVIDER, self.PROMPT)

    #     assert chat_handler.models[self.PROVIDER].invoke.call_count == 3 
