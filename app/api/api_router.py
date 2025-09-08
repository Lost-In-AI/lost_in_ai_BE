from fastapi import APIRouter
from app.api.endpoints.utility import router as utility_router


router = APIRouter()

router.include_router(utility_router)
