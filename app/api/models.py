from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class HealthResponse(BaseModel):
    status: str = Field(description="The health status of the API", json_schema_extra={"example": "healthy"})
    version: str = Field(description="The current version of the API", json_schema_extra={"example": "1.0.0"})

class ReportRequest(BaseModel):
    question: str = Field(description="The research question to be answered.", json_schema_extra={"example": "What are the core features of LangChain?"})

class ReportSource(BaseModel):
    title: str = Field(description="The title of the document or webpage.", json_schema_extra={"example": "Understanding LangChain"})
    url_or_id: str = Field(description="The URL or internal document identifier.", json_schema_extra={"example": "dummy.txt"})
    source_type: str = Field(description="The type of the source (e.g., 'document', 'web').", json_schema_extra={"example": "document"})
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Any additional metadata (e.g., snippet, page number).")

class ResearchReport(BaseModel):
    research_question: str = Field(description="The original question asked by the user.")
    executive_summary: str = Field(description="A brief, high-level summary of the findings.")
    key_findings: List[str] = Field(description="A bulleted list of 3-5 key findings.")
    sources: List[ReportSource] = Field(description="The list of sources used in the report, indexed to match the [id] citations.")
    limitations: str = Field(description="Any limitations or missing information in the gathered evidence. Must strictly describe gaps in evidence, not general ambiguity.")
    detailed_analysis: str = Field(description="A comprehensive analysis answering the user's question, citing sources using [id] notation.")
