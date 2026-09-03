import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "ResearchPilot"
    
    # LLM Config
    llm_provider: str = os.getenv('LLM_PROVIDER', 'gemini')
    llm_api_key: str = os.getenv('LLM_API_KEY', '')
    model_name: str = os.getenv('MODEL_NAME', 'gemini-3.5-flash')
    
    # Embeddings Config
    hf_token: str = os.getenv('HF_TOKEN', '')
    embedding_model: str = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    
    # DB
    vector_db_path: str = os.getenv('VECTOR_DB_PATH', './data/chroma')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
