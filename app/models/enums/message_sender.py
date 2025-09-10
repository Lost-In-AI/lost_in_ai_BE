from enum import Enum


class MessageSender(str, Enum):
    USER = 'user'
    BOT = 'bot'
