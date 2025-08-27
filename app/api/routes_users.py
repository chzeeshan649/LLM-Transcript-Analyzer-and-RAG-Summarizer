from fastapi import APIRouter


router = APIRouter()


@router.get("/me")
def get_user_profile():
    return {"status": "ok", "message": "User profile stub"}