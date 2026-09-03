from fastapi import APIRouter, HTTPException
from app.api.models import AskRequest, AskResponse, ResearchRequest, ResearchResponse
from app.services.rag import RAGService
from app.services.research import ResearchService
from app.services.agent import AgentService

router = APIRouter()
rag_service = RAGService()
research_service = ResearchService()
agent_service = AgentService()

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

from app.api.models import AgentResearchRequest, AgentResearchResponse

@router.post("/v3/research", response_model=AgentResearchResponse)
async def perform_agent_research(request: AgentResearchRequest):
    try:
        answer, tools_used, _ = agent_service.research(request.question)
        return AgentResearchResponse(answer=answer, tools_used=tools_used)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.api.models import ReportRequest, ResearchReport
from app.services.report import ReportService
report_service = ReportService()

@router.post("/v4/report", response_model=ResearchReport)
async def generate_research_report(request: ReportRequest):
    try:
        report = report_service.generate_report(request.question)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
