from openai import OpenAI, APIError
from core.configs import settings
import time


class OpenAIService:
    def __init__(self):
        _api_key: str = settings.OPENAI_API_KEY
        self.model: str = "gpt-4.1-nano"
        self.client = OpenAI(api_key=_api_key)
        self.retries: int = 3

    def generate_response(self, prompt: str, model: str = None, retries: int = None):
        for attempt in range(retries if retries else self.retries):
            try:
                return self.client.responses.create(model=model if model else self.model, input=prompt)
            except APIError as e:
                if e.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                raise
        raise Exception("OpenAI API failed after multiple retries")
