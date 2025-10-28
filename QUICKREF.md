# 🎯 QUICK REFERENCE - MedInSight RAG with Chat UI

## 📁 Complete File Structure
```
/Users/hariprasathc/Hackathon/Hari-version/
│
├── 🌐 FRONTEND
│   └── static/
│       └── chat.html          ← Beautiful chat interface (NEW!)
│
├── ⚙️ BACKEND
│   ├── app.py                 ← FastAPI server (UPDATED with chat routes)
│   └── rag_pipeline.py        ← RAG implementation
│
├── 📥 INGESTION
│   ├── ingest_simple.py       ← Quick (10 sec, built-in knowledge)
│   ├── ingest_dataset.py      ← Full (5-15 min, Dataset PDFs) (NEW!)
│   └── ingest.py              ← Legacy (for pdfs/ folder)
│
├── 🧪 TESTING
│   └── test_api.py            ← Automated API tests
│
├── 🚀 DEPLOYMENT
│   ├── start.sh               ← One-command startup (NEW!)
│   └── requirements.txt       ← Python dependencies
│
├── 📖 DOCUMENTATION
│   ├── README.md              ← Main docs (UPDATED with chat info)
│   ├── COMPLETE.md            ← This summary (NEW!)
│   ├── RENDER_DEPLOY.md       ← Render deployment guide (NEW!)
│   ├── SUBMISSION_GUIDE.md    ← Hack-A-Cure checklist
│   └── DEPLOYMENT.md          ← General deployment
│
└── 📂 DATA (Generated)
    ├── Dataset/               ← Put your PDFs here
    ├── vectorstore/           ← Generated FAISS index
    │   ├── index.faiss
    │   └── metadata.pkl
    └── .env.example           ← API key template
```

---

## 🎯 Routes & Endpoints

| Route | Method | Purpose | Response |
|-------|--------|---------|----------|
| `/` | GET | Root redirect | Redirects to `/query` |
| `/query` | GET | **Chat Interface** 💬 | HTML page |
| `/api/query` | POST | API endpoint | JSON |
| `/query` | POST | Legacy API (backward compat) | JSON |
| `/health` | GET | Health check | `{"status": "ok"}` |

---

## ⚡ Quick Commands

### Local Development
```bash
# Setup (one command)
export OPENAI_API_KEY="sk-..." && ./start.sh

# Manual setup
export OPENAI_API_KEY="sk-..."
pip install -r requirements.txt
python ingest_simple.py          # or ingest_dataset.py
python app.py

# Open chat
open http://localhost:10000/query
```

### Render Deployment
```bash
# Environment Variables (in Render dashboard)
OPENAI_API_KEY=sk-your-key-here

# Build Command (choose one)
pip install -r requirements.txt && python ingest_simple.py
pip install -r requirements.txt && python ingest_dataset.py

# Start Command
python app.py
```

### Testing
```bash
# Health check
curl http://localhost:10000/health

# API test
curl -X POST http://localhost:10000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diabetes?", "top_k": 3}'

# Automated tests
python test_api.py

# Chat UI
open http://localhost:10000/query
```

---

## 🎨 Chat Interface Features

### Visual Design
- Purple gradient theme
- Clean, modern UI
- Smooth animations
- Mobile-responsive

### Functionality
- Real-time Q&A
- Source citation display
- Sample question buttons
- Loading indicators
- Error handling
- Message history
- Auto-scroll

### User Flow
1. User visits `/query`
2. Sees welcome screen with sample questions
3. Types or clicks a question
4. Clicks "Send"
5. Sees loading spinner
6. Gets answer with source citations
7. Can ask more questions

---

## 📊 Ingestion Options Comparison

| Feature | ingest_simple.py | ingest_dataset.py |
|---------|------------------|-------------------|
| **Speed** | ~10 seconds | 5-15 minutes |
| **Source** | Built-in knowledge | Dataset PDFs |
| **Chunks** | 20 predefined | 100s-1000s extracted |
| **Memory** | Very low | Medium |
| **Best For** | Quick demo, testing | Production, full data |
| **Deploy Time** | Fast | Slower |

---

## 🔧 Configuration Quick Reference

### Embedding Model
**File**: `rag_pipeline.py`, `ingest_*.py`  
**Current**: `text-embedding-3-small` (1536 dim)  
**Alternative**: `text-embedding-3-large` (3072 dim)

### LLM Model
**File**: `rag_pipeline.py`  
**Current**: `gpt-4o`  
**Note**: GPT-5 not yet available

### Chunking (ingest_dataset.py)
```python
CHUNK_SIZE = 800           # Characters per chunk
CHUNK_OVERLAP = 200        # Overlap
MAX_CHUNKS_PER_PDF = 500   # Limit per PDF
BATCH_SIZE = 20            # Embeddings batch
```

### Port
**File**: `app.py`  
**Default**: 10000  
**Override**: Set `PORT` environment variable

---

## ✅ Pre-Deployment Checklist

### Code Ready
- [x] Chat UI created (`static/chat.html`)
- [x] FastAPI routes updated (`app.py`)
- [x] Dataset ingestion script (`ingest_dataset.py`)
- [x] Documentation complete

### Before Deploy
- [ ] Set `OPENAI_API_KEY` in Render
- [ ] Choose ingestion method (simple or dataset)
- [ ] Set correct build command
- [ ] Set start command: `python app.py`

### After Deploy
- [ ] Check health endpoint works
- [ ] Open chat UI at `/query`
- [ ] Test with sample question
- [ ] Verify source citations appear
- [ ] Test API with curl

---

## 🎯 Hack-A-Cure Submission

### What to Submit
**URL**: `https://your-app.onrender.com`

### What Judges Will See
1. **Chat Interface** at `/query`
   - Professional UI
   - Real-time responses
   - Source citations

2. **API Compliance** at `/api/query`
   - Exact JSON format
   - Fail-safe responses
   - Grounded answers

3. **Documentation**
   - Complete README
   - Deployment guides
   - API examples

### Scoring Advantages
- ✅ Exceeds requirements (chat UI bonus!)
- ✅ Professional presentation
- ✅ Complete documentation
- ✅ Production-ready code
- ✅ Mobile-friendly
- ✅ Anti-hallucination safeguards

---

## 🐛 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Chat UI blank | Check `static/chat.html` exists |
| API 500 error | Run ingestion, check API key |
| "Vectorstore not found" | Run `ingest_simple.py` |
| Memory error | Reduce `MAX_CHUNKS_PER_PDF` |
| Build timeout | Use `ingest_simple.py` |
| Chat not sending | Check browser console |

---

## 📱 Access Points

### Local
- **Chat**: http://localhost:10000/query
- **API**: http://localhost:10000/api/query
- **Health**: http://localhost:10000/health
- **Docs**: http://localhost:10000/docs (FastAPI auto-docs)

### Production (Render)
- **Chat**: https://your-app.onrender.com/query
- **API**: https://your-app.onrender.com/api/query
- **Health**: https://your-app.onrender.com/health

---

## 💡 Pro Tips

1. **First Deploy**: Use `ingest_simple.py` to verify everything works
2. **Then**: Redeploy with `ingest_dataset.py` for full PDFs
3. **Testing**: Use sample questions in chat UI to demo
4. **Customization**: Edit `chat.html` colors/text easily
5. **Monitoring**: Check `/health` endpoint regularly

---

## 🎉 Success Metrics

Your deployment is successful when:
- ✅ `/health` returns `{"status": "ok"}`
- ✅ `/query` loads beautiful chat UI
- ✅ Sample questions work in chat
- ✅ Answers include citations `[1]`, `[2]`
- ✅ API curl test works
- ✅ Mobile browser works

---

## 📞 Quick Help

### File Purposes
- `app.py` → Server routing
- `rag_pipeline.py` → RAG logic
- `chat.html` → Chat UI
- `ingest_*.py` → Data processing
- `*.md` → Documentation

### Where to Look
- **Chat not working?** → Check `app.py` routes
- **API errors?** → Check `rag_pipeline.py`
- **UI issues?** → Edit `static/chat.html`
- **Deploy issues?** → Read `RENDER_DEPLOY.md`
- **General help?** → Read `README.md`

---

## 🚀 Final Command Sequence

```bash
# 1. Set API key
export OPENAI_API_KEY="sk-..."

# 2. Install
pip install -r requirements.txt

# 3. Ingest (choose one)
python ingest_simple.py

# 4. Start
python app.py

# 5. Open browser
open http://localhost:10000/query

# 6. Test
curl http://localhost:10000/health
```

---

**You're ready to deploy and submit! 🎉**

*This is your complete, production-ready RAG system with chat interface!*
