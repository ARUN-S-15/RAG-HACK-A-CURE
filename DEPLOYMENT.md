# MedInSight RAG API - Deployment Guide for Hack-A-Cure

## Quick Deploy (Render.com or similar)

### 1. Environment Variables
Set in your platform's dashboard:
```
OPENAI_API_KEY=sk-your-key-here
```

### 2. Build Command
```bash
pip install -r requirements.txt && python ingest_simple.py
```

### 3. Start Command
```bash
python app.py
```

### 4. Port
The app automatically uses the `PORT` environment variable if set, otherwise defaults to 10000.

## Local Testing

### 1. Set environment variable
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run ingestion
```bash
python ingest_simple.py
```

Expected output:
```
Starting simplified ingest...
Prepared 20 document chunks
Initializing OpenAI client...
Creating embeddings for 20 texts...
✓ Created 20 embeddings
Vector dimension: 1536
Building FAISS index...
Saving index and metadata...
✓ Successfully indexed 20 chunks into ./vectorstore
```

### 4. Start server
```bash
python app.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

### 5. Test the API
In another terminal:
```bash
# Health check
curl http://localhost:10000/health

# Query test
curl -X POST http://localhost:10000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diabetes?", "top_k": 2}'
```

Expected response format:
```json
{
  "answer": "Diabetes is a chronic condition characterized by high blood sugar levels. [1]",
  "contexts": [
    "Diabetes is a chronic condition characterized by high blood sugar levels.",
    "The hallmark of diabetes is elevated glucose levels..."
  ]
}
```

## Troubleshooting

### "OPENAI_API_KEY environment variable is required"
- Make sure you've set the environment variable before running ingest or the app
- For deployment platforms, set it in the environment variables section of the dashboard

### "Module not found" errors
- Run: `pip install -r requirements.txt`

### Vectorstore not found
- Run `python ingest_simple.py` before starting the app
- Make sure it completes successfully and creates `./vectorstore/` directory

### Port already in use
- Change the port: `PORT=8000 python app.py`
- Or kill the process using port 10000: `lsof -ti:10000 | xargs kill -9`

## API Compliance Checklist

✅ POST /query endpoint
✅ Request format: {"query": "string", "top_k": 5}
✅ Response format: {"answer": "string", "contexts": ["string", ...]}
✅ contexts is array of plain strings
✅ Returns 200 OK on success
✅ Fail-safe message: "Information not available in dataset."
✅ GET /health endpoint returns {"status": "ok"}
✅ Answers grounded in retrieved context with citations [1], [2], etc.
✅ Optimized for <60s response time
