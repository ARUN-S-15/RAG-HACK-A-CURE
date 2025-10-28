"""
FastAPI Application for MedInSight - AI Textbook Medical Reasoning using RAG
Hack-A-Cure Submission
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List
import uvicorn
import os
import sys

# Initialize FastAPI app
app = FastAPI(
    title="MedInSight - Medical RAG API",
    description="AI Textbook Medical Reasoning using RAG for Hack-A-Cure",
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

# Global RAG pipeline instance
rag_pipeline = None


# ============ Request/Response Models ============

class QueryRequest(BaseModel):
    """Request model for /query endpoint"""
    query: str = Field(..., description="Medical question to answer")
    top_k: int = Field(default=5, description="Number of contexts to retrieve", ge=1, le=20)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is diabetes?",
                "top_k": 5
            }
        }


class QueryResponse(BaseModel):
    """Response model for /query endpoint - EXACT format for Hack-A-Cure"""
    answer: str = Field(..., description="Concise, medically accurate response")
    contexts: List[str] = Field(..., description="Array of retrieved text snippets")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Diabetes is a chronic condition characterized by high blood sugar levels.",
                "contexts": [
                    "Diabetes is a chronic metabolic disease...",
                    "The hallmark of diabetes is elevated glucose levels..."
                ]
            }
        }


class HealthResponse(BaseModel):
    """Response model for /health endpoint"""
    status: str


# ============ Startup Event ============

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup"""
    global rag_pipeline
    
    print("=" * 60)
    print("🚀 MedInSight - Hack-A-Cure RAG System Starting...")
    print("=" * 60)
    
    try:
        # Import here to avoid circular imports
        from ingest import VectorStore
        from rag_pipeline import RAGPipeline
        
        # Load vector store
        print("📚 Loading vector store...")
        vector_store = VectorStore()
        
        if not vector_store.load():
            print("⚠️  WARNING: Vector store not found!")
            print("   Please run: python ingest.py")
            print("   The API will start but /query will fail until vector store is built.")
            return
        
        # Initialize RAG pipeline
        print("🤖 Initializing RAG pipeline...")
        rag_pipeline = RAGPipeline(vector_store)
        
        print("✅ RAG system initialized successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        print("   The API will start but /query endpoint will not work.")
        print("   Please check your configuration and run ingest.py")
        import traceback
        traceback.print_exc()


# ============ API Endpoints ============

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - returns 200 OK if service is running.
    Required for Hack-A-Cure submission.
    """
    return {"status": "ok"}


@app.get("/favicon.ico")
async def favicon():
    """Serve the favicon"""
    favicon_path = os.path.join(os.path.dirname(__file__), "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    else:
        raise HTTPException(status_code=404, detail="Favicon not found")


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main RAG query endpoint.
    
    **Required Format for Hack-A-Cure:**
    - Request: {"query": "string", "top_k": 5}
    - Response: {"answer": "string", "contexts": ["snippet1", "snippet2", ...]}
    
    **Rules:**
    - Returns 200 OK on success only
    - contexts must be array of plain strings
    - Answer must be concise and based only on retrieved text
    - If retrieval fails: answer = "Information not available in dataset."
    """
    
    # Check if RAG pipeline is initialized
    if rag_pipeline is None:
        return QueryResponse(
            answer="Information not available in dataset.",
            contexts=[]
        )
    
    # Validate query
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        # Execute RAG pipeline
        result = rag_pipeline.query(
            question=request.query,
            top_k=request.top_k
        )
        
        # Ensure result has required fields
        if not isinstance(result, dict):
            raise ValueError("Invalid pipeline result format")
        
        answer = result.get("answer", "Information not available in dataset.")
        contexts = result.get("contexts", [])
        
        # Ensure contexts is a list of strings
        if not isinstance(contexts, list):
            contexts = []
        
        # Convert all contexts to strings
        contexts = [str(ctx) for ctx in contexts]
        
        # Return in exact format required
        return QueryResponse(
            answer=answer,
            contexts=contexts
        )
        
    except Exception as e:
        print(f"Error processing query: {e}")
        import traceback
        traceback.print_exc()
        
        # Fail-safe: return graceful error as per requirements
        return QueryResponse(
            answer="Information not available in dataset.",
            contexts=[]
        )


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "MedInSight - Medical RAG API",
        "version": "1.0.0",
        "description": "AI Textbook Medical Reasoning using RAG",
        "submission": "Hack-A-Cure",
        "endpoints": {
            "health": "/health - Health check",
            "query": "/query - Main RAG query endpoint"
        },
        "status": "ready" if rag_pipeline else "vector_store_not_loaded"
    }


# ============ Main Entry Point ============

if __name__ == "__main__":
    # Get port from environment variable (default: 8000 for local, 10000 for production)
    port = int(os.getenv("PORT", 8000))
    
    print(f"\n🌐 Starting server on http://0.0.0.0:{port}")
    print(f"📖 API docs available at http://localhost:{port}/docs\n")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
