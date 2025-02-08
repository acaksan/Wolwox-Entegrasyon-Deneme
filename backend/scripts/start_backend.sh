#!/bin/bash
echo "Starting backend services..."

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the FastAPI application with uvicorn
cd "$(dirname "$0")/.."
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python src/main.py

# Deactivate virtual environment on exit
deactivate 