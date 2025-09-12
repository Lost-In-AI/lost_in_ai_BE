from services import prompts

from openai import OpenAI, APIError
from core.configs import settings
import time


class OpenAIService:
    def __init__(self):
        _api_key: str = settings.OPENAI_API_KEY
        self.model: str = "gpt-4.1-mini"
        self.client = OpenAI(api_key=_api_key)
        self.retries: int = 3

    def generate_response(self, prompt: list[dict], model: str = None, retries: int = None):
        for attempt in range(retries if retries else self.retries):
            try:
                return self.client.responses.create(model=model if model else self.model, input=prompt)
            except APIError as e:
                if e.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                raise
        raise Exception("OpenAI API failed after multiple retries")

    def generate_summary(self, request: dict, model: str = None, retries: int = None):
        prompt = prompts.summary + str(request)
        for attempt in range(retries if retries else self.retries):
            try:
                return self.client.responses.create(model=model if model else self.model, input=prompt)
            except APIError as e:
                if e.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                raise
        raise Exception("OpenAI API failed after multiple retries")

    def summary_builder(self, history: list[dict], summary: str):
        init = f"INIZIALIZZAZIONE: {prompts.summary}\n"

        history_prompt = f"STORICO: {history}\n" if history else ""

        summary_prompt = f"SUMMARY {summary}\n" if summary else ""

        return init + history_prompt + summary_prompt
