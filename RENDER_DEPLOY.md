# 🚀 Render Deployment Guide - MedInSight RAG with Chat UI

## What You're Deploying

- ✅ Chat interface at `/query` (GET) - Beautiful web UI
- ✅ API endpoint at `/api/query` (POST) - For programmatic access
- ✅ Health check at `/health` (GET)
- ✅ RAG powered by your Dataset PDFs or quick medical knowledge base

---

## 📋 Pre-Deployment Checklist

### Option A: Quick Deploy (Built-in Knowledge)
- [ ] OpenAI API key ready
- [ ] GitHub repo pushed (or manual deploy)

### Option B: Full Deploy (Your Dataset PDFs)
- [ ] PDFs in `./Dataset/` folder
- [ ] OpenAI API key ready
- [ ] Sufficient build timeout (10-15 min for large PDFs)

---

## 🔧 Render Configuration

### Step 1: Create New Web Service

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo or choose "Manual Deploy"

### Step 2: Basic Settings

| Setting | Value |
|---------|-------|
| **Name** | `medinsi ght-rag` (or your choice) |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | See below ⬇️ |
| **Start Command** | `python app.py` |

### Step 3: Build Command

**For Quick Deploy (Built-in Knowledge):**
```bash
pip install -r requirements.txt && python ingest_simple.py
```

**For Full Deploy (Dataset PDFs):**
```bash
pip install -r requirements.txt && python ingest_dataset.py
```

### Step 4: Environment Variables

Click "Advanced" and add:

| Key | Value | Notes |
|-----|-------|-------|
| `OPENAI_API_KEY` | `sk-your-key-here` | ⚠️ Required! |
| `PYTHON_VERSION` | `3.11.0` | Optional, recommended |

### Step 5: Instance Type

- **Free Tier**: Works for demo/testing
- **Starter ($7/mo)**: Recommended for production
- **Standard**: For heavy traffic

### Step 6: Advanced Settings (Optional)

- **Health Check Path**: `/health`
- **Auto-Deploy**: Enable if using GitHub

---

## 📦 What Happens During Build

1. **Install Dependencies** (~2 min)
   - FastAPI, OpenAI client, FAISS, PyMuPDF, etc.

2. **Run Ingestion** (time varies)
   - **Quick**: ~10 seconds (20 chunks)
   - **Dataset**: 5-15 minutes (depends on PDF size)
   - Creates `./vectorstore/index.faiss` and `metadata.pkl`

3. **Start Server**
   - Loads vectorstore into memory
   - Starts FastAPI on port from `$PORT` env var

---

## ✅ Verify Deployment

### After deployment completes:

1. **Health Check**
   ```bash
   curl https://your-app.onrender.com/health
   ```
   Should return: `{"status": "ok"}`

2. **Open Chat Interface**
   ```
   https://your-app.onrender.com/query
   ```
   You should see the MedInSight chat UI!

3. **Test API**
   ```bash
   curl -X POST https://your-app.onrender.com/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is diabetes?", "top_k": 3}'
   ```

---

## 🐛 Troubleshooting

### Build Fails: "OPENAI_API_KEY environment variable is required"
**Fix**: Add `OPENAI_API_KEY` in Render environment variables

### Build Timeout with Dataset PDFs
**Fix**: 
- Reduce `MAX_CHUNKS_PER_PDF` in `ingest_dataset.py` (currently 500)
- Or use `ingest_simple.py` instead
- Or upgrade to Starter plan for longer build time

### "Vectorstore not found" Error
**Fix**: Make sure build command includes ingestion:
```bash
pip install -r requirements.txt && python ingest_simple.py
```

### Chat UI Not Loading
**Fix**: Check that `./static/chat.html` exists in your repo

### API Returns "Information not available in dataset"
**Possible causes**:
- Ingestion didn't run (check build logs)
- Query doesn't match indexed content
- Try with a different question

---

## 📊 Monitoring

### View Logs
Render Dashboard → Your Service → Logs

Look for:
```
✅ Successfully indexed X chunks into ./vectorstore
INFO: Uvicorn running on http://0.0.0.0:XXXX
```

### Check Resource Usage
Render Dashboard → Your Service → Metrics

- **Memory**: Should be under 512MB for quick ingest, up to 1GB for dataset
- **CPU**: Spikes during ingestion, low during normal operation

---

## 🔄 Updating Your Deployment

### To Re-ingest Data:

1. Modify `ingest_simple.py` or `ingest_dataset.py`
2. Push to GitHub (if auto-deploy enabled)
3. Or click "Manual Deploy" → "Clear build cache & deploy"

### To Update Chat UI:

1. Edit `static/chat.html`
2. Push changes
3. Deploy will automatically pick up new UI

---

## 💡 Pro Tips

### 1. Custom Domain
Render Settings → Custom Domains → Add your domain

### 2. Environment-Specific Configs
```python
# In app.py
import os
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

### 3. Monitoring with Health Checks
Set up UptimeRobot or similar to ping `/health` every 5 minutes

### 4. Cost Optimization
- Use `ingest_simple.py` for demo (instant, free)
- Only use `ingest_dataset.py` when you need full PDFs
- Downgrade to Free tier for testing

---

## 📱 Testing the Chat Interface

### Desktop
1. Go to `https://your-app.onrender.com/query`
2. Type a question: "What is hypertension?"
3. Click Send
4. See answer with source citations

### Mobile
- Fully responsive
- Works on all devices
- Touch-optimized input

### Sample Questions
- "What is diabetes?"
- "What are symptoms of asthma?"
- "How is pneumonia treated?"
- "What causes stroke?"

---

## 🎯 Submission to Hack-A-Cure

### Your Submission URL:
```
https://your-app-name.onrender.com
```

### API Endpoints for Judges:
- **Chat UI**: `https://your-app-name.onrender.com/query` (GET)
- **API**: `https://your-app-name.onrender.com/api/query` (POST)
- **Health**: `https://your-app-name.onrender.com/health` (GET)

### What Judges Will See:

1. **Beautiful Chat Interface**
   - Clean, modern UI
   - Real-time responses
   - Source citations
   - Mobile-friendly

2. **Compliant API**
   - Exact JSON format required
   - Fail-safe responses
   - Grounded answers with citations

3. **Professional Documentation**
   - README.md
   - DEPLOYMENT.md
   - This guide

---

## ✨ Final Checklist Before Submission

- [ ] Deployment successful (green status in Render)
- [ ] `/health` returns `{"status": "ok"}`
- [ ] Chat UI loads at `/query`
- [ ] Can ask questions and get answers
- [ ] Answers include source citations `[1]`, `[2]`, etc.
- [ ] API endpoint `/api/query` works with curl
- [ ] All environment variables set correctly
- [ ] Build logs show successful ingestion

---

## 🎉 You're Ready!

Your MedInSight RAG API with chat interface is now live and ready for submission!

**URL to submit**: `https://your-app-name.onrender.com`

Good luck! 🚀
