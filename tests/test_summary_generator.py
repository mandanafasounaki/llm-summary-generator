import pytest
from unittest.mock import Mock
from src.services.summary import SummaryGenerator
from src.models.schemas import SummaryRequest, SummaryResponse, SummaryCompareReq, SummaryCompareResp


@pytest.fixture
def model_manager():
    return Mock()

@pytest.fixture
def summary_generator(model_manager):
    return SummaryGenerator(model_manager)

class TestSummaryGenerator:
    TEXT = """AI-powered agents are an emerging field with no established theoretical frameworks fordefining, developing, 
        and evaluating them. This section is a best-effort attempt to build aframework from the existing literature, but it will evolve as the field does. 
        Compared to therest of the book, this section is more experimental. I received helpful feedback from earlyreviewers, and I hope to get feedback from readers of 
        this blog post, too.
        2. before this book came out, Anthropic published a blog post on Building effective agents(Dec 2024). 
        I’m glad to see that Anthropic’s blog post and my agent section are conceptually aligned, 
        though with slightly different terminologies. However, Anthropic’spost focuses on isolated patterns,
        whereas my post covers why and how things work. I alsofocus more on planning, tool selection, and failure modes.
        3.The post contains a lot of background information. Feel free to skip ahead if it feels a littletoo in the weeds!
        """
    
    def test_brief_summary_generation(self, summary_generator, model_manager):
        # Arrange
        model_manager.get_completion.return_value = "This is a brief summary."
        request = SummaryRequest(
            text="This is a sample text that needs to be summarized.",
            summary_type="brief",
            provider="anthropic"
        )

        # Act
        response = summary_generator.generate_summary(request)

        # Assert
        assert response.summary == "This is a brief summary."
        assert response.provider == "anthropic"
        assert response.summary_type == "brief"
        model_manager.get_completion.assert_called_once()

    def test_detailed_summary_generation(self, summary_generator, model_manager):
        # Arrange
        model_manager.get_completion.return_value = "This is a detailed summary with multiple points."
        request = SummaryRequest(
            text="This is a longer sample text that needs more detailed summarization.",
            summary_type="detailed",
            provider="anthropic"
        )

        # Act
        response = summary_generator.generate_summary(request)

        # Assert
        assert response.summary == "This is a detailed summary with multiple points."
        assert response.summary_type == "detailed"

    def test_bullet_summary_generation(self, summary_generator, model_manager):
        # Arrange
        model_manager.get_completion.return_value = "• Point 1\n• Point 2"
        request = SummaryRequest(
            text="Content that should be summarized in bullets.",
            summary_type="bullets",
            provider="anthropic"
        )

        # Act
        response = summary_generator.generate_summary(request)

        # Assert
        assert "•" in response.summary
        assert response.summary_type == "bullets"

    def test_long_text_handling(self, summary_generator, model_manager):
        # Arrange
        long_text = "word " * 5000  # Creates text longer than CHUNK_SIZE
        model_manager.get_completion.return_value = "Chunk summary"
        request = SummaryRequest(
            text=long_text,
            summary_type="brief",
            provider="anthropic"
        )

        # Act
        response = summary_generator.generate_summary(request)

        # Assert
        assert response.summary is not None
        assert model_manager.get_completion.call_count > 1  # Should be called multiple times for chunks

    def test_short_text_handling(self, summary_generator, model_manager):
        # Arrange
        model_manager.get_completion.return_value = "Very short summary"
        request = SummaryRequest(
            text="Hello world",
            summary_type="brief",
            provider="anthropic"
        )

        # Act
        response = summary_generator.generate_summary(request)

        # Assert
        assert response.summary == "Very short summary"
        model_manager.get_completion.assert_called_once()

    def test_special_characters_handling(self, summary_generator, model_manager):
        # Arrange
        special_text = "Special chars: !@#$%^&*()_+ àéîøū 漢字"
        model_manager.get_completion.return_value = "Summary with special chars"
        request = SummaryRequest(
            text=special_text,
            summary_type="brief",
            provider="anthropic"
        )

        # Act
        response = summary_generator.generate_summary(request)

        # Assert
        assert response.summary is not None
        assert response.error is None

    def test_error_handling(self, summary_generator, model_manager):
        # Arrange
        model_manager.get_completion.side_effect = Exception("An error occured in generating summary")
        request = SummaryRequest(
            text="Sample text",
            summary_type="brief",
            provider="anthropic"
        )

        # Act
        response = summary_generator.generate_summary(request)

        # Assert
        assert response.error is not None
        assert "error occured" in response.error
        assert response.summary is None

    def test_summary_comparison(self, summary_generator, model_manager):
        # Arrange
        model_manager.get_completion.return_value = "Comparison of summaries"
        summaries = [
            SummaryResponse(provider="anthropic", summary="Summary 1", summary_type="brief"),
            SummaryResponse(provider="gemma", summary="Summary 2", summary_type="brief")
        ]
        compare_req = SummaryCompareReq(
            text="Original text",
            summaries=summaries,
            provider="anthropic"
        )

        # Act
        response = summary_generator.compare_summaries(compare_req)

        # Assert
        assert isinstance(response, SummaryCompareResp)
        assert response.evaluation_of_summaries == "Comparison of summaries"
        assert response.provider == "anthropic"