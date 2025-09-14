from fastapi import APIRouter
from api.endpoints.utility import router as utility_router
from api.endpoints.chat import router as chat_router
from api.endpoints.test import router as test_router


router = APIRouter()

router.include_router(utility_router)
router.include_router(test_router, prefix='/test')
router.include_router(chat_router, prefix='/chat')
