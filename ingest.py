"""
Document ingestion pipeline for RAG system.
Loads PDFs, chunks them, and creates embeddings.
"""

import os
from typing import List
from pathlib import Path
import pickle

from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def load_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error loading {pdf_path}: {e}")
            return ""
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size * 0.5:  # At least 50% of chunk size
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
            
        return [c for c in chunks if len(c) > 50]  # Filter out very small chunks
    
    def process_documents(self, pdf_dir: str) -> tuple:
        """Process all PDFs in a directory."""
        pdf_dir = Path(pdf_dir)
        all_chunks = []
        metadata = []
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            print(f"Processing {pdf_file.name}...")
            text = self.load_pdf(str(pdf_file))
            
            if text:
                chunks = self.chunk_text(text)
                print(f"  - Created {len(chunks)} chunks")
                
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    metadata.append({
                        'source': pdf_file.name,
                        'chunk_id': i,
                        'text': chunk
                    })
        
        print(f"\nTotal chunks: {len(all_chunks)}")
        return all_chunks, metadata
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for text chunks."""
        print("Creating embeddings...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings


class VectorStore:
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        self.index = None
        self.metadata = []
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def build_index(self, embeddings: np.ndarray, metadata: List[dict]):
        """Build FAISS index from embeddings."""
        self.metadata = metadata
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(embeddings.astype('float32'))
        
        print(f"Index built with {self.index.ntotal} vectors")
    
    def save(self, index_path: str = "vector_store/faiss.index", 
             metadata_path: str = "vector_store/metadata.pkl"):
        """Save index and metadata to disk."""
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        faiss.write_index(self.index, index_path)
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        
        print(f"Vector store saved to {index_path}")
    
    def load(self, index_path: str = "vector_store/faiss.index",
             metadata_path: str = "vector_store/metadata.pkl"):
        """Load index and metadata from disk."""
        self.index = faiss.read_index(index_path)
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        
        print(f"Vector store loaded with {self.index.ntotal} vectors")
    
    def search(self, query: str, k: int = 5) -> List[dict]:
        """Search for similar chunks."""
        # Create query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Get results with metadata
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['distance'] = float(distances[0][i])
                result['relevance_score'] = 1 / (1 + result['distance'])
                results.append(result)
        
        return results


def build_vector_store(pdf_dir: str = "Dataset"):
    """Main function to build the vector store from PDFs."""
    # Initialize processor
    processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
    
    # Process documents
    chunks, metadata = processor.process_documents(pdf_dir)
    
    # Create embeddings
    embeddings = processor.create_embeddings(chunks)
    
    # Build and save vector store
    vector_store = VectorStore()
    vector_store.build_index(embeddings, metadata)
    vector_store.save()
    
    print("\n✅ Vector store built successfully!")
    return vector_store


if __name__ == "__main__":
    build_vector_store()
