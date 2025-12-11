import os
import glob
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from .config import CHROMA_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL

class LocalEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
    
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        return self.model.encode(input).tolist()

class FileIngestor:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.embedding_fn = LocalEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_fn
        )

    def extract_text(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def ingest_file(self, file_path: str):
        text = self.extract_text(file_path)
        chunks = self.chunk_text(text)
        filename = os.path.basename(file_path)
        
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        print(f"Ingested {len(chunks)} chunks from {filename}")

    def ingest_directory(self, directory_path: str):
        files = []
        for ext in ['*.pdf', '*.txt', '*.md']:
            files.extend(glob.glob(os.path.join(directory_path, ext)))
        
        for file_path in files:
            try:
                self.ingest_file(file_path)
            except Exception as e:
                print(f"Error ingesting {file_path}: {e}")
