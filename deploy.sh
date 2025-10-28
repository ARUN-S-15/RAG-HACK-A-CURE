#!/bin/bash

echo "================================================"
echo "🚀 Quick Deploy to Render - MedInSight RAG API"
echo "================================================"
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the RAG-HACK-A-CURE directory"
    exit 1
fi

echo "📋 Pre-deployment checklist:"
echo ""

# Check if vectorstore exists
if [ -d "vectorstore" ]; then
    echo "✅ Vector store found"
else
    echo "⚠️  Vector store not found - will be built during deployment"
fi

# Check if .env exists
if [ -f ".env" ]; then
    echo "✅ .env file found"
    if grep -q "your_openai_api_key_here" .env; then
        echo "⚠️  OpenAI API key not set - will use fallback model"
    else
        echo "✅ OpenAI API key configured"
    fi
else
    echo "⚠️  .env file not found"
fi

echo ""
echo "📦 Preparing for deployment..."
echo ""

# Add all files
echo "Adding files to git..."
git add .

# Show status
echo ""
echo "Git status:"
git status --short

echo ""
read -p "Do you want to commit and push? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Commit
    read -p "Enter commit message (or press Enter for default): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Deploy MedInSight RAG API to Render"
    fi
    
    git commit -m "$commit_msg"
    
    # Push
    echo ""
    echo "Pushing to GitHub..."
    git push origin main
    
    echo ""
    echo "================================================"
    echo "✅ Code pushed to GitHub!"
    echo "================================================"
    echo ""
    echo "Next steps:"
    echo "1. Go to https://dashboard.render.com/"
    echo "2. Click 'New +' → 'Web Service'"
    echo "3. Connect your GitHub repository"
    echo "4. Use these settings:"
    echo "   - Name: medinsight-rag-api"
    echo "   - Build Command: pip install -r requirements.txt && python ingest.py"
    echo "   - Start Command: python app.py"
    echo "   - Add Environment Variable: PORT=10000"
    echo "5. Click 'Create Web Service'"
    echo ""
    echo "Your API will be available at:"
    echo "https://medinsight-rag-api.onrender.com/docs"
    echo ""
    echo "📖 Full deployment guide: See DEPLOYMENT.md"
    echo ""
else
    echo ""
    echo "Deployment cancelled. Run this script again when ready."
fi
