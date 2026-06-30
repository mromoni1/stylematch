from fastapi import APIRouter
from pydantic import BaseModel

from lib.supabase import get_client

router = APIRouter(prefix="/auth")


class UserUpsert(BaseModel):
    google_id: str
    email: str


@router.post("/users")
def upsert_user(body: UserUpsert):
    db = get_client()
    result = (
        db.table("users")
        .upsert({"google_id": body.google_id, "email": body.email}, on_conflict="google_id")
        .execute()
    )
    return result.data[0]
