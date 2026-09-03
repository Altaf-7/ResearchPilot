from fastapi import FastAPI
from app.config import settings
from app.api.routes import router as api_router

app = FastAPI(
    title=settings.project_name,
    description="AI Research & Intelligence Assistant",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.project_name
    }
