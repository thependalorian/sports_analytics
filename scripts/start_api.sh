#!/bin/bash
# Start FastAPI Server
# Usage: ./scripts/start_api.sh

cd "$(dirname "$0")/.."
source sva/bin/activate

echo "🚀 Starting FastAPI server..."
echo "📍 API will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

