"""
Document Ingestion Pipeline for MedInSight
Loads PDFs from ./pdfs/ directory, chunks them, and creates FAISS vector store
Uses OpenAI text-embedding-3-large for embeddings
"""

import os
from typing import List, Dict, Tuple
from pathlib import Path
import pickle
from dotenv import load_dotenv

# PDF extraction libraries
try:
    import fitz  # PyMuPDF
    PDF_LIBRARY = "pymupdf"
except ImportError:
    try:
        import pdfplumber
        PDF_LIBRARY = "pdfplumber"
    except ImportError:
        from PyPDF2 import PdfReader
        PDF_LIBRARY = "pypdf2"

import faiss
import numpy as np
import openai

# Load environment variables
load_dotenv()


class DocumentProcessor:
    """
    Processes PDF documents: extraction, semantic chunking with overlap
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = int(os.getenv("CHUNK_SIZE", chunk_size))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", chunk_overlap))
        self.use_fallback = False
        self.fallback_model = None
        
        # Initialize OpenAI for embeddings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key and self.openai_api_key != "your_openai_api_key_here":
            openai.api_key = self.openai_api_key
        else:
            print("⚠️  WARNING: OPENAI_API_KEY not found or not set in .env file!")
            print("   Using fallback embedding model (sentence-transformers)")
            # Fallback to sentence-transformers if OpenAI not available
            try:
                from sentence_transformers import SentenceTransformer
                self.fallback_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.use_fallback = True
            except Exception as e:
                raise ValueError(f"No embedding model available. Please set OPENAI_API_KEY or install sentence-transformers: {e}")
        
    def load_pdf_pymupdf(self, pdf_path: str) -> str:
        """Extract text using PyMuPDF (best for tables and diagrams)"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            return text
        except Exception as e:
            print(f"Error with PyMuPDF for {pdf_path}: {e}")
            return ""
    
    def load_pdf_pdfplumber(self, pdf_path: str) -> str:
        """Extract text using pdfplumber"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error with pdfplumber for {pdf_path}: {e}")
            return ""
    
    def load_pdf_pypdf2(self, pdf_path: str) -> str:
        """Extract text using PyPDF2 (fallback)"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error with PyPDF2 for {pdf_path}: {e}")
            return ""
    
    def load_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using available library"""
        if PDF_LIBRARY == "pymupdf":
            return self.load_pdf_pymupdf(pdf_path)
        elif PDF_LIBRARY == "pdfplumber":
            return self.load_pdf_pdfplumber(pdf_path)
        else:
            return self.load_pdf_pypdf2(pdf_path)
    
    def chunk_text_semantic(self, text: str) -> List[str]:
        """
        Split text into meaningful chunks with overlap
        Tries to split at sentence boundaries for semantic coherence
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            chunk = text[start:end]
            
            # Try to break at sentence boundary if not at end
            if end < text_length:
                # Look for sentence endings
                last_period = chunk.rfind('. ')
                last_newline = chunk.rfind('\n\n')
                last_question = chunk.rfind('? ')
                last_exclamation = chunk.rfind('! ')
                
                break_point = max(last_period, last_newline, last_question, last_exclamation)
                
                # Only break if we're past 60% of chunk size
                if break_point > self.chunk_size * 0.6:
                    chunk = chunk[:break_point + 2]
                    end = start + break_point + 2
            
            chunk = chunk.strip()
            if len(chunk) > 50:  # Filter out very small chunks
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            
        return chunks
    
    def process_documents(self, pdf_dir: str = "./pdfs/") -> Tuple[List[str], List[Dict]]:
        """Process all PDFs in directory"""
        pdf_path = Path(pdf_dir)
        
        # Create directory if it doesn't exist
        if not pdf_path.exists():
            print(f"📁 Creating {pdf_dir} directory...")
            pdf_path.mkdir(parents=True, exist_ok=True)
            print(f"⚠️  No PDF files found. Please add PDFs to {pdf_dir}")
            return [], []
        
        all_chunks = []
        metadata = []
        
        pdf_files = list(pdf_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"⚠️  No PDF files found in {pdf_dir}")
            print("   Adding placeholder content for testing...")
            # Add placeholder content
            placeholder_chunks = [
                "Diabetes is a chronic metabolic disease characterized by elevated levels of blood glucose (or blood sugar), which leads over time to serious damage to the heart, blood vessels, eyes, kidneys, and nerves.",
                "The hallmark of diabetes is elevated glucose levels in the blood. This condition can result from the body's inability to produce insulin, use insulin effectively, or both.",
                "Heart disease refers to several types of heart conditions. The most common type is coronary artery disease, which can lead to heart attack.",
                "Hypertension, or high blood pressure, is a condition in which the force of the blood against the artery walls is too high. It can lead to serious health complications and increase the risk of heart disease.",
                "Cancer is a disease in which some of the body's cells grow uncontrollably and spread to other parts of the body. It can start almost anywhere in the human body."
            ]
            all_chunks = placeholder_chunks
            metadata = [
                {"source": "placeholder.pdf", "chunk_id": i, "text": chunk}
                for i, chunk in enumerate(placeholder_chunks)
            ]
            print(f"   Added {len(placeholder_chunks)} placeholder chunks")
            return all_chunks, metadata
        
        print(f"📚 Found {len(pdf_files)} PDF file(s) in {pdf_dir}")
        print(f"📖 Using {PDF_LIBRARY.upper()} for PDF extraction")
        print()
        
        for pdf_file in pdf_files:
            print(f"Processing: {pdf_file.name}")
            text = self.load_pdf(str(pdf_file))
            
            if text:
                chunks = self.chunk_text_semantic(text)
                print(f"  ✓ Created {len(chunks)} chunks")
                
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    metadata.append({
                        'source': pdf_file.name,
                        'chunk_id': i,
                        'text': chunk
                    })
            else:
                print(f"  ✗ No text extracted")
        
        print(f"\n📊 Total chunks created: {len(all_chunks)}")
        return all_chunks, metadata
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings using OpenAI text-embedding-3-large"""
        # Use fallback model if OpenAI not configured
        if self.use_fallback or not self.openai_api_key or self.openai_api_key == "your_openai_api_key_here":
            print("📊 Using fallback embedding model (sentence-transformers)")
            if self.fallback_model is None:
                from sentence_transformers import SentenceTransformer
                self.fallback_model = SentenceTransformer('all-MiniLM-L6-v2')
            return self.fallback_model.encode(texts, show_progress_bar=True)
        
        print("🔄 Creating embeddings with OpenAI text-embedding-3-large...")
        print(f"   Processing {len(texts)} chunks...")
        
        embeddings = []
        batch_size = 100  # Process in batches for efficiency
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            print(f"   Batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            
            try:
                response = openai.Embedding.create(
                    model="text-embedding-3-large",
                    input=batch
                )
                
                batch_embeddings = [item['embedding'] for item in response['data']]
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                print(f"   Error creating embeddings: {e}")
                print("   Falling back to sentence-transformers")
                if not hasattr(self, 'fallback_model'):
                    from sentence_transformers import SentenceTransformer
                    self.fallback_model = SentenceTransformer('all-MiniLM-L6-v2')
                return self.fallback_model.encode(texts, show_progress_bar=True)
        
        return np.array(embeddings)


class VectorStore:
    """
    FAISS-based vector store for similarity search
    """
    
    def __init__(self, embedding_dim: int = None):
        # OpenAI text-embedding-3-large has 3072 dimensions
        # Fallback model has 384 dimensions
        self.embedding_dim = embedding_dim or 3072
        self.index = None
        self.metadata = []
        self.processor = None
        
    def build_index(self, embeddings: np.ndarray, metadata: List[Dict]):
        """Build FAISS index from embeddings"""
        # Auto-detect embedding dimension
        if embeddings.shape[1] != self.embedding_dim:
            self.embedding_dim = embeddings.shape[1]
            print(f"📐 Auto-detected embedding dimension: {self.embedding_dim}")
        
        self.metadata = metadata
        
        # Create FAISS index (L2 distance)
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(embeddings.astype('float32'))
        
        print(f"✅ FAISS index built with {self.index.ntotal} vectors")
    
    def save(self, index_path: str = "./vectorstore/faiss.index", 
             metadata_path: str = "./vectorstore/metadata.pkl"):
        """Save index and metadata to ./vectorstore/"""
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        faiss.write_index(self.index, index_path)
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        
        print(f"💾 Vector store saved to {index_path}")
        print(f"💾 Metadata saved to {metadata_path}")
    
    def load(self, index_path: str = "./vectorstore/faiss.index",
             metadata_path: str = "./vectorstore/metadata.pkl") -> bool:
        """Load index and metadata from disk"""
        try:
            if not os.path.exists(index_path) or not os.path.exists(metadata_path):
                print(f"⚠️  Vector store not found at {index_path}")
                return False
            
            self.index = faiss.read_index(index_path)
            with open(metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            
            # Detect embedding dimension from loaded index
            self.embedding_dim = self.index.d
            
            print(f"✅ Vector store loaded: {self.index.ntotal} vectors, dim={self.embedding_dim}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
            return False
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar chunks using FAISS"""
        if self.index is None:
            print("⚠️  Index not loaded")
            return []
        
        # Initialize processor if not already done
        if self.processor is None:
            self.processor = DocumentProcessor()
        
        # Create query embedding
        try:
            if self.processor.openai_api_key and not getattr(self.processor, 'use_fallback', False):
                # Use OpenAI
                response = openai.Embedding.create(
                    model="text-embedding-3-large",
                    input=[query]
                )
                query_embedding = np.array([response['data'][0]['embedding']])
            else:
                # Use fallback
                query_embedding = self.processor.fallback_model.encode([query])
        except:
            # Fallback
            if not hasattr(self.processor, 'fallback_model'):
                from sentence_transformers import SentenceTransformer
                self.processor.fallback_model = SentenceTransformer('all-MiniLM-L6-v2')
            query_embedding = self.processor.fallback_model.encode([query])
        
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


def build_vector_store(pdf_dir: str = "./pdfs/"):
    """
    Main function to build the vector store from PDFs.
    
    Args:
        pdf_dir: Directory containing PDF files (default: ./pdfs/)
    """
    print("=" * 60)
    print("🏗️  Building Vector Store for MedInSight")
    print("=" * 60)
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # Process documents
    chunks, metadata = processor.process_documents(pdf_dir)
    
    if not chunks:
        print("❌ No chunks created. Please add PDF files to ./pdfs/")
        return None
    
    # Create embeddings
    embeddings = processor.create_embeddings(chunks)
    
    # Build and save vector store
    vector_store = VectorStore()
    vector_store.build_index(embeddings, metadata)
    vector_store.save()
    
    print("=" * 60)
    print("✅ Vector store built successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start the API server: python app.py")
    print("2. Test with: curl -X POST http://localhost:8000/query \\")
    print("              -H 'Content-Type: application/json' \\")
    print("              -d '{\"query\": \"What is diabetes?\", \"top_k\": 2}'")
    print()
    
    return vector_store


if __name__ == "__main__":
    build_vector_store()

