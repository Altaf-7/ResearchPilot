from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from app.services.retrieval import RetrieverService

class DocumentSearchInput(BaseModel):
    query: str = Field(description="The precise search query to look up in the internal documents.")

# We instantiate a default retriever for the tool to use.
# Note: we need to pass db_manager if our retrieval service requires it. 
# But wait, RetrieverService currently requires `chroma_dir`. It defaults to "./data/chroma".
_default_retriever = RetrieverService()

@tool("document_search", args_schema=DocumentSearchInput)
def document_search_tool(query: str) -> str:
    """
    Search the internal knowledge base for documents, policies, or proprietary data.
    Use this tool when the user asks a question about specific files or internal context.
    """
    docs = _default_retriever.retrieve(query)
    if not docs:
        return "No relevant documents found in the internal knowledge base."
        
    formatted = []
    for d in docs:
        source = d.metadata.get("source", "unknown")
        formatted.append(f"Source: {source} | Content: {d.page_content}")
        
    return "\n\n".join(formatted)
