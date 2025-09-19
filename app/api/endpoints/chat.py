from fastapi import APIRouter, Depends

from api.depends import get_chat_controller
from controllers.chat_controller import ChatController
from schemas.new_chat_request import NewChatRequest
from schemas.new_chat_response import NewChatResponse


router = APIRouter()


@router.post('/new', response_model=NewChatResponse, response_model_exclude_none=True)
async def chat(request: NewChatRequest, chat_controller: ChatController = Depends(get_chat_controller)
               ) -> NewChatResponse:
    try:
        return chat_controller.process_chat(request)
    except Exception as e:
        raise e
