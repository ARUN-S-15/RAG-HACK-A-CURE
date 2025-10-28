"""
Demo app that works without OpenAI API (uses mock embeddings).
Use this for testing the UI when you don't have API credits.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os

# Import mock RAG instead of real one
try:
    from rag_pipeline_mock import MockRAG as RAG
    USING_MOCK = True
except ImportError:
    from rag_pipeline import RAG
    USING_MOCK = False


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


app = FastAPI(title="MedInSight RAG API (Demo Mode)", version="1.0.0")

# Mount static files
if os.path.exists("./static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize RAG pipeline
rag = RAG(vectorstore_path="./vectorstore")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Redirect to chat interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/query" />
    </head>
    <body>
        <p>Redirecting to <a href="/query">MedInSight Chat</a>...</p>
    </body>
    </html>
    """


@app.get("/query", response_class=HTMLResponse)
async def chat_page():
    """Serve the chat interface"""
    chat_file = "./static/chat.html"
    if os.path.exists(chat_file):
        with open(chat_file, 'r') as f:
            content = f.read()
            # Add demo banner if using mock
            if USING_MOCK:
                banner = '''
                <div style="background: #fff3cd; color: #856404; padding: 10px; text-align: center; border-bottom: 2px solid #ffc107;">
                    ⚠️ DEMO MODE - Using mock embeddings (no OpenAI API). Add API credits for full functionality.
                </div>
                '''
                content = content.replace('<div class="container">', banner + '<div class="container">')
            return HTMLResponse(content=content)
    return HTMLResponse(content="<h1>Chat interface not found</h1>", status_code=404)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "mode": "mock" if USING_MOCK else "production"
    }


@app.post("/api/query")
async def api_query_endpoint(req: QueryRequest):
    """API endpoint for RAG queries"""
    if not req.query or not isinstance(req.query, str):
        raise HTTPException(status_code=400, detail="query must be a non-empty string")
    
    try:
        # Generate answer from RAG pipeline
        answer, contexts = rag.generate_answer(req.query, req.top_k)
        return {"answer": answer, "contexts": contexts}
    except Exception as e:
        # Fallback response
        return {
            "answer": "Information not available in dataset.",
            "contexts": []
        }


@app.post("/query")
async def query_endpoint(req: QueryRequest):
    """Legacy API endpoint (backward compatible)"""
    return await api_query_endpoint(req)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("\n" + "=" * 70)
    if USING_MOCK:
        print("⚠️  RUNNING IN DEMO MODE (Mock Embeddings)")
        print("   Add OpenAI API credits for full functionality")
    else:
        print("✅ RUNNING IN PRODUCTION MODE")
    print("=" * 70)
    print(f"\n🌐 Server starting on http://localhost:{port}")
    print(f"   Chat Interface: http://localhost:{port}/query")
    print(f"   API Endpoint:   http://localhost:{port}/api/query")
    print(f"   Health Check:   http://localhost:{port}/health")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run("app_demo:app", host="0.0.0.0", port=port, log_level="info")
