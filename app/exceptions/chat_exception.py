from fastapi import status


class ChatException(Exception):
    def __init__(self, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, detail: str = "Chat Exception"):
        self.status_code = status_code
        self.detail = detail


class BotResponseParsingError(ChatException):
    def __init__(self, message: str):
        error = "Error parsing bot response: " + str(message)
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=error
        )

class PlaceholdersParsingError(ChatException):
    def __init__(self, message: str):
        error = "Error parsing placeholders: " + str(message)
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=error
        )