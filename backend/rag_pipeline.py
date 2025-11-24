import google.generativeai as genai
from .config import GENERATION_MODEL, EMBEDDING_MODEL
from .file_ingestor import FileIngestor
import json

class RAGPipeline:
    def __init__(self):
        self.ingestor = FileIngestor()
        self.model = genai.GenerativeModel(GENERATION_MODEL)

    def rewrite_query(self, query: str) -> str:
        prompt = f"""Rewrite the following user query to be more suitable for semantic retrieval. 
        Keep it concise and focused on the technical concepts.
        Original Query: {query}
        Rewritten Query:"""
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def retrieve(self, query: str, k: int = 5):
        embedding_model = EMBEDDING_MODEL
        query_embedding = genai.embed_content(model=embedding_model,
                                            content=query,
                                            task_type="retrieval_query")["embedding"]
        
        results = self.ingestor.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def rerank(self, query: str, documents: list) -> list:
        # Simple LLM-based reranking
        scored_docs = []
        for doc in documents:
            prompt = f"""Rate the relevance of the following document snippet to the query on a scale of 0 to 10.
            Return ONLY the number.
            
            Query: {query}
            Document: {doc}
            Score:"""
            try:
                response = self.model.generate_content(prompt)
                score = float(response.text.strip())
            except:
                score = 0.0
            scored_docs.append((doc, score))
        
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs

    def generate_answer(self, query: str, context_docs: list):
        context_text = "\n\n".join([f"Snippet {i+1}: {doc}" for i, doc in enumerate(context_docs)])
        
        prompt = f"""You are an expert technical interviewer. Answer the user's question using ONLY the provided context.
        If the answer is not in the context, say "I cannot answer this based on the provided documents."
        
        Context:
        {context_text}
        
        Question: {query}
        
        Answer:"""
        
        response = self.model.generate_content(prompt)
        return response.text
