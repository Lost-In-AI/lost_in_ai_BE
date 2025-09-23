from fastapi import Depends
from fastapi import APIRouter, Request

from api.depends import get_webhook_controller
from controllers.webhook_controller import WebhookController

router = APIRouter()


@router.post('/new-user',)
async def clerk_webhook(request: Request, webhook_controller: WebhookController = Depends(get_webhook_controller)):
    try:
        return await webhook_controller.handle_event(request)

    except Exception as e:
        raise e
