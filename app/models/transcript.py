from pydantic import BaseModel
from typing import List


class TranscriptChunk(BaseModel):
    start: str
    end: str
    text: str
    embedding: List[float]