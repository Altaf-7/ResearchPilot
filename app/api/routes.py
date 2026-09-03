from fastapi import APIRouter, HTTPException
from app.api.models import AskRequest, AskResponse, ResearchRequest, ResearchResponse
from app.services.rag import RAGService
from app.services.research import ResearchService

router = APIRouter()
rag_service = RAGService()
research_service = ResearchService()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    try:
        answer, sources = rag_service.ask(request.question)
        return AskResponse(
            answer=answer,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):
    try:
        answer, sources = research_service.research(request.question)
        return ResearchResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
