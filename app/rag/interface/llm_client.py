from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage

class AsyncLLMClient(ABC):
    @abstractmethod
    async def call(self, prompt: str)->BaseMessage:
        pass
