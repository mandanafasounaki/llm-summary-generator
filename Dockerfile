FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY README.md ./

# Configure poetry
RUN poetry config virtualenvs.create false

COPY .env.example .env
RUN poetry --no-root install
RUN poetry run pytest -cov


# Create volume for input/output files
VOLUME /sample_data

EXPOSE 8000
# Set entrypoint
ENTRYPOINT ["poetry", "run", "uvicorn", "src.app.api:app"]