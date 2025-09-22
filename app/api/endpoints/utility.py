from fastapi import APIRouter, HTTPException
from services.database import test_connection

router = APIRouter()

@router.get("/health")
async def health():
    return "Tutto bene!"

@router.get("/health/db")
async def health_db():
    ok = test_connection()
    if not ok:
        raise HTTPException(status_code=500, detail="Database connessione fallita")
    return {"status": "ok"}
