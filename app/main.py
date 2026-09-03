import logging
from fastapi import FastAPI
from app.api.routes import router

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager
import shutil
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("ResearchPilot API is starting up...")
    
    # 1. Clear Documents
    docs_dir = "data/documents"
    if os.path.exists(docs_dir):
        try:
            shutil.rmtree(docs_dir)
            logger.info(f"Cleared {docs_dir} directory on startup.")
        except Exception as e:
            logger.warning(f"Could not clear {docs_dir}: {e}")
    os.makedirs(docs_dir, exist_ok=True)
    
    # 2. Clear Chroma collections natively to avoid Windows file lock issues
    chroma_dir = "data/chroma"
    if os.path.exists(chroma_dir):
        try:
            import chromadb
            client = chromadb.PersistentClient(path=chroma_dir)
            for collection in client.list_collections():
                client.delete_collection(name=collection.name)
            logger.info("Cleared ChromaDB collections on startup.")
        except Exception as e:
            logger.warning(f"Could not clear ChromaDB collections: {e}")
            
    yield
    logger.info("ResearchPilot API is shutting down...")

app = FastAPI(
    title="ResearchPilot API",
    description="An autonomous AI agent for citation-backed research and RAG.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)
