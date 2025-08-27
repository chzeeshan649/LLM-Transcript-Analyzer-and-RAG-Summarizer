from pydantic import BaseModel
from typing import List, Dict


class QueryRequest(BaseModel):
    transcript_id: str
    question: str


class QueryResponse(BaseModel):
    answer: str
    timestamps: List[Dict[str, str]]
    source_chunks: List[str]