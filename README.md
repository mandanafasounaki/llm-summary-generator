# Document Analyzer

A robust document analysis system that leverages multiple LLM providers (OpenAI, Anthropic, and Gemma) through LangChain to process and analyze documents in various formats.

## Features

- **Multi-format Document Processing**: Support for PDF, DOCX, and TXT files
- **Multiple LLM Provider Integration**: OpenAI, Anthropic, and Gemma support through LangChain
- **Intelligent Summary Generation**: Multiple summary types with automatic text chunking
- **Compare Different Summaries**: Comparing and evaluating different summaries generated by LLMs 
- **Robust Error Handling**: Comprehensive error handling and logging
- **Type Safety**: Full static type checking with mypy
- **Data Validation**: Input/output validation using Pydantic
- **Configurable**: Environment-based configuration management

## Requirements

- Python 3.11 or 3.12
- Poetry package manager
- OpenAI API key
- Anthropic API key
- Hugging Face access token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mandanafasounaki/aracor-ai-assignment-mandanafasounaki
cd aracor-ai-assignment-mandanafasounaki
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` with your API keys and configuration:
```env
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
DEFAULT_MODEL_PROVIDER=anthropic
```

## Usage

### Basic Usage

```python
from src.processors.document import DocumentProcessor
from src.services import ModelManager, SummaryGenerator
from src.config.settings import settings
from src.models.schemas import SummaryRequest, SummaryCompareReq
import logging

logger = logging.getLogger(__name__)

def main():
    model_manager = ModelManager()
    doc_processor = DocumentProcessor()

    text = doc_processor.extract_text('sample_data/hnsw.txt')

    summary_generator = SummaryGenerator(model_manager)
    gemma_summary_req = SummaryRequest(text=text, provider='gemma', summary_type='bullets')
    gemma_summary = summary_generator.generate_summary(gemma_summary_req)
    logger.info(gemma_summary)

    claude_summary_req = SummaryRequest(text=text, provider='anthropic', summary_type='bullets')
    claude_summary = summary_generator.generate_summary(claude_summary_req)
    logger.info(claude_summary)
    
    compare_req = SummaryCompareReq(text=text, summaries=[claude_summary, gemma_summary]) 
    evaluation = summary_generator.compare_summaries(compare_req)
    logger.info(evaluation)


if __name__ == "__main__":
    main()
```

### Summary Types

The system supports three types of summaries:
- `brief`: 2-3 sentence overview
- `detailed`: Comprehensive summary with main points
- `bullets`: Key points in bullet format


### Configuration Options

Key configuration options in `.env`:
```env
MAX_RETRIES=3              # Maximum retry attempts for API calls
REQUEST_TIMEOUT=30         # API request timeout in seconds
CHUNK_SIZE=4000           # Text chunk size for processing
```

### Running Tests

Run tests with coverage:
```bash
poetry run pytest -cov
```

### Docker
To run the API with Docker:
1.
```bash
sudo docker build -t aracor-api . 
```
2.
```bash
sudo docker run --network host  -p 8000:8000 --env-file=.env --mount src="$(pwd)/sample_data",target=/sample_data,type=bind   aracor-api
```
### Requests
**1. Summary Generation**
```bash
curl -X POST "http://127.0.0.1:8000/summarize" -H "Content-Type: application/json" -d '{"file_path": "/sample_data/CV.pdf", "summary_type": "bullets", "providers": ["anthropic", "gemma"]}'
```
**2.Compare Summaries**
 ```bash
 curl -X POST "http://localhost:8000/compare-summaries" \
     -H "Content-Type: application/json" \
     -d '{       "summaries": [
         {
           "provider": "anthropic",
           "summary": "This is a summary from anthropic",
           "summary_type": "brief",
           "error": null,
           "partial_summary": null
         },
         {
           "provider": "openai",
           "summary": "This is a summary from openai",
           "summary_type": "brief",
           "error": null,
           "partial_summary": null
         }
       ],
       "provider": "anthropic"
     }'

 ```
