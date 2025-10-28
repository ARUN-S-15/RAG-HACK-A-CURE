"""Simplified ingestion script that uses a sample text corpus instead of large PDFs."""
import os
import pickle
import numpy as np
from openai import OpenAI
import faiss

VEC_DIR = "./vectorstore"
EMB_MODEL = "text-embedding-3-small"

# Sample medical knowledge base (simplified for demo)
SAMPLE_TEXTS = [
    "Diabetes is a chronic condition characterized by high blood sugar levels.",
    "The hallmark of diabetes is elevated glucose levels that result from defects in insulin secretion, insulin action, or both.",
    "Type 1 diabetes is caused by autoimmune destruction of pancreatic beta cells.",
    "Type 2 diabetes is associated with insulin resistance and relative insulin deficiency.",
    "Management of diabetes includes lifestyle modification and, when needed, pharmacotherapy to control blood glucose.",
    "Complications of diabetes can include cardiovascular disease, neuropathy, nephropathy, and retinopathy.",
    "Hypertension is defined as blood pressure consistently above 140/90 mmHg.",
    "Essential hypertension has no identifiable cause and accounts for 90-95% of cases.",
    "Secondary hypertension results from specific identifiable causes such as renal disease or endocrine disorders.",
    "Treatment of hypertension includes lifestyle changes and antihypertensive medications.",
    "Myocardial infarction (heart attack) occurs when blood flow to the heart muscle is blocked.",
    "Common symptoms of myocardial infarction include chest pain, shortness of breath, and diaphoresis.",
    "Stroke is caused by interruption of blood supply to the brain, leading to cell death.",
    "Ischemic stroke is caused by blocked blood vessels, while hemorrhagic stroke involves bleeding in the brain.",
    "Asthma is a chronic inflammatory disease of the airways characterized by reversible airflow obstruction.",
    "Symptoms of asthma include wheezing, coughing, chest tightness, and shortness of breath.",
    "Pneumonia is an infection of the lung parenchyma caused by bacteria, viruses, or fungi.",
    "Common bacterial causes of pneumonia include Streptococcus pneumoniae and Haemophilus influenzae.",
    "Chronic obstructive pulmonary disease (COPD) includes chronic bronchitis and emphysema.",
    "The primary risk factor for COPD is cigarette smoking.",
]


def chunk_texts(texts, chunk_size=200):
    """Simple chunking - each item is already a manageable chunk."""
    docs = []
    for i, text in enumerate(texts):
        docs.append({"text": text, "source": f"knowledge_base_{i}"})
    return docs


def main():
    print("Starting simplified ingest...")
    os.makedirs(VEC_DIR, exist_ok=True)
    
    docs = chunk_texts(SAMPLE_TEXTS)
    print(f"Prepared {len(docs)} document chunks")
    
    # Get OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required")
    
    print("Initializing OpenAI client...")
    client = OpenAI(api_key=api_key)
    
    # Create embeddings
    texts = [d["text"] for d in docs]
    print(f"Creating embeddings for {len(texts)} texts...")
    
    try:
        resp = client.embeddings.create(input=texts, model=EMB_MODEL)
        vectors = [item.embedding for item in resp.data]
        print(f"✓ Created {len(vectors)} embeddings")
    except Exception as e:
        print(f"Error creating embeddings: {e}")
        raise
    
    # Convert to numpy
    vectors = np.array(vectors, dtype="float32")
    dim = vectors.shape[1]
    print(f"Vector dimension: {dim}")
    
    # Build FAISS index
    print("Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    
    # Save
    print("Saving index and metadata...")
    faiss.write_index(index, os.path.join(VEC_DIR, "index.faiss"))
    with open(os.path.join(VEC_DIR, "metadata.pkl"), "wb") as f:
        pickle.dump(docs, f)
    
    print(f"✓ Successfully indexed {len(docs)} chunks into {VEC_DIR}")
    print(f"✓ Index file: {os.path.join(VEC_DIR, 'index.faiss')}")
    print(f"✓ Metadata file: {os.path.join(VEC_DIR, 'metadata.pkl')}")


if __name__ == "__main__":
    main()
