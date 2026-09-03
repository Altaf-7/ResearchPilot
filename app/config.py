from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "ResearchPilot"
    llm_api_key: str = ""
    model_name: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    vector_db_path: str = "./data/chroma"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
