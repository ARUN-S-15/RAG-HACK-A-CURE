"""
RAG Query Engine - Retrieval and Generation logic
"""

import os
from typing import List, Dict
from dotenv import load_dotenv

from ingest import VectorStore

# Load environment variables
load_dotenv()


class RAGEngine:
    def __init__(self, use_local_model: bool = False):
        self.vector_store = VectorStore()
        self.vector_store.load()
        self.use_local_model = use_local_model or os.getenv("USE_LOCAL_MODEL", "false").lower() == "true"
        
        if not self.use_local_model:
            try:
                import openai
                self.openai_api_key = os.getenv("OPENAI_API_KEY")
                if not self.openai_api_key:
                    print("⚠️  No OpenAI API key found. Falling back to local model.")
                    self.use_local_model = True
                else:
                    self.client = openai.OpenAI(api_key=self.openai_api_key)
            except ImportError:
                print("⚠️  OpenAI package not available. Using local model.")
                self.use_local_model = True
    
    def retrieve_context(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve relevant chunks from vector store."""
        return self.vector_store.search(query, k=k)
    
    def generate_answer_openai(self, query: str, context: List[Dict]) -> Dict:
        """Generate answer using OpenAI GPT."""
        # Prepare context text
        context_text = "\n\n".join([
            f"Source: {doc['source']}\n{doc['text']}" 
            for doc in context
        ])
        
        # Create prompt
        prompt = f"""You are a helpful medical AI assistant. Use the following context to answer the user's question accurately and concisely.

Context:
{context_text}

Question: {query}

Instructions:
- Answer based on the provided context
- If the context doesn't contain enough information, say so
- Be precise and professional
- Cite the source documents when possible

Answer:"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": [{"source": doc['source'], "relevance": doc['relevance_score']} for doc in context],
                "model": "gpt-3.5-turbo"
            }
        except Exception as e:
            print(f"Error with OpenAI: {e}")
            return self.generate_answer_local(query, context)
    
    def generate_answer_local(self, query: str, context: List[Dict]) -> Dict:
        """Generate answer using local model (extractive QA)."""
        # For a simple implementation, we'll return the most relevant chunks
        # In production, you could use a local LLM like LLaMA or Mistral
        
        answer_parts = []
        for i, doc in enumerate(context[:3], 1):
            answer_parts.append(f"[From {doc['source']}]\n{doc['text'][:300]}...")
        
        answer = "\n\n".join(answer_parts)
        answer += "\n\n💡 Note: Using extractive mode. For better answers, configure an OpenAI API key."
        
        return {
            "answer": answer,
            "sources": [{"source": doc['source'], "relevance": doc['relevance_score']} for doc in context],
            "model": "extractive"
        }
    
    def query(self, question: str, k: int = 5) -> Dict:
        """Main query function - retrieves context and generates answer."""
        # Retrieve relevant chunks
        context = self.retrieve_context(question, k=k)
        
        if not context:
            return {
                "answer": "I couldn't find any relevant information in the knowledge base.",
                "sources": [],
                "model": "none"
            }
        
        # Generate answer
        if self.use_local_model:
            result = self.generate_answer_local(question, context)
        else:
            result = self.generate_answer_openai(question, context)
        
        return result


# CLI for testing
if __name__ == "__main__":
    print("🚀 Initializing RAG Engine...")
    rag = RAGEngine()
    
    print("\n✅ RAG Engine ready! Type 'exit' to quit.\n")
    
    while True:
        query = input("💬 Ask a question: ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            break
        
        if not query:
            continue
        
        print("\n🔍 Searching knowledge base...")
        result = rag.query(query)
        
        print(f"\n📝 Answer ({result['model']}):")
        print(result['answer'])
        
        print(f"\n📚 Sources:")
        for source in result['sources']:
            print(f"  - {source['source']} (relevance: {source['relevance']:.2f})")
        
        print("\n" + "-"*80 + "\n")
