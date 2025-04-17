from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

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
    def __call__(self, system_prompt: str, user_prompt: str)->InferenceResult:
        pass

class EmbeddingModel(ABC):
    
    def __init__(self, model_config: ModelConfig):
        config = ModelConfig(**model_config)
        self.config = config

    @abstractmethod
    def __call__(self, text: str) -> Any:
        pass