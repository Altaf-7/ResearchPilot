from typing import List
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings

class RetrieverService:
    def __init__(self, chroma_dir: str = "./data/chroma", k: int = 4):
        self.chroma_dir = chroma_dir
        self.k = k
        
        embedding_model = settings.embedding_model
        if "text-embedding-3" in embedding_model or "embedding-001" in embedding_model:
            embedding_model = "models/gemini-embedding-001"
            
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=embedding_model,
            google_api_key=settings.llm_api_key
        )
        
        self.vector_store = Chroma(
            persist_directory=self.chroma_dir,
            embedding_function=self.embeddings
        )

    def retrieve(self, query: str) -> List:
        """Retrieve top k relevant chunks for the given query."""
        docs = self.vector_store.similarity_search(query, k=self.k)
        return docs
