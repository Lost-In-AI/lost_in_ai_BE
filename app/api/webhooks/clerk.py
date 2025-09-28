from fastapi import Depends
from fastapi import APIRouter, Request

from api.depends import get_webhook_controller
from controllers.webhook_controller import WebhookController

router = APIRouter()


@router.post('/new-user',
             summary="Clerk new user webhook",
             description=(
                 "Endpoint to handle incoming **Clerk webhook events** for new user creation."
                 "Clerk calls this endpoint whenever a new user is registered in the system."
                 "The request body contains the event payload from Clerk, which is passed to the webhook controller."
             )
)
async def clerk_webhook(request: Request, webhook_controller: WebhookController = Depends(get_webhook_controller)):
    try:
        return await webhook_controller.handle_event(request)

    except Exception as e:
        raise e
