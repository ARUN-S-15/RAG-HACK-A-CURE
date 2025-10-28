"""
RAG Pipeline - Retrieval and Generation Logic
MedInSight - AI Textbook Medical Reasoning using RAG
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline for medical question answering.
    Uses FAISS for retrieval and GPT-4 for generation.
    """
    
    def __init__(self, vector_store):
        """
        Initialize RAG pipeline.
        
        Args:
            vector_store: FAISS vector store instance
        """
        self.vector_store = vector_store
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client
        openai.api_key = self.openai_api_key
    
    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieve relevant context from vector store.
        
        Args:
            query: User's question
            top_k: Number of documents to retrieve
            
        Returns:
            List of text snippets (contexts)
        """
        try:
            results = self.vector_store.search(query, k=top_k)
            
            # Extract text snippets
            contexts = []
            for result in results:
                if isinstance(result, dict) and 'text' in result:
                    contexts.append(result['text'])
                elif isinstance(result, str):
                    contexts.append(result)
            
            return contexts
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []
    
    def generate(self, query: str, contexts: List[str]) -> str:
        """
        Generate answer using GPT-4 based on retrieved contexts.
        Implements anti-hallucination by grounding answer strictly in contexts.
        
        Args:
            query: User's question
            contexts: Retrieved text snippets
            
        Returns:
            Generated answer (concise and grounded)
        """
        if not contexts:
            return "Information not available in dataset."
        
        # Build context string
        context_text = "\n\n".join([
            f"[Context {i+1}]\n{ctx}" 
            for i, ctx in enumerate(contexts)
        ])
        
        # Create prompt with strict grounding instructions
        system_prompt = """You are MedInSight, a medical AI assistant that provides accurate information strictly based on medical textbooks.

CRITICAL RULES:
1. Answer ONLY using information from the provided contexts
2. If the answer is not in the contexts, respond with: "Information not available in dataset."
3. Be concise and medically accurate
4. Do NOT add information from your training data
5. Quote or paraphrase from the contexts directly
6. Keep responses focused and brief (2-4 sentences when possible)"""

        user_prompt = f"""Question: {query}

Contexts from medical textbooks:
{context_text}

Based ONLY on the above contexts, provide a concise and accurate answer. If the information is not available in the contexts, respond with "Information not available in dataset."

Answer:"""

        try:
            # Call OpenAI API (GPT-4)
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Using GPT-4 as specified (gpt-5 not available yet)
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for factual accuracy
                max_tokens=500,   # Keep answers concise
                timeout=50        # Ensure response within 60 seconds total
            )
            
            answer = response.choices[0].message.content.strip()
            return answer
            
        except Exception as e:
            print(f"Error during generation: {e}")
            return "Information not available in dataset."
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Complete RAG pipeline: retrieve + generate.
        
        Args:
            question: User's medical question
            top_k: Number of contexts to retrieve
            
        Returns:
            Dictionary with 'answer' and 'contexts' keys
        """
        # Step 1: Retrieve relevant contexts
        contexts = self.retrieve(question, top_k=top_k)
        
        # Step 2: Generate answer grounded in contexts
        answer = self.generate(question, contexts)
        
        # Step 3: Return in required format
        return {
            "answer": answer,
            "contexts": contexts[:top_k]  # Ensure we return exactly top_k contexts
        }
