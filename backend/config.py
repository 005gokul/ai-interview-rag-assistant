import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Groq API for generation
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables")

groq_client = Groq(api_key=GROQ_API_KEY)

# Model Configurations
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Local embedding model (no API needed)
GENERATION_MODEL = "llama-3.3-70b-versatile"  # Groq model

# ChromaDB Configuration
CHROMA_DB_DIR = os.path.join(os.path.dirname(__file__), "data", "chroma_db")
COLLECTION_NAME = "interview_docs"
