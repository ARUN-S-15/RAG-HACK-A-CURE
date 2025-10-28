# ⚠️ API Quota Exceeded - Quick Fix Guide

## Problem
Your OpenAI API key has exceeded its quota (no credits remaining).

## Solutions

### **Option 1: Add Credits to OpenAI** (Recommended for Submission)

1. Go to https://platform.openai.com/account/billing
2. Add payment method
3. Add at least $5 in credits
4. Wait 5-10 minutes for credits to appear
5. Run ingestion again:
   ```bash
   python ingest_simple.py
   ```

### **Option 2: Use Mock Data** (Quick Demo)

For immediate testing without API credits:

```bash
# Run mock ingestion (no OpenAI API needed)
python ingest_mock.py

# Start server on different port
PORT=8000 python app.py
```

Then open: http://localhost:8000/query

**⚠️ Limitations:**
- Uses fake embeddings (hash-based)
- Retrieval quality is limited
- No actual LLM generation
- Good for UI testing only

### **Option 3: Get New Free Trial**

1. Create new OpenAI account with different email
2. Get new API key (comes with $5 free credits)
3. Replace API key:
   ```bash
   export OPENAI_API_KEY="sk-new-key-here"
   python ingest_simple.py
   python app.py
   ```

## Current Status

✅ **Chat UI** - Working (no API needed)  
✅ **FastAPI Server** - Working  
❌ **Embeddings** - Needs API credits  
❌ **LLM Generation** - Needs API credits

## For Hack-A-Cure Submission

**You MUST have a working OpenAI API key with credits.**

The mock version is only for local testing/demonstration of the UI.

### Quick Check

```bash
# Test if API key has credits
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# If it returns models list → API key is valid
# If it returns 429 error → No credits
```

## Next Steps

1. **Immediate**: 
   ```bash
   python ingest_mock.py  # Use mock data
   PORT=8000 python app.py
   ```
   Open http://localhost:8000/query to see the UI

2. **For submission**: 
   - Add credits to OpenAI
   - Run `python ingest_simple.py`
   - Deploy to Render with valid API key

## Files Created for Mock Demo

- `ingest_mock.py` - Creates vectorstore with mock embeddings
- `rag_pipeline_mock.py` - RAG without OpenAI API calls

These are temporary solutions for testing the UI only.
