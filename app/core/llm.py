import logging
from app.config import settings

logger = logging.getLogger(__name__)

def get_llm(tools=None):
    """
    Factory function to instantiate the correct LLM based on settings.llm_provider.
    """
    provider = settings.llm_provider.lower().strip()
    
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=settings.model_name, 
            google_api_key=settings.llm_api_key,
            temperature=0
        )
    elif provider == "groq":
        from langchain_groq import ChatGroq
        llm = ChatGroq(
            model=settings.model_name,
            api_key=settings.llm_api_key,
            temperature=0
        )
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model=settings.model_name,
            api_key=settings.llm_api_key,
            temperature=0
        )
    elif provider == "anthropic" or provider == "claude":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(
            model=settings.model_name,
            api_key=settings.llm_api_key,
            temperature=0
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    
    if tools:
        llm = llm.bind_tools(tools)
        
    return llm
