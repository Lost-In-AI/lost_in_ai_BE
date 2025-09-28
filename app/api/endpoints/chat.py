from fastapi import APIRouter, Depends

from api.depends import get_chat_controller, get_current_user
from controllers.chat_controller import ChatController
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse
from schemas.patch_chat_request import PatchChatRequest
from schemas.patch_chat_response import PatchChatResponse
from services.clerk_service import ClerkToken

router = APIRouter()


@router.post('/', response_model=ChatResponse, response_model_exclude_none=True)
async def chat(request: ChatRequest, chat_controller: ChatController = Depends(get_chat_controller),
               token: ClerkToken = Depends(get_current_user)) -> ChatResponse:
    try:
        response = chat_controller.process_chat(request, token)
        chat_controller.chat_repository.db.commit()
        return response
    except Exception as e:
        chat_controller.chat_repository.db.rollback()
        raise e


@router.patch('/', response_model=PatchChatResponse, response_model_exclude_none=True)
async def chat(request: PatchChatRequest, chat_controller: ChatController = Depends(get_chat_controller)):
    try:
        return chat_controller.patch_chat(request)
    except Exception as e:
        raise e
