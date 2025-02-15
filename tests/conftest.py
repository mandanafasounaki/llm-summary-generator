import pytest
from pathlib import Path
from src.config.settings import Settings
from src.processors.document import DocumentProcessor
from src.services import ModelManager, SummaryGenerator

@pytest.fixture
def settings():
    return Settings()

@pytest.fixture
def document_processor():
    return DocumentProcessor()

@pytest.fixture
def model_manager():
    return ModelManager()

@pytest.fixture
def summary_generator():
    return SummaryGenerator(model_manager)
