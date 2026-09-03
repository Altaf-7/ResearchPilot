from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AskRequest(BaseModel):
    question: str

class SourceNode(BaseModel):
    filename: str
    page: Optional[int] = None
    type: Optional[str] = None
    snippet: str

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceNode]

class ResearchRequest(BaseModel):
    question: str

class ResearchResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]] = []

# V3 Models
class AgentResearchRequest(BaseModel):
    question: str

class AgentResearchResponse(BaseModel):
    answer: str
    tools_used: List[Dict[str, Any]] = Field(default_factory=list)

# V4 Models
class ReportRequest(BaseModel):
    question: str

class ReportSource(BaseModel):
    title: str = Field(description="The title of the source (e.g., page title or document name)")
    url_or_id: str = Field(description="The URL or internal ID of the source")
    source_type: str = Field(description="Type of source, e.g., 'web' or 'document'")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context or metadata")

class ResearchReport(BaseModel):
    question: str = Field(description="The original research question")
    executive_summary: str = Field(description="A high-level summary of the research findings")
    key_findings: List[str] = Field(description="A list of 3-5 key findings supported by the evidence")
    detailed_analysis: str = Field(description="An in-depth analysis of the topic. Use citations like [1], [2] corresponding to the sources list.")
    sources: List[ReportSource] = Field(description="The list of sources used in the report. Must match the numbered citations in the analysis.")
    limitations: str = Field(description="List limitations strictly based on missing evidence. Do not mention general topic ambiguity.")
