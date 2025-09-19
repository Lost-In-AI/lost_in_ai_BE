from fastapi import APIRouter, Depends

from api.depends import get_chat_controller
from controllers.chat_controller import ChatController
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse
from schemas.patch_chat_request import PatchChatRequest
from schemas.patch_chat_response import PatchChatResponse

router = APIRouter()


@router.post('/', response_model=ChatResponse, response_model_exclude_none=True)
async def chat(request: ChatRequest, chat_controller: ChatController = Depends(get_chat_controller)
               ) -> ChatResponse:
    try:
        return chat_controller.process_chat(request)
    except Exception as e:
        raise e


@router.patch('/', response_model=PatchChatResponse, response_model_exclude_none=True)
async def chat(request: PatchChatRequest, chat_controller: ChatController = Depends(get_chat_controller)):
    try:
        return chat_controller.patch_chat(request)
    except Exception as e:
        raise e
