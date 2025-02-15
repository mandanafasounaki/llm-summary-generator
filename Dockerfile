FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src/ ./src/
COPY README.md ./

# Configure poetry
RUN poetry config virtualenvs.create false

COPY .env.example .env
RUN poetry --no-root install

# # Set environment variables
# ENV PYTHONPATH=/app
# ENV PYTHONUNBUFFERED=1

# Create volume for input/output files
# VOLUME /app/data
EXPOSE 8000
# Set entrypoint
ENTRYPOINT ["poetry", "run", "uvicorn", "src.app.api:app"]