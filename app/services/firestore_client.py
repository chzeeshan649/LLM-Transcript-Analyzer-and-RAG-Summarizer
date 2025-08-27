import asyncio
import os
from typing import Optional, List, Dict, Any
from google.cloud import firestore
from google.auth import exceptions
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class FirestoreClient:
    _client: Optional[firestore.Client] = None

    @classmethod
    def _client_sync(cls) -> firestore.Client:
        if cls._client is None:
            # Ensure GOOGLE_APPLICATION_CREDENTIALS is set from .env
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not credentials_path or not os.path.exists(credentials_path):
                raise exceptions.DefaultCredentialsError(
                    f"GOOGLE_APPLICATION_CREDENTIALS not set or file not found: {credentials_path}"
                )
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

            cls._client = firestore.Client()
        return cls._client

    # ---- Sync helpers (private) ----
    @classmethod
    def _save_transcript_sync(cls, user_id: str, transcript_id: str, content: str):
        client = cls._client_sync()
        client.collection("users").document(user_id).collection("transcripts").document(transcript_id).set({
            "content": content
        })

    @classmethod
    def _get_transcript_sync(cls, user_id: str, transcript_id: str) -> Optional[Dict[str, Any]]:
        client = cls._client_sync()
        doc = client.collection("users").document(user_id).collection("transcripts").document(transcript_id).get()
        return doc.to_dict() if doc.exists else None

    @classmethod
    def _save_chunks_sync(cls, user_id: str, transcript_id: str, chunks: List[Dict[str, Any]]):
        client = cls._client_sync()
        client.collection("users").document(user_id).collection("transcripts").document(transcript_id).collection("chunks").document("index").set({
            "chunks": chunks
        })

    @classmethod
    def _get_chunks_sync(cls, user_id: str, transcript_id: str) -> Optional[List[Dict[str, Any]]]:
        client = cls._client_sync()
        doc = client.collection("users").document(user_id).collection("transcripts").document(transcript_id).collection("chunks").document("index").get()
        return doc.to_dict().get("chunks") if doc.exists else None

    @classmethod
    def _save_query_sync(cls, user_id: str, transcript_id: str, payload: Dict[str, Any]):
        client = cls._client_sync()
        client.collection("users").document(user_id).collection("transcripts").document(transcript_id).collection("queries").add(payload)

    @classmethod
    def _list_transcripts_sync(cls, user_id: str) -> List[Dict[str, Any]]:
        client = cls._client_sync()
        docs = client.collection("users").document(user_id).collection("transcripts").stream()
        return [d.to_dict() for d in docs]

    # ---- Async wrappers (call these from async code) ----
    @classmethod
    async def save_transcript(cls, user_id: str, transcript_id: str, content: str):
        await asyncio.to_thread(cls._save_transcript_sync, user_id, transcript_id, content)

    @classmethod
    async def get_transcript(cls, user_id: str, transcript_id: str):
        return await asyncio.to_thread(cls._get_transcript_sync, user_id, transcript_id)

    @classmethod
    async def save_chunks(cls, user_id: str, transcript_id: str, chunks: List[Dict[str, Any]]):
        await asyncio.to_thread(cls._save_chunks_sync, user_id, transcript_id, chunks)

    @classmethod
    async def get_chunks(cls, user_id: str, transcript_id: str):
        return await asyncio.to_thread(cls._get_chunks_sync, user_id, transcript_id)

    @classmethod
    async def save_query(cls, user_id: str, transcript_id: str, payload: Dict[str, Any]):
        await asyncio.to_thread(cls._save_query_sync, user_id, transcript_id, payload)

    @classmethod
    async def list_transcripts_for_user(cls, user_id: str) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(cls._list_transcripts_sync, user_id)
