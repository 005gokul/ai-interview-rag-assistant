@echo off
echo Starting RAG Application Locally...

:: Check if .env exists
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
)

:: Setup Backend
echo Setting up Backend...
pip install -r backend/requirements.txt
start "RAG Backend" cmd /k "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001"

:: Setup Frontend
echo Setting up Frontend...
cd frontend
call npm install
start "RAG Frontend" cmd /k "npm run dev"

echo.
echo Application started!
echo Backend running at http://localhost:8001
echo Frontend running at http://localhost:5173
pause
