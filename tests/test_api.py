import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from typing import List

from src.app.api import app
from src.models import schemas


client = TestClient(app)

SAMPLE_TEXT = "This is a sample text to be summarized"
SAMPLE_SUMMARY = "This is the summary text"
SAMPLE_PATH = "sample_data/hnsw.txt"

@pytest.fixture
def mock_text_processor():
    with patch('src.processors.document.DocumentProcessor.extract_text') as mock:
        mock.return_value = SAMPLE_TEXT
        yield mock

@pytest.fixture
def api_mock_summary_generator():
    with patch('src.services.summary.SummaryGenerator') as MockClass:
        instance = MockClass.return_value

        # Mock the instance methods
        instance.generate_summary.return_value = schemas.SummaryResponse(
            provider = 'anthropic',
            summary = SAMPLE_SUMMARY,
            summary_type = 'brief',
            error = None,
            partial_summary = None
            )
        instance.compare_summaries.return_value = schemas.SummaryCompareResp(
            provider = 'anthropic',
            evaluation_of_summaries = "Compare summaries"
        )
        yield instance


class TestSummarizeEndpoint:
    
    def test_successful_summary_generation(self, mock_text_processor,  api_mock_summary_generator):
        request_data = {
            "file_path": SAMPLE_PATH,
            "summary_type": "brief",
            "providers": ["anthropic"]
        }

        response = client.post("/summarize", json=request_data) 

        assert response.status_code == 200
        assert len(response.json()['summaries']) == 1
        ## TODO: mock properly 
        # assert response.json()['summaries'][0] == SAMPLE_SUMMARY


    def test_multiple_providers(self, mock_text_processor, api_mock_summary_generator):
        request_data = {
            "file_path": SAMPLE_PATH,
            "summary_type": "brief",
            "providers": ["anthropic","gemma"]
            
        }
        response = client.post("/summarize", json=request_data)

        assert response.status_code == 200
        assert len(response.json()['summaries']) == 2
        