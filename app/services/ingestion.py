import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.config import settings
from app.core.embeddings import get_embeddings

class DocumentIngestor:
    def __init__(self, docs_dir: str = "./data/documents", chroma_dir: str = "./data/chroma"):
        self.docs_dir = docs_dir
        self.chroma_dir = chroma_dir
        # Initialize Embeddings using our generic factory
        self.embeddings = get_embeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        # Ensure dirs exist
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.chroma_dir, exist_ok=True)

    def load_documents(self) -> List:
        docs = []
        for filename in os.listdir(self.docs_dir):
            file_path = os.path.join(self.docs_dir, filename)
            if not os.path.isfile(file_path):
                continue
                
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                docs.extend(loader.load())
            elif filename.endswith(".md"):
                # Using TextLoader instead of Unstructured for simplicity and less dependencies
                loader = TextLoader(file_path)
                loaded_docs = loader.load()
                for d in loaded_docs:
                    d.metadata["type"] = "markdown"
                docs.extend(loaded_docs)
            elif filename.endswith(".txt"):
                loader = TextLoader(file_path)
                loaded_docs = loader.load()
                for d in loaded_docs:
                    d.metadata["type"] = "text"
                docs.extend(loaded_docs)
            else:
                print(f"Skipping unsupported file: {filename}")
        
        # Clean metadata (Chroma doesn't like complex types)
        for doc in docs:
            doc.metadata["source"] = os.path.basename(doc.metadata.get("source", filename))
        
        return docs

    def process_and_store(self):
        print(f"Loading documents from {self.docs_dir}...")
        documents = self.load_documents()
        
        if not documents:
            print("No documents found. Skipping ingestion.")
            return

        print(f"Loaded {len(documents)} document pages/files.")
        print("Splitting into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks.")
        
        print("Generating embeddings and storing in ChromaDB...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.chroma_dir
        )
        print("Ingestion complete.")
        return vector_store
