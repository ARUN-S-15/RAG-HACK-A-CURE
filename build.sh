#!/bin/bash

echo "🚀 Building RAG System..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Build vector store
echo "🔨 Building vector store from PDFs..."
python ingest.py

echo "✅ Build complete!"
