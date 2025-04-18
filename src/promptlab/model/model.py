from abc import ABC, abstractmethod
from typing import Any
import asyncio

from promptlab.types import InferenceResult, ModelConfig


class Model(ABC):
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.config = model_config

    @abstractmethod
    def invoke(self, system_prompt: str, user_prompt: str) -> InferenceResult:
        """Synchronous invocation of the model"""
        pass

    @abstractmethod
    async def ainvoke(self, system_prompt: str, user_prompt: str) -> InferenceResult:
        """Asynchronous invocation of the model"""
        pass

    def invoke_async(self, system_prompt: str, user_prompt: str) -> InferenceResult:
        """Helper method to run async method in sync context"""
        return asyncio.run(self.ainvoke(system_prompt, user_prompt))

    def __call__(self, system_prompt: str, user_prompt: str) -> InferenceResult:
        return self.invoke(system_prompt, user_prompt)


class EmbeddingModel(ABC):
    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.config = model_config

    @abstractmethod
    def __call__(self, text: str) -> Any:
        pass
