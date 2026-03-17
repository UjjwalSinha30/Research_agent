from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
def auth_root():
    return {"message": "Auth endpoint"}