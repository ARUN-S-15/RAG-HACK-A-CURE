#!/bin/bash

echo "================================================"
echo "🔍 MedInSight API Status Checker"
echo "================================================"
echo ""

# Check local server
echo "Checking local server (http://localhost:8000)..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Local server is RUNNING"
    echo "   → Docs: http://localhost:8000/docs"
    echo "   → Health: http://localhost:8000/health"
else
    echo "❌ Local server is NOT running"
    echo "   To start: cd /Users/hariprasathc/Hackathon/RAG-HACK-A-CURE && python app.py"
fi

echo ""
echo "------------------------------------------------"
echo ""

# Check Render deployment
echo "Checking Render deployment..."
RENDER_URL="https://medinsight-rag-api.onrender.com"

if curl -s --max-time 5 $RENDER_URL/health > /dev/null 2>&1; then
    echo "✅ Render deployment is LIVE"
    echo "   → Docs: $RENDER_URL/docs"
    echo "   → Health: $RENDER_URL/health"
else
    echo "❌ Render deployment NOT found"
    echo ""
    echo "To deploy to Render:"
    echo "1. Run: ./deploy.sh"
    echo "   OR"
    echo "2. Follow steps in DEPLOYMENT.md"
    echo ""
    echo "After deploying, your API will be at:"
    echo "https://your-service-name.onrender.com/docs"
fi

echo ""
echo "================================================"
