from fastapi import APIRouter, Depends

from api.depends import get_chat_controller
from controllers.chat_controller import ChatController
from schemas.new_chat_request import NewChatRequest
from schemas.new_chat_response import NewChatResponse


router = APIRouter()


@router.post('/chat', response_model=NewChatResponse)
async def test_chat(request: NewChatRequest, chat_controller: ChatController = Depends(get_chat_controller)
                    ) -> NewChatResponse:
    return chat_controller.mock_response(request)
