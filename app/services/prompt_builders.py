from typing import List, Dict, Optional
from schemas.enums.message_sender import MessageSender
from schemas.message import Message


def prepare_prompt(
    init_text: str,
    current_message: str,
    history_messages: List[Message] | None = None,
    summary_text: Optional[str] = None,
) -> List[Dict]:

    messages: List[Dict] = [prepare_message(MessageSender.SYSTEM, init_text.strip())]

    if summary_text:
        messages.append(prepare_message(MessageSender.ASSISTANT, summary_text.strip()))

    if history_messages:
        for message in history_messages:
            messages.append(prepare_message(message.sender,  message.text))

    messages.append(prepare_message(MessageSender.USER, current_message))

    return messages


def prepare_message(role: MessageSender, text: str):
    if role == MessageSender.USER:
        role = "user"
        text_type = "input_text"
    elif role == MessageSender.ASSISTANT:
        role = "assistant"
        text_type = "output_text"
    else:
        role = "system"
        text_type = "input_text"

    return {
        "role": role,
        "content": [{"type": text_type, "text": text}]
    }
