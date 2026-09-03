import logging
from app.config import settings

logger = logging.getLogger(__name__)

def get_embeddings():
    """
    Factory function to instantiate Embeddings using HuggingFace Inference API.
    """
    from langchain_huggingface import HuggingFaceEndpointEmbeddings
    
    hf_token = settings.hf_token
    if not hf_token:
        raise ValueError("HF_TOKEN is missing in environment variables. It is required for embeddings.")
        
    embeddings = HuggingFaceEndpointEmbeddings(
        model=settings.embedding_model,
        huggingfacehub_api_token=hf_token
    )
    
    return embeddings
