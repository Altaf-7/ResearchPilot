from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.project_name,
    description="AI Research & Intelligence Assistant",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.project_name
    }
