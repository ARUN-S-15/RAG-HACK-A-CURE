# 🏥 MedInSight - AI Textbook Medical Reasoning using RAG# 🏥 MedInSight - AI Textbook Medical Reasoning using RAG# Medical RAG System 🏥



**Hack-A-Cure Submission**



MedInSight is a Retrieval-Augmented Generation (RAG) system that answers medical questions using textbook PDF datasets. The system prevents hallucinations by strictly grounding answers in retrieved context.**Hack-A-Cure Submission**A Retrieval-Augmented Generation (RAG) system built for medical documents. This system processes medical PDFs, creates embeddings, and allows users to query the knowledge base using natural language.



---



## 🎯 FeaturesMedInSight is a Retrieval-Augmented Generation (RAG) system that answers medical questions using textbook PDF datasets (text + tables + diagrams). The system prevents hallucinations by strictly grounding answers in retrieved context.## 🚀 Features



- ✅ PDF extraction with support for text, tables, and diagrams

- ✅ Semantic chunking with intelligent overlap  

- ✅ OpenAI text-embedding-3-large embeddings (or free fallback)---- **PDF Processing**: Automatically extracts and chunks text from medical PDFs

- ✅ FAISS vector store for fast similarity search

- ✅ GPT-4 for answer generation (or free fallback)- **Vector Search**: Fast similarity search using FAISS

- ✅ Anti-hallucination: Answers strictly grounded in retrieved context

- ✅ Response time: < 60 seconds## 🎯 Project Overview- **Smart Retrieval**: Finds most relevant context for user queries

- ✅ Exact API format compliance for Hack-A-Cure

- **LLM Integration**: Supports both OpenAI GPT and local models

---

### Features- **REST API**: Easy-to-use FastAPI endpoints

## 🚀 Quick Start

- ✅ PDF extraction with support for text, tables, and diagrams- **Deployment Ready**: Configured for Render, AWS, or Docker

### Prerequisites

- ✅ Semantic chunking with intelligent overlap

- Python 3.9+

- (Optional) OpenAI API key for better performance- ✅ OpenAI text-embedding-3-large embeddings## 📋 Prerequisites



### Installation- ✅ FAISS vector store for fast similarity search



```bash- ✅ GPT-4 for answer generation- Python 3.10+

# Clone the repository

git clone https://github.com/ARUN-S-15/RAG-HACK-A-CURE.git- ✅ Anti-hallucination: Answers strictly grounded in retrieved context- (Optional) OpenAI API key for better responses

cd RAG-HACK-A-CURE

- ✅ Response time: < 60 seconds

# Install dependencies

pip install -r requirements.txt- ✅ Exact API format compliance for Hack-A-Cure## 🛠️ Installation

```



### Configuration

### Technology Stack### 1. Clone or download this repository

Create a `.env` file:



```bash

cp .env.example .env| Component | Technology |### 2. Install dependencies

```

|-----------|-----------|

Edit `.env` and optionally add your OpenAI API key:

| **PDF Extraction** | PyMuPDF (with pdfplumber/PyPDF2 fallbacks) |```bash

```env

OPENAI_API_KEY=your_key_here| **Chunking** | Semantic splitting with 200-char overlap |pip install -r requirements.txt



# Optional| **Embeddings** | OpenAI text-embedding-3-large |```

CHUNK_SIZE=1000

CHUNK_OVERLAP=200| **Vector Store** | FAISS |

```

| **Retrieval** | similarity_search(top_k) |### 3. Configure environment (optional)

**Note:** If you don't have an OpenAI key, the system will use a free fallback model!

| **LLM** | GPT-4 via OpenAI API |

### Build Vector Store

| **Framework** | FastAPI |Create a `.env` file:

```bash

python ingest.py

```

---```bash

### Start API Server

cp .env.example .env

```bash

python app.py## 📁 Project Structure```

```



Server will start at `http://localhost:8000`

```Edit `.env` and add your OpenAI API key (optional):

---

RAG-HACK-A-CURE/```

## 📡 API Endpoints


| Endpoint | Type | Description |

|----------|------|-------------|├── rag_pipeline.py         # RAG retrieval + generation logic

| `/health` | GET | Health check |

| `/query` | POST | Main RAG query endpoint |├── ingest.py               # PDF ingestion + FAISS indexingUSE_LOCAL_MODEL=false

| `/docs` | GET | Interactive API documentation |

| `/` | GET | API information |├── requirements.txt        # Python dependencies```



---├── README.md               # This file



## 🧪 Testing├── .env.example            # Environment variables templateOr use local model (no API key needed):



### Test Health Check├── pdfs/                   # Place your PDF files here```



```bash└── vectorstore/            # FAISS index (created after ingestion)USE_LOCAL_MODEL=true

curl http://localhost:8000/health

```    ├── faiss.index```



### Test Query Endpoint    └── metadata.pkl



```bash```## 📊 Build the Vector Store

curl -X POST http://localhost:8000/query \

  -H "Content-Type: application/json" \

  -d '{

    "query": "What is diabetes?",---Process the PDFs and build the vector database:

    "top_k": 2

  }'

```

## 🚀 Quick Start```bash

**Expected Response:**

python ingest.py

```json

{### 1. Prerequisites```

  "answer": "Diabetes is a chronic metabolic disease...",

  "contexts": [

    "Diabetes is a chronic metabolic disease...",

    "The hallmark of diabetes is..."- Python 3.9+This will:

  ]

}- OpenAI API key- Load all PDFs from the `Dataset/` folder

```

- Split documents into chunks

---

### 2. Installation- Create embeddings using sentence-transformers

## 🚢 Deployment

- Build a FAISS index

### Deploy to Render

```bash- Save everything to `vector_store/`

1. Push code to GitHub

2. Go to [Render Dashboard](https://dashboard.render.com/)# Clone the repository

3. New → Web Service

4. Connect your repogit clone https://github.com/ARUN-S-15/RAG-HACK-A-CURE.git## 🎯 Usage

5. Configure:

   - **Build Command:** `pip install -r requirements.txt && python ingest.py`cd RAG-HACK-A-CURE

   - **Start Command:** `python app.py`

   - **Environment:** Add `PORT=10000` and optionally `OPENAI_API_KEY`### Option 1: Command Line Interface

6. Deploy!

# Install dependencies

See `DEPLOYMENT.md` for detailed instructions.

pip install -r requirements.txtTest the RAG system directly:

### Deploy to Vercel

```

**Note:** Vercel is optimized for serverless functions. For this RAG API with persistent vector store, **Render is recommended**.

```bash

---

### 3. Configurationpython rag_engine.py

## 📚 Documentation

```

- **Interactive Docs:** Visit `/docs` for Swagger UI

- **Deployment Guide:** See `DEPLOYMENT.md`Create a `.env` file in the project root:

- **API Specification:** Hack-A-Cure compliant format

Then ask questions like:

---

```bash- "What are the symptoms of heart disease?"

## ✅ Hack-A-Cure Compliance

# Copy from example- "Explain diabetes management"

- ✅ POST `/query` endpoint

- ✅ Request format: `{query, top_k}`cp .env.example .env- "What are common dental procedures?"

- ✅ Response format: `{answer, contexts[]}`

- ✅ Returns 200 OK only```

- ✅ contexts = array of plain strings

- ✅ Anti-hallucination built-in### Option 2: REST API

- ✅ `/health` endpoint

- ✅ Response time < 60 secondsEdit `.env` and add your OpenAI API key:

- ✅ Fail-safe responses

Start the API server:

---

```env

## 🏗️ Architecture

OPENAI_API_KEY=your_openai_api_key_here```bash

```

User Query → FastAPI → RAG Pipeline → FAISS Search → GPT-4 → Responsepython app.py

```

# Optional configurations```

**Components:**

- `app.py` - FastAPI serverCHUNK_SIZE=1000

- `rag_pipeline.py` - RAG logic

- `ingest.py` - PDF processing & indexingCHUNK_OVERLAP=200The API will be available at `http://localhost:8000`

- `vectorstore/` - FAISS index

```

---

**API Endpoints:**

## 📄 License

### 4. Add PDF Documents

MIT License

- `GET /` - Health check

---

Place your medical textbook PDFs in the `pdfs/` directory:- `GET /health` - Detailed health status

## 👥 Team

- `GET /stats` - Vector store statistics

Hack-A-Cure submission by ARUN-S-15

```bash- `POST /query` - Query the RAG system

---

mkdir -p pdfs

**🎉 Ready for deployment!**

# Copy your PDF files to pdfs/**Example request:**

```

```bash

**Note:** If no PDFs are found, the system will create placeholder content for testing.curl -X POST "http://localhost:8000/query" \

  -H "Content-Type: application/json" \

### 5. Build Vector Store  -d '{

    "question": "What are the symptoms of heart disease?",

Run the ingestion pipeline to process PDFs and build the FAISS index:    "k": 5

  }'

```bash```

python ingest.py

```**API Documentation:**

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

Expected output:

```## 🌐 Deployment

============================================================

🏗️  Building Vector Store for MedInSight### Option 1: Deploy to Render (Easiest)

============================================================

📚 Found 5 PDF file(s) in ./pdfs/1. Create a Render account at https://render.com

📖 Using PYMUPDF for PDF extraction2. Create a new Web Service

3. Connect your GitHub repository

Processing: medical_textbook_1.pdf4. Render will automatically detect `render.yaml`

  ✓ Created 234 chunks5. Click "Create Web Service"

...

📊 Total chunks created: 1,247The service will:

🔄 Creating embeddings with OpenAI text-embedding-3-large...- Install dependencies

✅ FAISS index built with 1,247 vectors- Build the vector store from your PDFs

💾 Vector store saved to ./vectorstore/faiss.index- Start the API server

============================================================- Provide you with a public URL

✅ Vector store built successfully!

============================================================### Option 2: Deploy to AWS/EC2

```

1. Launch an EC2 instance (t2.medium or larger recommended)

### 6. Start the API Server2. SSH into your instance

3. Install dependencies:

```bash   ```bash

python app.py   sudo apt update

```   sudo apt install python3-pip

   ```

Expected output:4. Clone your repository

```5. Install requirements:

============================================================   ```bash

🚀 MedInSight - Hack-A-Cure RAG System Starting...   pip3 install -r requirements.txt

============================================================   ```

📚 Loading vector store...6. Build vector store:

🤖 Initializing RAG pipeline...   ```bash

✅ RAG system initialized successfully!   python3 ingest.py

============================================================   ```

🌐 Starting server on http://0.0.0.0:80007. Run the app:

📖 API docs available at http://localhost:8000/docs   ```bash

```   python3 app.py

   ```

The server will start on `http://localhost:8000` (or port specified in `PORT` environment variable).8. Configure security group to allow port 8000



---### Option 3: Deploy with Docker



## 📡 API EndpointsBuild the image:

```bash

### 1. Health Checkdocker build -t medical-rag .

```

**Endpoint:** `GET /health`

Run the container:

**Response:**```bash

```jsondocker run -p 8000:8000 -v $(pwd)/Dataset:/app/Dataset medical-rag

{```

  "status": "ok"

}## 📁 Project Structure

```

```

**Example:**.

```bash├── Dataset/                    # Medical PDF files

curl http://localhost:8000/health│   ├── Anatomy&Physiology.pdf

```│   ├── Cardiology.pdf

│   └── ...

### 2. Query Endpoint (Main)├── vector_store/              # Generated vector database (after build)

│   ├── faiss.index

**Endpoint:** `POST /query`│   └── metadata.pkl

├── ingest.py                  # Document processing & vector store builder

**Request Format:**├── rag_engine.py             # RAG query engine

```json├── app.py                    # FastAPI application

{├── requirements.txt          # Python dependencies

  "query": "string (required)",├── Dockerfile               # Docker configuration

  "top_k": 5  // optional, default: 5├── render.yaml              # Render deployment config

}└── README.md                # This file

``````



**Response Format:**## 🔧 Configuration

```json

{Edit these settings in your `.env` file:

  "answer": "Concise, medically accurate response",

  "contexts": ["Snippet 1", "Snippet 2", ...]- `OPENAI_API_KEY`: Your OpenAI API key (optional)

}- `USE_LOCAL_MODEL`: Set to `true` to use local extractive model

```- `CHUNK_SIZE`: Size of text chunks (default: 1000)

- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)

**Rules:**

- Returns 200 OK on success only## 📈 Performance Tips

- `contexts` must be array of plain strings

- Answer must be concise and based only on retrieved text1. **For better answers**: Use OpenAI GPT models (requires API key)

- Fail-safe: If retrieval fails → `answer: "Information not available in dataset."`2. **For cost-effective**: Use local extractive model (no API key needed)

3. **For faster search**: Reduce number of retrieved documents (`k` parameter)

---4. **For better accuracy**: Increase number of retrieved documents



## 🧪 Testing## 🧪 Testing



### Test 1: Basic QueryTest the API with curl:



```bash```bash

curl -X POST http://localhost:8000/query \# Health check

  -H "Content-Type: application/json" \curl http://localhost:8000/health

  -d '{

    "query": "What is diabetes?",# Get statistics

    "top_k": 2curl http://localhost:8000/stats

  }'

```# Query the system

curl -X POST "http://localhost:8000/query" \

**Expected Response:**  -H "Content-Type: application/json" \

```json  -d '{"question": "What is cardiology?", "k": 5}'

{```

  "answer": "Diabetes is a chronic metabolic disease characterized by elevated levels of blood glucose, which can lead to serious damage to the heart, blood vessels, eyes, kidneys, and nerves over time.",

  "contexts": [## 🐛 Troubleshooting

    "Diabetes is a chronic metabolic disease characterized by elevated levels of blood glucose (or blood sugar), which leads over time to serious damage to the heart, blood vessels, eyes, kidneys, and nerves.",

    "The hallmark of diabetes is elevated glucose levels in the blood. This condition can result from the body's inability to produce insulin, use insulin effectively, or both."**"Vector store not found"**

  ]- Run `python ingest.py` first to build the vector store

}

```**"OPENAI_API_KEY not set"**

- Either add your API key to `.env` or set `USE_LOCAL_MODEL=true`

### Test 2: Complex Medical Query

**Slow performance**

```bash- Reduce `k` parameter in queries

curl -X POST http://localhost:8000/query \- Use a machine with more RAM

  -H "Content-Type: application/json" \- Consider using GPU for embeddings

  -d '{

    "query": "What are the symptoms of heart disease?",## 📝 License

    "top_k": 3

  }'This project is for hackathon purposes.

```

## 🤝 Contributing

### Test 3: Query Not in Dataset

Built for HackACure hackathon.

```bash

curl -X POST http://localhost:8000/query \---

  -H "Content-Type: application/json" \

  -d '{**Made with ❤️ for better healthcare information access**

    "query": "How to perform brain surgery?",
    "top_k": 5
  }'
```

**Expected Response:**
```json
{
  "answer": "Information not available in dataset.",
  "contexts": []
}
```

### Test 4: Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "What is hypertension?",
        "top_k": 3
    }
)

print(response.json())
```

---

## 🔧 Configuration Options

### Environment Variables

Create a `.env` file with the following options:

```env
# Required
OPENAI_API_KEY=your_api_key_here

# Optional - Chunking Configuration
CHUNK_SIZE=1000          # Characters per chunk (default: 1000)
CHUNK_OVERLAP=200        # Overlap between chunks (default: 200)

# Optional - Server Configuration
PORT=8000                # API server port (default: 8000)
```

### Customizing Chunking Strategy

Edit parameters in `ingest.py`:

```python
processor = DocumentProcessor(
    chunk_size=1500,      # Larger chunks for more context
    chunk_overlap=300     # More overlap for continuity
)
```

---

## 🧠 RAG Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 1. PDF EXTRACTION                                           │
│    PyMuPDF → Extract text, tables, diagrams                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. SEMANTIC CHUNKING                                        │
│    Split at sentence boundaries with overlap                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. EMBEDDINGS                                               │
│    OpenAI text-embedding-3-large (3072 dims)                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. VECTOR STORE                                             │
│    FAISS IndexFlatL2 for similarity search                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. RETRIEVAL (Query Time)                                   │
│    Query → Embedding → FAISS search → Top-K contexts        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. GENERATION                                               │
│    GPT-4 with strict grounding instructions                 │
│    Temperature: 0.1 (factual accuracy)                      │
│    Max tokens: 500 (concise answers)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Anti-Hallucination Strategy

The system implements multiple layers to prevent hallucinations:

1. **Strict Prompt Engineering:**
   ```
   "Answer ONLY using information from the provided contexts"
   "If the answer is not in the contexts, respond with: 
    'Information not available in dataset.'"
   ```

2. **Low Temperature:** `temperature=0.1` for deterministic, factual responses

3. **Context Verification:** All answers must quote or paraphrase from retrieved snippets

4. **Fail-Safe Response:** If retrieval fails or no relevant context is found, the system returns: `"Information not available in dataset."`

---

## 🚢 Deployment

### Local Development

```bash
python app.py
# Server runs on http://localhost:8000
```

### Production (Render / Cloud)

The project includes deployment configurations:

**render.yaml:**
```yaml
services:
  - type: web
    name: medinsight-api
    env: python
    buildCommand: "pip install -r requirements.txt && python ingest.py"
    startCommand: "python app.py"
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PORT
        value: 10000
```

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python ingest.py
CMD ["python", "app.py"]
```

### Environment Variables for Production

Set these in your deployment platform:
- `OPENAI_API_KEY` (required)
- `PORT` (optional, defaults to 8000)

---

## 📊 Performance Metrics

- **Latency:** < 60 seconds per query
- **Embedding Speed:** ~100 chunks/second (batch processing)
- **Memory:** ~2GB with 10,000 document chunks
- **Accuracy:** Depends on dataset quality and coverage

---

## 🐛 Troubleshooting

### Issue: "Vector store not found"

**Solution:**
```bash
python ingest.py
```
Make sure PDFs are in the `pdfs/` directory.

### Issue: "OpenAI API key not found"

**Solution:**
1. Create `.env` file
2. Add: `OPENAI_API_KEY=your_key_here`

### Issue: "No PDF files found"

**Solution:**
```bash
mkdir -p pdfs
# Add your PDF files to pdfs/ directory
python ingest.py
```

The system will use placeholder content if no PDFs are available (for testing only).

### Issue: "Connection refused" or "ERR_CONNECTION_REFUSED"

**Solution:**
1. Make sure the API server is running: `python app.py`
2. Check if the port is correct (default: 8000)
3. If using a different port, update the URL in your requests

---

## 📝 API Documentation

Interactive API documentation is available at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## ✅ Hack-A-Cure Compliance Checklist

- ✅ FastAPI server with single POST /query endpoint
- ✅ Request format: `{"query": "string", "top_k": 5}`
- ✅ Response format: `{"answer": "string", "contexts": ["snippet1", ...]}`
- ✅ Returns 200 OK on success only
- ✅ contexts is array of plain strings
- ✅ Concise answers grounded in retrieved text
- ✅ Fail-safe: "Information not available in dataset."
- ✅ PDF extraction (PyMuPDF)
- ✅ Semantic chunking with overlap
- ✅ OpenAI text-embedding-3-large
- ✅ FAISS vector store
- ✅ GPT-4 for generation
- ✅ Anti-hallucination measures
- ✅ Response time < 60 seconds
- ✅ /health endpoint

---

## 👥 Team

**Hack-A-Cure Submission by:** ARUN-S-15

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 and embedding models
- Facebook Research for FAISS
- FastAPI team for the excellent framework
- Hack-A-Cure organizers

---

**For questions or issues, please open an issue on GitHub.**
