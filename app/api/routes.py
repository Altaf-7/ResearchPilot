import logging
from fastapi import APIRouter, HTTPException
from app.api.models import ReportRequest, ResearchReport, HealthResponse
from app.services.report import ReportService

logger = logging.getLogger(__name__)
router = APIRouter()
report_service = ReportService()

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
