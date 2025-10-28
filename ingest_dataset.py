"""
Optimized PDF ingestion for large medical textbook datasets.
Handles memory efficiently by processing PDFs in chunks and limiting embeddings.
"""
import os
import glob
import pickle
import numpy as np
from openai import OpenAI
import faiss
import fitz  # PyMuPDF
from tqdm import tqdm

# Configuration
DATASET_DIR = "./Dataset"  # Your large PDF folder
VEC_DIR = "./vectorstore"
EMB_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 800  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks
MAX_CHUNKS_PER_PDF = 500  # Limit chunks per PDF to avoid memory issues
BATCH_SIZE = 20  # Smaller batches for embeddings


def extract_text_from_pdf(pdf_path, max_pages=None):
    """Extract text from PDF with optional page limit."""
    try:
        doc = fitz.open(pdf_path)
        texts = []
        page_count = len(doc) if max_pages is None else min(len(doc), max_pages)
        
        for page_num in range(page_count):
            try:
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    texts.append(text)
            except Exception as e:
                print(f"  Warning: Error reading page {page_num}: {e}")
                continue
        
        doc.close()
        return "\n".join(texts)
    except Exception as e:
        print(f"  Error opening PDF: {e}")
        return ""


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    if not text or not text.strip():
        return []
    
    text = text.replace('\r', '\n')
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len and len(chunks) < MAX_CHUNKS_PER_PDF:
        end = min(start + chunk_size, text_len)
        
        # Try to break at sentence boundary
        if end < text_len:
            # Look for sentence end
            for punct in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
                last_punct = text.rfind(punct, start, end)
                if last_punct > start + chunk_size // 2:
                    end = last_punct + len(punct)
                    break
        
        chunk = text[start:end].strip()
        if len(chunk) > 50:  # Only keep substantial chunks
            chunks.append(chunk)
        
        start = end - overlap
        if start < 0:
            start = 0
    
    return chunks


def batch_iter(lst, n=BATCH_SIZE):
    """Yield successive n-sized batches from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    print("=" * 70)
    print("MedInSight - Dataset PDF Ingestion")
    print("=" * 70)
    
    os.makedirs(VEC_DIR, exist_ok=True)
    
    # Find PDFs
    pdf_files = glob.glob(os.path.join(DATASET_DIR, "*.pdf"))
    
    if not pdf_files:
        print(f"\n❌ No PDFs found in {DATASET_DIR}/")
        print(f"Please add PDF files to the Dataset folder.")
        return
    
    print(f"\n📂 Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        size_mb = os.path.getsize(pdf) / (1024 * 1024)
        print(f"  • {os.path.basename(pdf)} ({size_mb:.1f} MB)")
    
    # Get API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='sk-...'")
        return
    
    print(f"\n🔧 Configuration:")
    print(f"  • Chunk size: {CHUNK_SIZE} chars")
    print(f"  • Chunk overlap: {CHUNK_OVERLAP} chars")
    print(f"  • Max chunks per PDF: {MAX_CHUNKS_PER_PDF}")
    print(f"  • Embedding model: {EMB_MODEL}")
    print(f"  • Batch size: {BATCH_SIZE}")
    
    client = OpenAI(api_key=api_key)
    
    # Process PDFs
    all_docs = []
    print(f"\n📖 Processing PDFs...")
    
    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        print(f"\n  Processing: {pdf_name}")
        
        # Extract text
        print(f"    → Extracting text...")
        text = extract_text_from_pdf(pdf_path)
        
        if not text:
            print(f"    ⚠ No text extracted, skipping")
            continue
        
        print(f"    → Extracted {len(text):,} characters")
        
        # Chunk text
        print(f"    → Chunking...")
        chunks = chunk_text(text)
        print(f"    → Created {len(chunks)} chunks")
        
        # Store chunks with metadata
        for i, chunk in enumerate(chunks):
            all_docs.append({
                "text": chunk,
                "source": pdf_name,
                "chunk_id": i
            })
    
    if not all_docs:
        print("\n❌ No documents to index!")
        return
    
    print(f"\n✅ Total documents to embed: {len(all_docs):,}")
    
    # Create embeddings in batches
    print(f"\n🔄 Creating embeddings...")
    texts = [d["text"] for d in all_docs]
    vectors = []
    
    total_batches = (len(texts) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num, batch in enumerate(batch_iter(texts, BATCH_SIZE), 1):
        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} texts)...", end=' ')
        try:
            resp = client.embeddings.create(input=batch, model=EMB_MODEL)
            batch_vectors = [item.embedding for item in resp.data]
            vectors.extend(batch_vectors)
            print("✓")
        except Exception as e:
            print(f"\n  ❌ Error in batch {batch_num}: {e}")
            print(f"  Continuing with {len(vectors)} embeddings so far...")
            break
    
    if not vectors:
        print("\n❌ Failed to create any embeddings!")
        return
    
    print(f"\n✅ Created {len(vectors):,} embeddings")
    
    # Trim docs to match vectors if needed
    if len(vectors) < len(all_docs):
        print(f"  ⚠ Trimming documents from {len(all_docs)} to {len(vectors)}")
        all_docs = all_docs[:len(vectors)]
    
    # Build FAISS index
    print(f"\n🗄️  Building FAISS index...")
    vectors_array = np.array(vectors, dtype="float32")
    dim = vectors_array.shape[1]
    print(f"  Vector dimension: {dim}")
    
    index = faiss.IndexFlatL2(dim)
    index.add(vectors_array)
    print(f"  ✓ Added {index.ntotal:,} vectors to index")
    
    # Save
    print(f"\n💾 Saving to {VEC_DIR}/...")
    index_path = os.path.join(VEC_DIR, "index.faiss")
    meta_path = os.path.join(VEC_DIR, "metadata.pkl")
    
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(all_docs, f)
    
    print(f"  ✓ Index: {index_path}")
    print(f"  ✓ Metadata: {meta_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ INGESTION COMPLETE!")
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"  • PDFs processed: {len(pdf_files)}")
    print(f"  • Total chunks: {len(all_docs):,}")
    print(f"  • Index size: {os.path.getsize(index_path) / (1024*1024):.2f} MB")
    print(f"  • Metadata size: {os.path.getsize(meta_path) / (1024*1024):.2f} MB")
    print("\n🚀 Ready to start the server with: python app.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
