from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from duckduckgo_search import DDGS

# 1. Provider Abstraction
class WebSearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search the web and return normalized results (title, url, snippet)."""
        pass

# 2. Concrete Implementation
class DuckDuckGoProvider(WebSearchProvider):
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        try:
            with DDGS() as ddgs:
                raw_results = list(ddgs.text(query, max_results=max_results))
                
            normalized = []
            for r in raw_results:
                normalized.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "source": "DuckDuckGo"
                })
            return normalized
        except Exception as e:
            # We must not raise an exception, otherwise the agent enters an infinite retry loop.
            # Instead, we return an empty list or print the error.
            print(f"Web search exception: {e}")
            return []

# 3. Tool Schema
class WebSearchInput(BaseModel):
    query: str = Field(description="The precise search query to look up on the internet.")

# 4. LangChain Tool
# We instantiate a default provider for the tool to use.
_default_provider = DuckDuckGoProvider()

@tool("web_search", args_schema=WebSearchInput)
def web_search_tool(query: str) -> str:
    """
    Search the internet for current events, facts, or information not found in your training data or context.
    Use this tool when the user asks a question about the real world that requires up-to-date knowledge.
    Do NOT use this tool if the user is asking about a specific internal document or PDF, unless you need external context.
    """
    import json
    results = _default_provider.search(query)
    if not results:
        return "Search failed. No data available. Do not retry the search. Tell the user you don't have this information."
    return json.dumps(results)
