from fastapi import APIRouter, UploadFile, BackgroundTasks, Depends, HTTPException
from app.core.security import get_current_user
from app.services.transcript_service import save_and_index, list_transcripts

router = APIRouter()


@router.post("/upload")
async def upload_transcript(file: UploadFile, background_tasks: BackgroundTasks, user_id: str = Depends(get_current_user)):
    if not file.filename.endswith((".txt", ".md")):
        raise HTTPException(status_code=400, detail="Only .txt or .md transcripts supported")
    # Save and index (indexing includes building vectorstore)
    transcript_id = await save_and_index(user_id, file)
    return {"transcript_id": transcript_id, "status": "indexed"}
    

@router.get("/")
async def list_user_transcripts(user_id: str = Depends(get_current_user)):
    return await list_transcripts(user_id)
