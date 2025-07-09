from abc import ABC, abstractmethod
from typing import List, Union, Awaitable
import asyncio

from promptlab.types import ModelResponse, ModelConfig


class Model(ABC):
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.max_concurrent_tasks = getattr(model_config, "max_concurrent_tasks", 5)

    @abstractmethod
    def invoke(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        """Synchronous invocation of the model"""
        pass

    @abstractmethod
    async def ainvoke(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        """Asynchronous invocation of the model"""
        pass

    def __call__(
        self, system_prompt: str, user_prompt: str
    ) -> Union[ModelResponse, Awaitable[ModelResponse]]:
        """Make the model callable for both sync and async contexts"""
        # Check if we're in an async context by inspecting the caller's frame
        try:
            # If we're in an async context and the caller is awaiting this call
            if asyncio.get_event_loop().is_running():
                return self.ainvoke(system_prompt, user_prompt)
        except RuntimeError:
            # If we're not in an async context, use the sync version
            pass

        # Default to synchronous invocation
        return self.invoke(system_prompt, user_prompt)


class EmbeddingModel(ABC):
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config

    @abstractmethod
    def __call__(self, text: str) -> List[float]:
        pass
