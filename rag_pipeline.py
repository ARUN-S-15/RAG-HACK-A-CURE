import os
import pickle
import re
import numpy as np
from openai import OpenAI
import faiss

class RAG:
    """RAG pipeline: loads FAISS index + metadata and provides similarity_search and generate_answer.

    - Embeddings: text-embedding-3-large
    - Retriever: similarity_search(top_k)
    - LLM: gpt-4o (using gpt-4o as gpt-5 is not yet available)
    """

    def __init__(self, vectorstore_path="./vectorstore", openai_api_key_env="OPENAI_API_KEY"):
        self.client = OpenAI(api_key=os.environ.get(openai_api_key_env))
        self.vs_path = vectorstore_path
        self.index_file = os.path.join(self.vs_path, "index.faiss")
        self.meta_file = os.path.join(self.vs_path, "metadata.pkl")
        self.emb_model = "text-embedding-3-small"  # Using smaller model to avoid memory issues
        self.llm_model = "gpt-4o"
        self.index = None
        self.metadata = []
        self.dim = None
        self._load_vectorstore()

    def _load_vectorstore(self):
        if not os.path.exists(self.index_file) or not os.path.exists(self.meta_file):
            # Not yet ingested
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

    def _embed(self, texts):
        """Call OpenAI embeddings in batch. Returns list of vectors."""
        if not texts:
            return []
        resp = self.client.embeddings.create(input=texts, model=self.emb_model)
        return [d.embedding for d in resp.data]

    def similarity_search(self, query, top_k=5):
        """Return top_k text snippets (strings) for query using FAISS similarity search.
        If vectorstore is missing or empty, returns empty list.
        """
        if self.index is None or not self.metadata:
            return []
        q_vec = np.array(self._embed([query]), dtype='float32')
        # Guard: if embedding failed
        if q_vec.size == 0:
            return []
        D, I = self.index.search(q_vec, top_k)
        results = []
        for idx in I[0]:
            if idx < 0 or idx >= len(self.metadata):
                continue
            # metadata stored as dict with 'text'
            results.append(self.metadata[idx]["text"])
        return results

    def generate_answer(self, query, top_k=5):
        """Retrieve contexts and generate a concise answer strictly grounded in them.

        Returns (answer_string, contexts_list)
        """
        contexts = self.similarity_search(query, top_k)
        contexts = contexts[:top_k]
        if not contexts:
            return "Information not available in dataset.", []

        # Build prompt that forces grounding and quoting of snippets
        system_msg = (
            "You are a medical assistant. Answer concisely and ONLY using the provided context snippets.\n"
            "Do NOT hallucinate or invent facts. If the answer cannot be determined from the contexts, respond exactly: Information not available in dataset.\n"
            "When you provide an answer, include bracketed citations to the context snippets you used (e.g. [1] or [1,2]).\n"
            "The final answer must be a single concise paragraph no longer than ~2-3 sentences.\n"
        )

        user_msg = "Here are the retrieved contexts:\n\n"
        for i, c in enumerate(contexts, start=1):
            # keep snippets as plain text
            user_msg += f"Context [{i}]:\n{c}\n\n"
        user_msg += f"Question: {query}\n\nAnswer:" 

        # Call OpenAI chat completion (gpt-4o) with temperature 0 for determinism
        try:
            resp = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
                max_tokens=200,
                temperature=0,
            )
        except Exception as e:
            # On any LLM error, fall back to fail-safe
            return "Information not available in dataset.", contexts

        answer = resp.choices[0].message.content.strip()

        # Safety check: ensure answer references contexts with bracketed indices OR is explicit fail-safe
        if "Information not available in dataset." in answer:
            return "Information not available in dataset.", contexts

        if not re.search(r"\[\d+(,\s*\d+)*\]", answer):
            # If LLM didn't include explicit bracketed citations, fail safe to avoid hallucination
            return "Information not available in dataset.", contexts

        # Trim contexts to top_k plain strings
        return answer, contexts
