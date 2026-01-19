from fastapi import APIRouter, Depends
from app.core.auth import verify_token
from app.engines.ip_engine import run

router = APIRouter()

@router.post("/")
def ip_lookup(payload: dict, _: str = Depends(verify_token)):
    return run(payload)
