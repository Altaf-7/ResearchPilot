from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.services.retrieval import RetrieverService

class DocumentSearchInput(BaseModel):
    query: str = Field(description="The precise search query to look up in the internal documents.")

@tool("document_search", args_schema=DocumentSearchInput)
def document_search_tool(query: str) -> str:
    """
    Search the internal knowledge base for documents, policies, or proprietary data.
    Use this tool when the user asks a question about specific files or internal context.
    """
    retriever = RetrieverService()
    try:
        docs = retriever.retrieve(query)
    except Exception as e:
        print(f"RAG search exception: {e}")
        docs = []
        
    if not docs:
        return "Search failed or no relevant documents found in the internal knowledge base. DO NOT retry this search tool."
        
    formatted = []
    for d in docs:
        source = d.metadata.get("source", "unknown")
        formatted.append(f"Source: {source} | Content: {d.page_content}")
        
    return "\n\n".join(formatted)
