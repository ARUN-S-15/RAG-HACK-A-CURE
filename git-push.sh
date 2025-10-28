#!/bin/bash

# MedInSight - Git Setup and Push to Update Render
# This script initializes git (if needed) and pushes to your repository

echo "================================================"
echo "MedInSight - Git Repository Setup & Push"
echo "================================================"
echo ""

# Navigate to project directory
cd /Users/hariprasathc/Hackathon/Hari-version

# Check if git is already initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✓ Git initialized"
    echo ""
else
    echo "✓ Git repository already exists"
    echo ""
fi

# Show what will be committed
echo "📋 Files to be committed:"
echo "----------------------------------------"
git status -s 2>/dev/null || ls -la | grep -v "^d" | awk '{print $9}'
echo "----------------------------------------"
echo ""

# Prompt for remote URL
echo "🔗 Git Remote Setup"
echo ""
echo "Do you have an existing GitHub repository URL?"
echo "Example: https://github.com/yourusername/your-repo.git"
echo ""
read -p "Enter your GitHub repository URL (or press Enter to skip): " REPO_URL

if [ -n "$REPO_URL" ]; then
    # Check if remote exists
    if git remote | grep -q "origin"; then
        echo "Remote 'origin' already exists. Updating..."
        git remote set-url origin "$REPO_URL"
    else
        echo "Adding remote 'origin'..."
        git remote add origin "$REPO_URL"
    fi
    echo "✓ Remote configured: $REPO_URL"
    echo ""
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Vectorstore (will be regenerated on deploy)
vectorstore/

# Logs
*.log
EOF
    echo "✓ .gitignore created"
    echo ""
fi

# Stage all files
echo "📦 Staging files..."
git add .
echo "✓ Files staged"
echo ""

# Show status
echo "📊 Current status:"
git status
echo ""

# Prompt for commit message
echo "💬 Commit Message"
read -p "Enter commit message (or press Enter for default): " COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Add chat interface and enhanced RAG features

- Add beautiful chat UI at /query route
- Add Dataset PDF processing (ingest_dataset.py)
- Add demo mode for testing without API credits
- Update API routes (GET /query, POST /api/query)
- Add comprehensive documentation (6 guides)
- Improve error handling and fail-safe responses
- Add mobile-responsive design
- Add source citation display"
fi

# Commit
echo ""
echo "💾 Creating commit..."
git commit -m "$COMMIT_MSG"
echo "✓ Commit created"
echo ""

# Check if we have a remote
if git remote | grep -q "origin"; then
    echo "🚀 Ready to push!"
    echo ""
    read -p "Push to remote repository now? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Get current branch name
        BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
        
        echo "📤 Pushing to origin/$BRANCH..."
        git push -u origin $BRANCH
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "================================================"
            echo "✅ SUCCESS! Code pushed to repository!"
            echo "================================================"
            echo ""
            echo "Next steps:"
            echo "1. Go to Render dashboard: https://dashboard.render.com"
            echo "2. Your service will auto-deploy (if enabled)"
            echo "   OR click 'Manual Deploy' → 'Deploy latest commit'"
            echo "3. Monitor build in Logs tab"
            echo "4. Test at: https://your-app.onrender.com/query"
            echo ""
        else
            echo ""
            echo "⚠️  Push failed. This might be because:"
            echo "- Repository doesn't exist yet"
            echo "- Wrong URL"
            echo "- Authentication needed"
            echo ""
            echo "Create the repository on GitHub first, then re-run this script"
        fi
    else
        echo "Skipped push. Run 'git push origin main' when ready."
    fi
else
    echo "⚠️  No remote repository configured."
    echo ""
    echo "To push later:"
    echo "  git remote add origin https://github.com/yourusername/repo.git"
    echo "  git push -u origin main"
fi

echo ""
echo "================================================"
echo "Local repository is ready!"
echo "================================================"
