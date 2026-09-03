import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "ResearchPilot"
    llm_api_key: str = os.getenv('LLM_API_KEY')
    model_name: str = os.getenv('MODEL_NAME')
    embedding_model: str = os.getenv('EMBEDDING_MODEL')
    vector_db_path: str = os.getenv('VECTOR_DB_PATH')

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
