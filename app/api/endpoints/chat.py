from fastapi import APIRouter, Depends

from api.depends import get_chat_controller
from controllers.chat_controller import ChatController
from schemas.chat_request import ChatRequest
from schemas.chat_response import ChatResponse

router = APIRouter()


@router.post('/',
             response_model=ChatResponse,
             response_model_exclude_none=True,
             summary="Start a new chat",
             description=(
                 "Process a new chat request. "
                 "Takes user input, forwards it to the chat controller, and returns the AI's response."
             ))
async def chat(request: ChatRequest, chat_controller: ChatController = Depends(get_chat_controller),
               ) -> ChatResponse:
    try:
        response = chat_controller.process_chat(request)
        chat_controller.chat_repository.db.commit()
        return response
    except Exception as e:
        chat_controller.chat_repository.db.rollback()
        raise e
