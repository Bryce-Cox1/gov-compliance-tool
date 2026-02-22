#!/bin/bash
# Start script for deployment

# Download spaCy model if not present
python -m spacy download en_core_web_sm 2>/dev/null || true

# Start the FastAPI server
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
