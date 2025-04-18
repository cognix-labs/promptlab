from abc import ABC, abstractmethod
from typing import Union, Any, Optional
import asyncio
from dataclasses import dataclass

from promptlab.types import EmbeddingModelConfig, InferenceResult, InferenceModelConfig

@dataclass
class ModelConfig:
    type: str
    model_deployment: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None

@dataclass
class InferenceResult:
    inference: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: int

class Model(ABC):

    def __init__(self, model_config: ModelConfig):
        config = ModelConfig(**model_config)
        self.config = config

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
        config = ModelConfig(**model_config)
        self.config = config

    @abstractmethod
    def __call__(self, text: str) -> Any:
        pass
