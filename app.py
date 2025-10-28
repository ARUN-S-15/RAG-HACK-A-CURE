"""
FastAPI application for RAG system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

from rag_engine import RAGEngine

# Initialize FastAPI app
app = FastAPI(
    title="Medical RAG System API",
    description="Retrieval-Augmented Generation system for medical documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = None


# Request/Response models
class QueryRequest(BaseModel):
    question: str
    k: Optional[int] = 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What are the symptoms of heart disease?",
                "k": 5
            }
        }


class Source(BaseModel):
    source: str
    relevance: float


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    model: str


class HealthResponse(BaseModel):
    status: str
    message: str
    vector_store_loaded: bool


@app.on_event("startup")
async def startup_event():
    """Initialize RAG engine on startup."""
    global rag_engine
    print("🚀 Starting up RAG system...")
    try:
        rag_engine = RAGEngine()
        print("✅ RAG engine initialized successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize RAG engine: {e}")
        print("    Vector store may not be built yet. Run ingest.py first.")


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Medical RAG System API is running",
        "vector_store_loaded": rag_engine is not None
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy" if rag_engine else "degraded",
        "message": "System operational" if rag_engine else "Vector store not loaded",
        "vector_store_loaded": rag_engine is not None
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the RAG system with a question.
    
    - **question**: The question to ask
    - **k**: Number of relevant documents to retrieve (default: 5)
    """
    if not rag_engine:
        raise HTTPException(
            status_code=503,
            detail="RAG engine not initialized. Please run ingest.py to build the vector store."
        )
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        result = rag_engine.query(request.question, k=request.k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get statistics about the vector store."""
    if not rag_engine:
        raise HTTPException(
            status_code=503,
            detail="RAG engine not initialized"
        )
    
    try:
        num_vectors = rag_engine.vector_store.index.ntotal
        return {
            "total_documents": num_vectors,
            "embedding_dimension": rag_engine.vector_store.embedding_dim,
            "model_type": "local" if rag_engine.use_local_model else "openai"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


if __name__ == "__main__":
    # Get port from environment variable (for Render deployment)
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
