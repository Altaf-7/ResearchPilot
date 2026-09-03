from typing import Tuple, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from app.services.retrieval import RetrieverService
from app.api.models import SourceNode
from app.config import settings

class RAGService:
    def __init__(self, retriever_service: RetrieverService = None):
        self.retriever = retriever_service or RetrieverService()
        
        model_name = settings.model_name
        # Fallback in case user left the openai default in .env
        if "gpt" in model_name:
            model_name = "gemini-1.5-flash"
            
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=settings.llm_api_key,
            temperature=0.0
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent research assistant. 
Answer the user's question based strictly on the provided context below.
If the answer cannot be found in the context, clearly state that you don't know and do not invent information.

Context:
{context}
"""),
            ("user", "{question}")
        ])
        
        self.chain = self.prompt_template | self.llm
        
    def format_docs(self, docs: List[Document]) -> str:
        formatted = []
        for d in docs:
            formatted.append(f"Source: {d.metadata.get('source', 'unknown')} | Content: {d.page_content}")
        return "\n\n".join(formatted)

    def ask(self, question: str) -> Tuple[str, List[SourceNode]]:
        # 1. Retrieve context
        docs = self.retriever.retrieve(question)
        
        # 2. Format context
        context_text = self.format_docs(docs)
        
        # 3. Generate answer
        response = self.chain.invoke({
            "context": context_text,
            "question": question
        })
        
        # 4. Extract sources
        sources = []
        for d in docs:
            sources.append(SourceNode(
                filename=str(d.metadata.get("source", "unknown")),
                page=d.metadata.get("page", None),
                type=d.metadata.get("type", None),
                snippet=d.page_content[:200] + "..." # return a snippet for verification
            ))
            
        return response.content, sources
