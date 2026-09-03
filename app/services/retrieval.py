from typing import List
from langchain.schema import Document
from chromadb.api.models.Collection import Collection
from app.config import settings
from app.core.embeddings import get_embeddings
from langchain_chroma import Chroma

class RetrieverService:
    def __init__(self, chroma_dir: str = "./data/chroma", k: int = 4):
        self.chroma_dir = chroma_dir
        self.k = k
        self.embeddings = get_embeddings()
        
        self.vector_store = Chroma(
            persist_directory=self.chroma_dir,
            embedding_function=self.embeddings
        )

    def retrieve(self, query: str) -> List:
        """Retrieve top k relevant chunks for the given query."""
        docs = self.vector_store.similarity_search(query, k=self.k)
        return docs
