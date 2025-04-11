from abc import ABC, abstractmethod
from typing import Any

from promptlab.types import EmbeddingModelConfig, InferenceResult, InferenceModelConfig


class Model(ABC):
    
    def __init__(self, model_config: InferenceModelConfig):
        self.model_config = model_config

    @abstractmethod
    def __call__(self, system_prompt: str, user_prompt: str)->InferenceResult:
        pass

class EmbeddingModel(ABC):
    
    def __init__(self, model_config: EmbeddingModelConfig):
        self.model_config = model_config

    @abstractmethod
    def __call__(self, text: str) -> Any:
        pass