from fastapi import APIRouter, HTTPException
from services.database import test_connection

router = APIRouter()

@router.get("/health")
async def health():
    return "Tutto bene!"
