"""
Fallback ingestion without OpenAI API - uses mock embeddings for demo.
Use this when you don't have OpenAI API credits.
"""
import os
import pickle
import numpy as np
import faiss

VEC_DIR = "./vectorstore"

# Sample medical knowledge base
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


def generate_mock_embeddings(texts, dim=1536):
    """Generate consistent mock embeddings using text hashing."""
    np.random.seed(42)  # For reproducibility
    embeddings = []
    
    for text in texts:
        # Create a deterministic embedding based on text hash
        text_hash = hash(text)
        np.random.seed(text_hash % (2**32))
        embedding = np.random.randn(dim).astype('float32')
        # Normalize
        embedding = embedding / np.linalg.norm(embedding)
        embeddings.append(embedding)
    
    return np.array(embeddings, dtype='float32')


def main():
    print("=" * 70)
    print("MedInSight - Mock Ingestion (No OpenAI API Required)")
    print("=" * 70)
    print("\n⚠️  This uses mock embeddings for demonstration purposes.")
    print("For production, you need a valid OpenAI API key with credits.\n")
    
    os.makedirs(VEC_DIR, exist_ok=True)
    
    # Prepare documents
    docs = []
    for i, text in enumerate(SAMPLE_TEXTS):
        docs.append({
            "text": text,
            "source": f"medical_knowledge_{i}",
            "chunk_id": i
        })
    
    print(f"📚 Prepared {len(docs)} document chunks")
    
    # Generate mock embeddings
    print(f"🔄 Generating mock embeddings (dimension: 1536)...")
    vectors = generate_mock_embeddings([d["text"] for d in docs])
    dim = vectors.shape[1]
    print(f"✅ Created {len(vectors)} mock embeddings")
    
    # Build FAISS index
    print(f"\n🗄️  Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    print(f"  ✓ Added {index.ntotal:,} vectors to index")
    
    # Save
    print(f"\n💾 Saving to {VEC_DIR}/...")
    index_path = os.path.join(VEC_DIR, "index.faiss")
    meta_path = os.path.join(VEC_DIR, "metadata.pkl")
    
    faiss.write_index(index, index_path)
    with open(meta_path, "wb") as f:
        pickle.dump(docs, f)
    
    print(f"  ✓ Index: {index_path}")
    print(f"  ✓ Metadata: {meta_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ MOCK INGESTION COMPLETE!")
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"  • Total chunks: {len(docs):,}")
    print(f"  • Index size: {os.path.getsize(index_path) / 1024:.2f} KB")
    print(f"  • Metadata size: {os.path.getsize(meta_path) / 1024:.2f} KB")
    print("\n⚠️  NOTE: This uses MOCK embeddings!")
    print("   The chat will work, but retrieval quality will be limited.")
    print("   For production, add OpenAI API credits and run:")
    print("   python ingest_simple.py")
    print("\n🚀 Ready to start the server with: python app.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
