import json
import os

import openai

import config
from classes.file_manager import FileManager
from classes.resources_paths import AI_PROMPTS_PATH
from .enums import GPTRole, GPTModel


class GPTMessage:

    def __init__(self, prompt: str, message_list: list[dict[str, str]] | None = None):
        self._prompt_name = prompt
        self.message_list = self._init_message() if message_list is None else message_list

    def _init_message(self) -> list[dict[str, str]]:
        message = {
            'role': GPTRole.SYSTEM.value,
            'content': self._load_prompt(),
        }
        return [message]

    def _load_prompt(self) -> str:
        prompt_path: str = os.path.join(AI_PROMPTS_PATH, self._prompt_name)
        prompt = FileManager.read_txt(prompt_path)
        return prompt

    def update(self, role: GPTRole, message: str):
        message = {
            'role': role.value,
            'content': message,
        }
        self.message_list.append(message)

    def json(self):
        item = json.dumps(
            self,
            default=lambda i: i.__dict__,
            ensure_ascii=False,
            indent=4,
        )
        return item

    @classmethod
    def from_json(cls, data: str):
        json_data = json.loads(data)
        return cls(json_data['_prompt_name'], json_data['message_list'])


class ChatGPT:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model: GPTModel = GPTModel.GPT_4_TURBO):
        self._gpt_token = config.OPENAI_TOKEN
        self._proxy = config.PROXY
        self._client = self._create_client()
        self._model = model.value

    def _create_client(self):
        gpt_client = openai.AsyncOpenAI(
            api_key=self._gpt_token,
            base_url=self._proxy,
        )
        return gpt_client

    async def request(self, message_list: GPTMessage) -> str:
        response = await self._client.chat.completions.create(
            messages=message_list.message_list,
            model=self._model,
        )

        return response.choices[0].message.content
