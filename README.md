MedInSight — AI Textbook Medical Reasoning using RAG
===================================================

## 🎯 What's New: Chat Interface!

**Live Chat UI at `/query`** - Beautiful web interface for asking medical questions  
**API Endpoint at `/api/query`** - Programmatic access for integrations  
**Full PDF Support** - Process your Dataset folder with medical textbooks

---

## Overview
MedInSight is a Retrieval-Augmented Generation (RAG) service that answers medical questions grounded in textbook knowledge. It features a modern chat interface and compliant API endpoints.

**Features:**
- 💬 Beautiful chat interface at `/query`
- 🔌 RESTful API at `/api/query`
- 📚 PDF processing from Dataset folder
- 🎯 Citation-backed answers `[1]`, `[2]`
- 🚫 Anti-hallucination fail-safe
- 📱 Mobile-responsive design

---

## 🚀 Quick Start

### Option 1: One-Command Start (macOS/Linux)
```bash
export OPENAI_API_KEY="sk-..."
./start.sh
```

### Option 2: Manual Steps

**1. Set API Key:**
```bash
export OPENAI_API_KEY="sk-..."
```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Choose Ingestion Method:**

**Quick (10 seconds):**
```bash
python ingest_simple.py
```

**Full Dataset PDFs (5-15 min):**
```bash
python ingest_dataset.py
```

**4. Start Server:**
```bash
python app.py
```

**5. Open Chat Interface:**
```
http://localhost:10000/query
```

---

## 🌐 Endpoints

### 1. Chat Interface (New!)
- **URL**: `GET /query`
- **Description**: Interactive web UI for medical questions
- **Features**: 
  - Real-time responses
  - Source citations
  - Message history
  - Mobile-friendly

### 2. API Endpoint
- **URL**: `POST /api/query`
- **Request**:
  ```json
  {
    "query": "What is diabetes?",
    "top_k": 5
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Diabetes is a chronic condition characterized by high blood sugar levels. [1]",
    "contexts": [
      "Diabetes is a chronic condition...",
      "The hallmark of diabetes is..."
    ]
  }
  ```

### 3. Health Check
- **URL**: `GET /health`
- **Response**: `{"status": "ok"}`

---

## 📁 Project Structure

```
├── app.py                  # FastAPI server (API + Chat UI)
├── rag_pipeline.py         # RAG implementation
├── static/
│   └── chat.html          # Chat interface (NEW!)
├── ingest_simple.py        # Quick ingest (built-in knowledge)
├── ingest_dataset.py       # Full PDF processing (NEW!)
├── Dataset/                # Place your PDFs here
├── vectorstore/            # Generated FAISS index
├── requirements.txt        # Dependencies
├── start.sh               # One-command startup (NEW!)
├── README.md              # This file
├── RENDER_DEPLOY.md       # Render deployment guide (NEW!)
└── SUBMISSION_GUIDE.md    # Complete submission docs
```

---

## 📊 Dataset Processing

### Your Dataset Folder
Place medical textbook PDFs in `./Dataset/`:
- Anatomy&Physiology.pdf (94 MB)
- Cardiology.pdf (188 MB)
- Dentistry.pdf (189 MB)
- EmergencyMedicine.pdf (275 MB)
- And more...

### Optimized Processing
`ingest_dataset.py` handles large PDFs efficiently:
- ✅ Chunking with overlap
- ✅ Memory-safe batching
- ✅ Progress tracking
- ✅ Error recovery
- ✅ Max 500 chunks per PDF (configurable)

---

## 🎨 Chat Interface Features

### Modern UI
- Clean, gradient design
- Real-time message updates
- Loading indicators
- Error handling

### Smart Features
- **Sample Questions**: Click to try
- **Source Citations**: See which textbook passages were used
- **Context Display**: View retrieved text snippets
- **Mobile Responsive**: Works on all devices

### Screenshots
![Chat Interface](static/chat.html)  
*Medical chat assistant with source citations*

---

## 🔧 Configuration

### Embedding Model
Currently: `text-embedding-3-small` (1536 dimensions)  
Why: Faster, cheaper, memory-efficient

To use `text-embedding-3-large`:
- Edit `rag_pipeline.py` line 19
- Edit `ingest_*.py` EMB_MODEL variable
- Re-run ingestion

### LLM Model
Currently: `gpt-4o`  
Why: GPT-5 not yet available

### Chunking Settings (ingest_dataset.py)
```python
CHUNK_SIZE = 800           # Characters per chunk
CHUNK_OVERLAP = 200        # Overlap between chunks
MAX_CHUNKS_PER_PDF = 500   # Limit per PDF
BATCH_SIZE = 20            # Embeddings batch size
```

---

## 🚢 Deployment

### Render.com (Recommended)
See **[RENDER_DEPLOY.md](RENDER_DEPLOY.md)** for step-by-step guide.

**Quick Config:**
- Build: `pip install -r requirements.txt && python ingest_simple.py`
- Start: `python app.py`
- Env: `OPENAI_API_KEY=sk-...`

### Other Platforms (Railway, Heroku, AWS)
Similar configuration:
1. Set `OPENAI_API_KEY` environment variable
2. Install requirements
3. Run ingestion in build step
4. Start with `python app.py`

---

## 🧪 Testing

### Manual Test (Browser)
1. Open `http://localhost:10000/query`
2. Type: "What is diabetes?"
3. Click Send
4. Verify answer with citations

### API Test (curl)
```bash
curl -X POST http://localhost:10000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What causes hypertension?", "top_k": 3}'
```

### Automated Tests
```bash
python test_api.py
```

---

## ✅ Hack-A-Cure Compliance

| Requirement | Status | Implementation |
|------------|--------|----------------|
| POST /query endpoint | ✅ | `/api/query` (also `/query` for backward compat) |
| Exact JSON format | ✅ | FastAPI Pydantic models |
| contexts array | ✅ | List of strings |
| 200 OK on success | ✅ | Default behavior |
| Fail-safe message | ✅ | "Information not available in dataset." |
| RAG architecture | ✅ | FAISS + Embeddings + GPT-4o |
| Anti-hallucination | ✅ | Citation requirement |
| /health endpoint | ✅ | Returns {"status": "ok"} |
| <60s response | ✅ | Optimized retrieval |

**BONUS:**  
✨ Chat UI at `/query` - Interactive web interface (not required but impressive!)

---

## 📖 Documentation

- **[RENDER_DEPLOY.md](RENDER_DEPLOY.md)** - Render deployment guide
- **[SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)** - Complete submission checklist
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - General deployment guide

---

## 🐛 Troubleshooting

### "Vectorstore not found"
Run ingestion: `python ingest_simple.py` or `python ingest_dataset.py`

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY="sk-..."
```

### Chat UI not loading
Check that `./static/chat.html` exists

### Memory issues with large PDFs
Reduce `MAX_CHUNKS_PER_PDF` in `ingest_dataset.py`

### API returns fail-safe message
- Check ingestion completed successfully
- Try a different query
- Verify PDFs have extractable text

---

## 💡 Tips

### Adding More Medical Knowledge
1. Edit `ingest_simple.py` → `SAMPLE_TEXTS` array
2. Re-run: `python ingest_simple.py`
3. Restart server

### Using Your Own PDFs
1. Place PDFs in `./Dataset/` folder
2. Run: `python ingest_dataset.py`
3. Start server: `python app.py`

### Customizing Chat UI
Edit `static/chat.html`:
- Colors: Search for gradient values
- Sample questions: Update `sample-questions` div
- Branding: Change header text

---

## 📝 License & Disclaimer

Created for Hack-A-Cure Hackathon.  
Medical knowledge for educational/demo purposes only.  
**Not for actual medical advice.**

---

## 🎉 Ready to Deploy!

1. ✅ Set `OPENAI_API_KEY`
2. ✅ Run ingestion
3. ✅ Start server
4. ✅ Test chat at `/query`
5. ✅ Submit to Hack-A-Cure!

**Good luck!** 🚀
