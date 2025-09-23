from fastapi import APIRouter
from api.webhooks.clerk import router


webhook = APIRouter()

webhook.include_router(router)
