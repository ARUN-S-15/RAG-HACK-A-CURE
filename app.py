from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from rag_pipeline import RAG

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

app = FastAPI(title="MedInSight RAG API", version="1.0.0")

# Mount static files directory
if os.path.exists("./static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize RAG pipeline (loads vectorstore if available)
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
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Chat interface not found</h1>", status_code=404)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/api/query")
async def api_query_endpoint(req: QueryRequest):
    """API endpoint for RAG queries"""
    if not req.query or not isinstance(req.query, str):
        raise HTTPException(status_code=400, detail="query must be a non-empty string")
    # Generate answer from RAG pipeline
    answer, contexts = rag.generate_answer(req.query, req.top_k)
    # Always return 200 OK on success path
    return {"answer": answer, "contexts": contexts}


# Keep backward compatibility - POST /query still works
@app.post("/query")
async def query_endpoint(req: QueryRequest):
    """Legacy API endpoint (backward compatible)"""
    return await api_query_endpoint(req)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info")
