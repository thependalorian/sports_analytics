#!/bin/bash
# Start Streamlit App
# Usage: ./scripts/start_streamlit.sh

cd "$(dirname "$0")/.."
source sva/bin/activate

echo "🚀 Starting Streamlit app..."
echo "📍 App will be available at: http://localhost:8501"
echo ""

streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

