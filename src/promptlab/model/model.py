from abc import ABC, abstractmethod
from typing import Any

from promptlab.types import EmbeddingModelConfig, InferenceResult, InferenceModelConfig, ModelConfig


class Model(ABC):
    
    def __init__(self, model_config: ModelConfig):
        config = ModelConfig(**model_config)
        self.config = config

    @abstractmethod
    def __call__(self, system_prompt: str, user_prompt: str)->InferenceResult:
        pass

class EmbeddingModel(ABC):
    
    def __init__(self, model_config: ModelConfig):
        config = ModelConfig(**model_config)
        self.config = config

    @abstractmethod
    def __call__(self, text: str) -> Any:
        pass