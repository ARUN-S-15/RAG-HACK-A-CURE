#!/bin/bash

echo "=============================================="
echo "MedInSight - Quick Setup Script"
echo "=============================================="
echo ""

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY environment variable is not set!"
    echo ""
    echo "Please set it first:"
    echo "  export OPENAI_API_KEY='sk-your-key-here'"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✓ OPENAI_API_KEY is set"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Check if vectorstore exists
if [ -f "./vectorstore/index.faiss" ] && [ -f "./vectorstore/metadata.pkl" ]; then
    echo "✓ Vectorstore already exists"
    echo ""
    read -p "Do you want to re-ingest? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        RUN_INGEST=true
    else
        RUN_INGEST=false
    fi
else
    echo "📥 Vectorstore not found. Running ingestion..."
    RUN_INGEST=true
fi

if [ "$RUN_INGEST" = true ]; then
    echo ""
    echo "Choose ingestion method:"
    echo "  1) Quick ingest (built-in medical knowledge, ~10 seconds)"
    echo "  2) Dataset PDFs (from ./Dataset folder, may take several minutes)"
    echo ""
    read -p "Enter choice (1 or 2): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^2$ ]]; then
        if [ -d "./Dataset" ] && [ "$(ls -A ./Dataset/*.pdf 2>/dev/null)" ]; then
            echo "🔄 Processing Dataset PDFs..."
            python ingest_dataset.py
        else
            echo "⚠️  No PDFs found in ./Dataset folder"
            echo "Falling back to quick ingest..."
            python ingest_simple.py
        fi
    else
        echo "🔄 Running quick ingest..."
        python ingest_simple.py
    fi
    
    if [ $? -ne 0 ]; then
        echo "❌ Ingestion failed"
        exit 1
    fi
fi

echo ""
echo "=============================================="
echo "✅ Setup complete!"
echo "=============================================="
echo ""
echo "🚀 Starting server..."
echo ""
echo "  Chat interface: http://localhost:10000/query"
echo "  API endpoint: http://localhost:10000/api/query"
echo "  Health check: http://localhost:10000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
