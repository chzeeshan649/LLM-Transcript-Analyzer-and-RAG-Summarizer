from app.core.config import settings
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings_model():
    if settings.EMBEDDINGS_BACKEND and settings.EMBEDDINGS_BACKEND.lower() == "huggingface":
        # Hugging Face model for embeddings
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # OpenAI embeddings
    return OpenAIEmbeddings(
        model=settings.OPENAI_EMBED_MODEL,
        api_key=settings.OPENAI_API_KEY
    )
