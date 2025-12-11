from sentence_transformers import SentenceTransformer
from .config import GENERATION_MODEL, EMBEDDING_MODEL, groq_client
from .file_ingestor import FileIngestor

class RAGPipeline:
    def __init__(self):
        self.ingestor = FileIngestor()
        self.model_name = GENERATION_MODEL
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def _generate(self, prompt: str) -> str:
        """Generate text using Groq API"""
        response = groq_client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content

    def rewrite_query(self, query: str) -> str:
        prompt = f"""Rewrite the following user query to be more suitable for semantic retrieval. 
        Keep it concise and focused on the technical concepts.
        Original Query: {query}
        Rewritten Query:"""
        return self._generate(prompt).strip()

    def retrieve(self, query: str, k: int = 5):
        query_embedding = self.embedding_model.encode(query).tolist()
        
        results = self.ingestor.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def rerank(self, query: str, documents: list) -> list:
        scored_docs = []
        for doc in documents:
            prompt = f"""Rate the relevance of the following document snippet to the query on a scale of 0 to 10.
            Return ONLY the number.
            
            Query: {query}
            Document: {doc}
            Score:"""
            try:
                response = self._generate(prompt)
                score = float(response.strip())
            except:
                score = 0.0
            scored_docs.append((doc, score))
        
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs

    def generate_answer(self, query: str, context_docs: list):
        context_text = "\n\n".join([f"Snippet {i+1}: {doc}" for i, doc in enumerate(context_docs)])
        
        prompt = f"""You are an expert technical interviewer. Answer the user's question using the provided context.
        You may infer the answer if it is reasonably supported by the text.
        If the answer is not in the context, say "I cannot answer this based on the provided documents."
        
        Context:
        {context_text}
        
        Question: {query}
        
        Answer:"""
        
        return self._generate(prompt)
