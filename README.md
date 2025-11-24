# RAG Interview Prep Application

A full-stack RAG (Retrieval-Augmented Generation) application designed to help users prepare for technical interviews (Java, SQL, DSA, GenAI). The system allows users to upload study materials (PDF, TXT, MD), asks questions, and receives AI-generated answers with citations.

## 🚀 Features

-   **Document Ingestion**: Upload and chunk PDF, TXT, and MD files.
-   **Vector Search**: Uses Google Gemini Embeddings (`text-embedding-004`) and ChromaDB for semantic search.
-   **RAG Pipeline**:
    -   **Query Rewriting**: Optimizes user queries for better retrieval.
    -   **Reranking**: Scores retrieved documents for relevance using Gemini.
    -   **Citations**: Provides source attribution for every answer.
-   **Analytics**: Tracks query latency, similarity scores, and rerank scores.
-   **Modern UI**: Dark-themed React + Vite frontend with Tailwind CSS.

## 🛠️ Tech Stack

-   **Backend**: FastAPI, Python 3.11
-   **Frontend**: React, Vite, Tailwind CSS
-   **Database**: ChromaDB (Vector Store)
-   **AI/LLM**: Google Gemini (`gemini-1.5-flash`, `text-embedding-004`)
-   **Containerization**: Docker, Docker Compose

## 🏗️ Architecture

```ascii
[User] -> [Frontend (React)] -> [Backend (FastAPI)]
                                      |
                                      v
                                [RAG Pipeline]
                               /      |       \
                              v       v        v
                        [Gemini] [ChromaDB] [Analytics]
```

## 🏃‍♂️ Setup Instructions

### Prerequisites

-   Docker & Docker Compose
-   Google Gemini API Key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rag-application
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run with Docker

```bash
docker compose up --build
```

-   **Frontend**: http://localhost:5173
-   **Backend API**: http://localhost:8000/docs

### 4. How to Use

1.  **Upload**: Go to the "Upload Documents" section and upload your interview prep PDFs.
2.  **Ask**: Type a question in the chat box (e.g., "Explain the difference between abstract class and interface in Java").
3.  **Analyze**: Check the "Analytics" panel to see how the system performed.

## 📈 Analytics

The system logs every query to `backend/analytics/records.jsonl`. The Analytics panel visualizes:
-   Query Latency
-   Top Rerank Scores
-   Question History

## 🔮 Future Improvements

-   Add user authentication.
-   Support for more file formats (DOCX, HTML).
-   Advanced analytics dashboard with charts.
-   Chat history persistence.
