import pytest
from unittest.mock import patch, MagicMock
from app.services.ingestion import DocumentIngestor
from langchain_core.documents import Document

@patch("app.services.ingestion.Chroma")
@patch("app.services.ingestion.GoogleGenerativeAIEmbeddings")
@patch("app.services.ingestion.PyPDFLoader")
@patch("app.services.ingestion.TextLoader")
@patch("os.listdir")
@patch("os.path.isfile")
def test_load_documents(mock_isfile, mock_listdir, mock_text_loader, mock_pdf_loader, mock_embeddings, mock_chroma):
    mock_listdir.return_value = ["test.pdf", "test.txt", "test.md"]
    mock_isfile.return_value = True
    
    mock_pdf_instance = MagicMock()
    mock_pdf_instance.load.return_value = [Document(page_content="pdf content", metadata={"source": "test.pdf", "page": 1})]
    mock_pdf_loader.return_value = mock_pdf_instance
    
    def mock_text_load_side_effect(filepath):
        filename = filepath.split("/")[-1].split("\\")[-1]
        mock_instance = MagicMock()
        mock_instance.load.return_value = [Document(page_content="text content", metadata={"source": filename})]
        return mock_instance
        
    mock_text_loader.side_effect = mock_text_load_side_effect
    
    ingestor = DocumentIngestor(docs_dir="/mock/dir", chroma_dir="/mock/chroma")
    
    docs = ingestor.load_documents()
    
    assert len(docs) == 3
    
    # Assert metadata was cleaned and added correctly
    pdf_doc = [d for d in docs if d.metadata.get("source") == "test.pdf"][0]
    txt_doc = [d for d in docs if d.metadata.get("source") == "test.txt" and d.metadata.get("type") == "text"][0]
    md_doc = [d for d in docs if d.metadata.get("source") == "test.md" and d.metadata.get("type") == "markdown"][0]
    
    assert pdf_doc.metadata["page"] == 1
    assert txt_doc.page_content == "text content"
    assert md_doc.page_content == "text content"
