from fastapi import Header, HTTPException

async def get_current_user(user_id: str = Header(None, convert_underscores=False)):
    """
    Minimal auth shim — expects header 'user-id'.
    Replace with JWT/OAuth in production.
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID required in header 'user-id'")
    return user_id
