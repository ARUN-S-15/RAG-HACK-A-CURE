import os
import glob
import pickle
import numpy as np
from openai import OpenAI
import faiss
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

PDF_DIR = "./pdfs"
VEC_DIR = "./vectorstore"
EMB_MODEL = "text-embedding-3-small"  # Using smaller model to avoid memory issues


def ensure_sample_pdf(pdf_dir):
    os.makedirs(pdf_dir, exist_ok=True)
    sample_path = os.path.join(pdf_dir, "sample_diabetes.pdf")
    if os.path.exists(sample_path):
        return sample_path
    c = canvas.Canvas(sample_path, pagesize=letter)
    text = c.beginText(40, 700)
    lines = [
        "Diabetes is a chronic condition characterized by high blood sugar levels.",
        "The hallmark of diabetes is elevated glucose levels that result from defects in insulin secretion, insulin action, or both.",
        "Management includes lifestyle modification and, when needed, pharmacotherapy to control blood glucose.",
        "Complications can include cardiovascular disease, neuropathy, nephropathy, and retinopathy."
    ]
    for l in lines:
        text.textLine(l)
    c.drawText(text)
    c.save()
    return sample_path


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    return "\n".join(texts)


def chunk_text(text, chunk_size=1000, overlap=200):
    # Simple semantic-ish chunker using character windows with overlap
    text = text.replace('\r', '\n')
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def batch_iter(lst, n=50):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    print("Starting ingest...")
    os.makedirs(VEC_DIR, exist_ok=True)
    # Ensure a sample PDF exists if none provided
    os.makedirs(PDF_DIR, exist_ok=True)
    files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
    if not files:
        print("No PDFs found in ./pdfs/. Creating a sample PDF for testing...")
        sample = ensure_sample_pdf(PDF_DIR)
        files = [sample]
    
    print(f"Found {len(files)} PDF files")

    docs = []
    for p in files:
        print(f"Processing {p}...")
        text = extract_text_from_pdf(p)
        chunks = chunk_text(text)
        print(f"  Extracted {len(chunks)} chunks")
        for i, c in enumerate(chunks):
            docs.append({"text": c, "source": os.path.basename(p)})

    if not docs:
        print("No text extracted from PDFs. Exiting.")
        return
    
    print(f"Total docs to embed: {len(docs)}")

    # Batch embeddings
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required to run ingest.py")
    
    print("Initializing OpenAI client...")
    client = OpenAI(api_key=api_key)

    texts = [d["text"] for d in docs]
    vectors = []
    print(f"Embedding {len(texts)} texts in batches of 50...")
    for i, batch in enumerate(batch_iter(texts, n=50)):
        print(f"  Batch {i+1}...")
        resp = client.embeddings.create(input=batch, model=EMB_MODEL)
        vectors.extend([item.embedding for item in resp.data])

    print("Converting to numpy array...")
    vectors = np.array(vectors, dtype="float32")
    dim = vectors.shape[1]
    print(f"Vector dimension: {dim}")

    # Build FAISS index
    print("Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    # Save index and metadata
    print("Saving index and metadata...")
    faiss.write_index(index, os.path.join(VEC_DIR, "index.faiss"))
    pickle.dump(docs, open(os.path.join(VEC_DIR, "metadata.pkl"), "wb"))

    print(f"✓ Indexed {len(docs)} chunks into {VEC_DIR}")


if __name__ == "__main__":
    main()
