FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY README.md ./

# Environment variables
COPY .env.example .env

# Install dependencies
RUN poetry --no-root install

# To reach the port inside the container
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["poetry", "run", "uvicorn", "src.app.api:app"]