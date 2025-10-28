# 🚀 Deploying MedInSight RAG API to Render

This guide will help you deploy your RAG API to Render so you can access `/docs` and all endpoints publicly.

---

## 📋 Prerequisites

1. A [Render account](https://render.com/) (free tier works!)
2. Your GitHub repository pushed to GitHub
3. (Optional) OpenAI API key for better performance

---

## 🎯 Deployment Steps

### Option 1: Deploy via Render Dashboard (Recommended)

#### Step 1: Push to GitHub

Make sure all your changes are committed and pushed:

```bash
cd /Users/hariprasathc/Hackathon/RAG-HACK-A-CURE

# Add all files
git add .

# Commit changes
git commit -m "Complete RAG API for Hack-A-Cure submission"

# Push to GitHub
git push origin main
```

#### Step 2: Create Web Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `ARUN-S-15/RAG-HACK-A-CURE`
4. Configure the service:

**Settings:**
- **Name:** `medinsight-rag-api` (or any name you want)
- **Region:** Oregon (or closest to you)
- **Branch:** `main`
- **Root Directory:** (leave empty)
- **Runtime:** `Python 3`
- **Build Command:** 
  ```bash
  pip install -r requirements.txt && python ingest.py
  ```
- **Start Command:** 
  ```bash
  python app.py
  ```
- **Plan:** `Free`

#### Step 3: Add Environment Variables

In the **Environment** section, add:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `PORT` | `10000` | Render default port |
| `OPENAI_API_KEY` | `your_key_here` | Optional - use your OpenAI key for better results |

**If you don't have an OpenAI key:** The system will work with the free fallback model (sentence-transformers)!

#### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (3-5 minutes)
3. Watch the build logs

#### Step 5: Access Your API

Once deployed, Render will give you a URL like:
```
https://medinsight-rag-api.onrender.com
```

**Your endpoints will be:**
- 🏠 Root: `https://medinsight-rag-api.onrender.com/`
- 📚 **Interactive Docs**: `https://medinsight-rag-api.onrender.com/docs` ⭐
- 📖 Alternative Docs: `https://medinsight-rag-api.onrender.com/redoc`
- ❤️ Health Check: `https://medinsight-rag-api.onrender.com/health`
- 🔍 Query: `POST https://medinsight-rag-api.onrender.com/query`

---

### Option 2: Deploy via render.yaml (Infrastructure as Code)

If you want to use the `render.yaml` file:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your repository
4. Render will automatically detect `render.yaml` and configure everything
5. Add your `OPENAI_API_KEY` in the dashboard (optional)
6. Deploy!

---

## 🧪 Testing Your Deployed API

### Test 1: Check if it's running
```bash
curl https://your-app-name.onrender.com/health
```

**Expected Response:**
```json
{"status": "ok"}
```

### Test 2: Query the RAG system
```bash
curl -X POST https://your-app-name.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diabetes?", "top_k": 2}'
```

**Expected Response:**
```json
{
  "answer": "Diabetes is a chronic metabolic disease...",
  "contexts": ["context1", "context2"]
}
```

### Test 3: Visit the Interactive Docs
Open in your browser:
```
https://your-app-name.onrender.com/docs
```

You'll see the beautiful Swagger UI where you can test all endpoints!

---

## 🔧 Important Notes

### Free Tier Limitations

- **Cold starts:** The free tier spins down after 15 minutes of inactivity
- **First request after sleep:** Takes ~30-60 seconds to wake up
- **Solution for demos:** Keep the service active by pinging it or upgrade to paid tier

### Keep Service Awake (Optional)

Create a simple cron job or use a service like [UptimeRobot](https://uptimerobot.com/) to ping your `/health` endpoint every 10 minutes.

### Adding PDFs

To add your medical PDFs after deployment:

**Option A:** Commit PDFs to GitHub (if they're small)
```bash
# Add PDFs to the pdfs folder
cp your_medical_textbook.pdf pdfs/

# Commit and push
git add pdfs/
git commit -m "Add medical textbooks"
git push origin main

# Render will auto-redeploy
```

**Option B:** Use Render Disks (for larger files)
- Go to your service in Render Dashboard
- Add a **Persistent Disk**
- Upload PDFs via SSH or file sync

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution:** Check that all dependencies are in `requirements.txt`

### Issue: "Vector store not found"

**Solution:** The build command should run `python ingest.py`. Check build logs.

### Issue: "OpenAI API error"

**Solution:** Either:
1. Add valid `OPENAI_API_KEY` in Render dashboard, OR
2. Leave it blank - the system will use free fallback model

### Issue: "Application failed to start"

**Solution:** Check logs in Render dashboard. Common fixes:
- Ensure `PORT` environment variable is set
- Check that `app.py` uses `os.getenv("PORT", 8000)`

---

## 📊 Monitoring Your Deployment

### View Logs
1. Go to Render Dashboard
2. Click on your service
3. Click **"Logs"** tab
4. You'll see real-time logs

### Check Metrics
1. Click **"Metrics"** tab
2. See CPU, Memory, Request counts

---

## 🎉 Success Checklist

Once deployed, verify:

- ✅ `/health` returns `{"status": "ok"}`
- ✅ `/` returns API information
- ✅ `/docs` shows Swagger UI
- ✅ `/query` accepts POST requests and returns answers
- ✅ No errors in Render logs

---

## 🔗 Update Your Frontend

Once deployed, update your `index.html` to use the Render URL:

```javascript
const API_URL = 'https://your-app-name.onrender.com';
```

Replace `http://localhost:8000` with your Render URL.

---

## 💡 Pro Tips

1. **Custom Domain:** You can add a custom domain in Render settings
2. **HTTPS:** Render provides free SSL certificates automatically
3. **Auto-Deploy:** Enable auto-deploy from GitHub for continuous deployment
4. **Health Checks:** Render automatically uses `/health` endpoint
5. **Scaling:** Upgrade to paid tier for better performance and no cold starts

---

## 📞 Support

If you run into issues:
- Check [Render Documentation](https://render.com/docs)
- Review build/runtime logs in Render Dashboard
- Ensure all environment variables are set correctly

---

**Your API will be live at:** `https://your-app-name.onrender.com/docs` 🎊
