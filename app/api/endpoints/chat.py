from fastapi import APIRouter, Depends

from api.depends import get_chat_controller
from controllers.chat_controller import ChatController
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse


router = APIRouter()


@router.post('/', response_model=ChatResponse, response_model_exclude_none=True)
async def test_chat(request: ChatRequest, chat_controller: ChatController = Depends(get_chat_controller)
                    ) -> ChatResponse:
    return chat_controller.new_chatbot(request)
