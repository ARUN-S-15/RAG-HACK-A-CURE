# Medical RAG System 🏥

A Retrieval-Augmented Generation (RAG) system built for medical documents. This system processes medical PDFs, creates embeddings, and allows users to query the knowledge base using natural language.

## 🚀 Features

- **PDF Processing**: Automatically extracts and chunks text from medical PDFs
- **Vector Search**: Fast similarity search using FAISS
- **Smart Retrieval**: Finds most relevant context for user queries
- **LLM Integration**: Supports both OpenAI GPT and local models
- **REST API**: Easy-to-use FastAPI endpoints
- **Deployment Ready**: Configured for Render, AWS, or Docker

## 📋 Prerequisites

- Python 3.10+
- (Optional) OpenAI API key for better responses

## 🛠️ Installation

### 1. Clone or download this repository

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment (optional)

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key (optional):
```
OPENAI_API_KEY=sk-your-key-here
USE_LOCAL_MODEL=false
```

Or use local model (no API key needed):
```
USE_LOCAL_MODEL=true
```

## 📊 Build the Vector Store

Process the PDFs and build the vector database:

```bash
python ingest.py
```

This will:
- Load all PDFs from the `Dataset/` folder
- Split documents into chunks
- Create embeddings using sentence-transformers
- Build a FAISS index
- Save everything to `vector_store/`

## 🎯 Usage

### Option 1: Command Line Interface

Test the RAG system directly:

```bash
python rag_engine.py
```

Then ask questions like:
- "What are the symptoms of heart disease?"
- "Explain diabetes management"
- "What are common dental procedures?"

### Option 2: REST API

Start the API server:

```bash
python app.py
```

The API will be available at `http://localhost:8000`

**API Endpoints:**

- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /stats` - Vector store statistics
- `POST /query` - Query the RAG system

**Example request:**

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the symptoms of heart disease?",
    "k": 5
  }'
```

**API Documentation:**
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## 🌐 Deployment

### Option 1: Deploy to Render (Easiest)

1. Create a Render account at https://render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click "Create Web Service"

The service will:
- Install dependencies
- Build the vector store from your PDFs
- Start the API server
- Provide you with a public URL

### Option 2: Deploy to AWS/EC2

1. Launch an EC2 instance (t2.medium or larger recommended)
2. SSH into your instance
3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip
   ```
4. Clone your repository
5. Install requirements:
   ```bash
   pip3 install -r requirements.txt
   ```
6. Build vector store:
   ```bash
   python3 ingest.py
   ```
7. Run the app:
   ```bash
   python3 app.py
   ```
8. Configure security group to allow port 8000

### Option 3: Deploy with Docker

Build the image:
```bash
docker build -t medical-rag .
```

Run the container:
```bash
docker run -p 8000:8000 -v $(pwd)/Dataset:/app/Dataset medical-rag
```

## 📁 Project Structure

```
.
├── Dataset/                    # Medical PDF files
│   ├── Anatomy&Physiology.pdf
│   ├── Cardiology.pdf
│   └── ...
├── vector_store/              # Generated vector database (after build)
│   ├── faiss.index
│   └── metadata.pkl
├── ingest.py                  # Document processing & vector store builder
├── rag_engine.py             # RAG query engine
├── app.py                    # FastAPI application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── render.yaml              # Render deployment config
└── README.md                # This file
```

## 🔧 Configuration

Edit these settings in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key (optional)
- `USE_LOCAL_MODEL`: Set to `true` to use local extractive model
- `CHUNK_SIZE`: Size of text chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)

## 📈 Performance Tips

1. **For better answers**: Use OpenAI GPT models (requires API key)
2. **For cost-effective**: Use local extractive model (no API key needed)
3. **For faster search**: Reduce number of retrieved documents (`k` parameter)
4. **For better accuracy**: Increase number of retrieved documents

## 🧪 Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/health

# Get statistics
curl http://localhost:8000/stats

# Query the system
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is cardiology?", "k": 5}'
```

## 🐛 Troubleshooting

**"Vector store not found"**
- Run `python ingest.py` first to build the vector store

**"OPENAI_API_KEY not set"**
- Either add your API key to `.env` or set `USE_LOCAL_MODEL=true`

**Slow performance**
- Reduce `k` parameter in queries
- Use a machine with more RAM
- Consider using GPU for embeddings

## 📝 License

This project is for hackathon purposes.

## 🤝 Contributing

Built for HackACure hackathon.

---

**Made with ❤️ for better healthcare information access**
