from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import get_current_user
from app.services.rag_service import answer_query, get_history

router = APIRouter()


class QueryPayload(BaseModel):
    transcript_id: str
    question: str
    k: int = 4
    use_cache: bool = True


@router.post("/ask")
async def ask(payload: QueryPayload, user_id: str = Depends(get_current_user)):
    return await answer_query(user_id, payload.transcript_id, payload.question, top_k=payload.k, use_cache=payload.use_cache)


@router.get("/history/{transcript_id}")
async def history(transcript_id: str, user_id: str = Depends(get_current_user)):
    return await get_history(user_id, transcript_id)
