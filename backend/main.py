from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import time
from .rag_pipeline import RAGPipeline
from .file_ingestor import FileIngestor
from .analytics import AnalyticsLogger
import logging
import traceback

# Configure logging
logging.basicConfig(filename='backend_error.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title="RAG Interview Prep API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGPipeline()
ingestor = FileIngestor()
analytics = AnalyticsLogger()

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        ingestor.ingest_file(file_path)
        return {"message": f"Successfully uploaded and ingested {file.filename}"}
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
def trigger_ingest():
    ingestor.ingest_directory(DATA_DIR)
    return {"message": "Ingestion complete"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    start_time = time.time()
    
    # 1. Rewrite
    rewritten_query = rag.rewrite_query(request.question)
    
    # 2. Retrieve
    retrieval_results = rag.retrieve(rewritten_query)
    documents = retrieval_results['documents'][0]
    metadatas = retrieval_results['metadatas'][0]
    distances = retrieval_results['distances'][0]
    
    # 3. Rerank
    reranked_results = rag.rerank(request.question, documents)
    top_docs = [doc for doc, score in reranked_results[:3]] # Top 3
    rerank_scores = [score for doc, score in reranked_results[:3]]
    
    # 4. Generate
    answer = rag.generate_answer(request.question, top_docs)
    
    latency = time.time() - start_time
    
    # Log analytics
    analytics.log_query({
        "question": request.question,
        "rewritten_query": rewritten_query,
        "answer": answer,
        "latency": latency,
        "similarity_scores": distances, # Note: Chroma returns distances (lower is better)
        "rerank_scores": rerank_scores
    })
    
    return {
        "answer": answer,
        "citations": [{"text": doc, "metadata": meta} for doc, meta in zip(top_docs, metadatas)], # Simplified mapping
        "scores": {
            "similarity": distances,
            "rerank": rerank_scores
        }
    }

@app.get("/analytics")
def get_analytics():
    return analytics.get_records()
