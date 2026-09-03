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
