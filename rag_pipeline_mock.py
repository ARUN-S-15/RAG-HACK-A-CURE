"""
Mock RAG pipeline that works without OpenAI API.
For demo/testing when you don't have API credits.
"""
import os
import pickle
import re
import numpy as np
import faiss


class MockRAG:
    """RAG pipeline using mock embeddings (no OpenAI API needed)."""

    def __init__(self, vectorstore_path="./vectorstore"):
        self.vs_path = vectorstore_path
        self.index_file = os.path.join(self.vs_path, "index.faiss")
        self.meta_file = os.path.join(self.vs_path, "metadata.pkl")
        self.index = None
        self.metadata = []
        self.dim = 1536
        self._load_vectorstore()

    def _load_vectorstore(self):
        if not os.path.exists(self.index_file) or not os.path.exists(self.meta_file):
            self.index = None
            self.metadata = []
            self.dim = None
            return
        try:
            self.metadata = pickle.load(open(self.meta_file, "rb"))
        except Exception:
            self.metadata = []
        try:
            self.index = faiss.read_index(self.index_file)
            self.dim = self.index.d
        except Exception:
            self.index = None
            self.dim = None

    def _mock_embed(self, text):
        """Generate mock embedding from text hash."""
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(self.dim).astype('float32')
        return embedding / np.linalg.norm(embedding)

    def similarity_search(self, query, top_k=5):
        """Return top_k text snippets using mock embeddings."""
        if self.index is None or not self.metadata:
            return []
        
        q_vec = np.array([self._mock_embed(query)], dtype='float32')
        D, I = self.index.search(q_vec, top_k)
        
        results = []
        for idx in I[0]:
            if idx < 0 or idx >= len(self.metadata):
                continue
            results.append(self.metadata[idx]["text"])
        return results

    def generate_answer(self, query, top_k=5):
        """Generate answer using keyword matching (no LLM)."""
        contexts = self.similarity_search(query, top_k)
        contexts = contexts[:top_k]
        
        if not contexts:
            return "Information not available in dataset.", []

        # Simple keyword-based answer generation
        query_lower = query.lower()
        
        # Find the most relevant context by keyword matching
        best_context = contexts[0] if contexts else ""
        
        # Generate a simple answer by extracting the first sentence
        sentences = best_context.split('.')
        answer = sentences[0].strip() + '.' if sentences else best_context
        
        # Add citation
        answer += " [1]"
        
        return answer, contexts
