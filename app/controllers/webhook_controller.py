from fastapi import status, Request, Response
from svix.webhooks import Webhook, WebhookVerificationError

from controllers.user_controller import UserController
from core.configs import settings


class WebhookController:
    def __init__(self, user_controller: UserController):
        self.CLERK_WEBHOOK_SECRET = settings.CLERK_WEBHOOK_SECRET
        self.webhook = Webhook(self.CLERK_WEBHOOK_SECRET)
        self.user_controller = user_controller


    async def handle_event(self, request: Request):
        try:
            event_payload = await request.body()
            svix_id = request.headers.get("svix-id")
            svix_timestamp = request.headers.get("svix-timestamp")
            svix_signature = request.headers.get("svix-signature")

            if not (svix_id and svix_timestamp and svix_signature):
                return None  # TODO

            event = self.webhook.verify(event_payload, {
                "svix-id": svix_id,
                "svix-timestamp": svix_timestamp,
                "svix-signature": svix_signature,
            })

            event_type = event.get("type")
            data = event.get("data", {})

            if event_type == "user.created":
                return self.user_controller.create_user(data)
            else:
                return None

        except WebhookVerificationError as e:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content=f"Invalid signature: {e}")
