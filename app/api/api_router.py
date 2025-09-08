from fastapi import APIRouter
from api.endpoints.utility import router as utility_router


router = APIRouter()

router.include_router(utility_router)
