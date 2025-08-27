import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    FIRESTORE_PROJECT: str = os.getenv("FIRESTORE_PROJECT", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    VECTORSTORE_BACKEND: str = os.getenv("VECTORSTORE_BACKEND", "faiss")  # faiss | chroma
    EMBEDDINGS_BACKEND: str = os.getenv("EMBEDDINGS_BACKEND", "openai")  # openai | huggingface
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    OPENAI_EMBED_MODEL: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    OPENAI_CHAT_MODEL: str = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")

    class Config:
        env_file = ".env"

settings = Settings()
