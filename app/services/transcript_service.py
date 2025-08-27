import uuid
import asyncio
from fastapi import UploadFile
from app.utils.chunking import extract_blocks, blocks_to_documents
from app.services.vectorstore_service import VectorStoreService
from app.services.firestore_client import FirestoreClient


async def save_and_index(user_id: str, file: UploadFile) -> str:
    content = (await file.read()).decode("utf-8")
    transcript_id = str(uuid.uuid4())

    # Persist raw transcript under user
    await FirestoreClient.save_transcript(user_id, transcript_id, content)

    # Chunk + convert to LangChain Documents
    blocks = extract_blocks(content)
    docs = blocks_to_documents(blocks)

    # Save chunk metadata in Firestore for convenience
    chunks_meta = [
        {
            "start": d.metadata.get("start"),
            "end": d.metadata.get("end"),
            "text": d.page_content,
        }
        for d in docs
    ]

    # Run sync Firestore helper in a thread so it doesn’t block
    await asyncio.to_thread(
        FirestoreClient._save_chunks_sync, user_id, transcript_id, chunks_meta
    )

    # Index vectorstore for this user+transcript
    await VectorStoreService.index_transcript(user_id, transcript_id, chunks_meta)

    return transcript_id


async def list_transcripts(user_id: str):
    return await FirestoreClient.list_transcripts_for_user(user_id)
