import os
from typing import List, Dict, Any
from app.core.config import settings
from app.services.embeddings_service import get_embeddings_model

# Try to import FAISS from langchain, fallback to community
try:
    from langchain.vectorstores import FAISS
except Exception:
    from langchain_community.vectorstores import FAISS

class VectorStoreService:
    _in_memory_cache = {}

    @staticmethod
    async def index_transcript(user_id: str, transcript_id: str, chunks: List[Dict[str, Any]]):
        embedder = get_embeddings_model()
        texts = []
        metadatas = []
        for c in chunks:
            text = c.get("text") if isinstance(c, dict) else getattr(c, "text", "")
            md = {"start": c.get("start") if isinstance(c, dict) else getattr(c, "start", None),
                  "end": c.get("end") if isinstance(c, dict) else getattr(c, "end", None)}
            texts.append(text)
            metadatas.append(md)

        vs = FAISS.from_texts(texts, embedding=embedder, metadatas=metadatas)

        base = os.path.join(settings.DATA_DIR, user_id, transcript_id)
        os.makedirs(base, exist_ok=True)
        try:
            vs.save_local(base)
        except Exception:
            try:
                FAISS.save_local(vs, base)
            except Exception:
                pass

        VectorStoreService._in_memory_cache[(user_id, transcript_id)] = vs
        return vs

    @staticmethod
    def _get_disk_path(user_id: str, transcript_id: str) -> str:
        return os.path.join(settings.DATA_DIR, user_id, transcript_id)

    @staticmethod
    async def get_retriever(user_id: str, transcript_id: str, k: int = 4):
        key = (user_id, transcript_id)
        vs = VectorStoreService._in_memory_cache.get(key)
        if not vs:
            base = VectorStoreService._get_disk_path(user_id, transcript_id)
            embedder = get_embeddings_model()
            try:
                vs = FAISS.load_local(base, embedder, allow_dangerous_deserialization=True)
            except Exception:
                raise ValueError(f"Vectorstore not found for user {user_id}, transcript {transcript_id} at {base}")
            VectorStoreService._in_memory_cache[key] = vs

        return vs.as_retriever(search_kwargs={"k": k})
