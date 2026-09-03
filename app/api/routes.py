import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.api.models import ReportRequest, ResearchReport, HealthResponse
from app.services.report import ReportService
from app.services.ingestion import DocumentIngestor
import os
import shutil

logger = logging.getLogger(__name__)
router = APIRouter()
report_service = ReportService()
ingestor = DocumentIngestor()

@router.delete("/api/clear")
async def clear_data():
    """
    Clears all uploaded documents and resets the ChromaDB vector storage.
    """
    try:
        # Clear documents
        if os.path.exists(ingestor.docs_dir):
            shutil.rmtree(ingestor.docs_dir)
        os.makedirs(ingestor.docs_dir, exist_ok=True)
        
        # Clear Chroma collections natively to avoid Windows file lock (WinError 32)
        import chromadb
        client = chromadb.PersistentClient(path=ingestor.chroma_dir)
        for collection in client.list_collections():
            client.delete_collection(name=collection.name)
            
        logger.info("Successfully cleared data directories and vector db.")
        return {"status": "success", "message": "All proprietary data and vector indexes have been cleared."}
    except Exception as e:
        logger.error(f"Failed to clear data: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear data.")

@router.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a document to the server and automatically ingests it into ChromaDB.
    """
    allowed_extensions = [".pdf", ".txt", ".md"]
    if not any(file.filename.endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and Markdown files are supported.")
        
    try:
        os.makedirs(ingestor.docs_dir, exist_ok=True)
        file_path = os.path.join(ingestor.docs_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"File {file.filename} saved to {file_path}. Starting ingestion...")
        ingestor.process_and_store(specific_filename=file.filename)
        logger.info(f"File {file.filename} successfully ingested.")
        
        return {"status": "success", "message": f"File {file.filename} uploaded and ingested successfully."}
    except Exception as e:
        logger.error(f"Error uploading file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return HealthResponse(status="healthy", version="1.0.0")

@router.post("/api/research", response_model=ResearchReport)
async def generate_research_report(request: ReportRequest):
    """
    Generates a citation-backed research report using autonomous agents.
    """
    logger.info(f"Received research request: {request.question}")
    try:
        report = report_service.generate_report(request.question)
        logger.info("Successfully generated research report.")
        return report
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
