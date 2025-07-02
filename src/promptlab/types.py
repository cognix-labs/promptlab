from dataclasses import dataclass
from typing import List, Optional, Protocol, runtime_checkable

from pydantic import BaseModel, field_validator

from promptlab.enums import TracerType
from promptlab.evaluator.evaluator import Evaluator
from promptlab._utils import Utils


@dataclass
class ModelResponse:
    response: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: int


@dataclass
class ModelConfig:
    model_deployment: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[str] = None
    max_concurrent_tasks: int = 5


@runtime_checkable
class Model(Protocol):
    def invoke(self, system_prompt: str, user_prompt: str) -> ModelResponse: ...
    async def ainvoke(self, system_prompt: str, user_prompt: str) -> ModelResponse: ...


@runtime_checkable
class EmbeddingModel(Protocol):
    def __call__(self, text: str) -> List[float]: ...


@dataclass
class Asset:
    name: str
    description: str
    file_path: str
    version: int = 0


class Dataset(BaseModel):
    name: str
    description: str
    file_path: str
    version: int = 0


class PromptTemplate(BaseModel):
    name: str
    description: str
    system_prompt: str
    user_prompt: str
    version: int = 0


class EvaluationConfig(BaseModel):
    metric: str
    column_mapping: dict
    evaluator: Optional[Evaluator] = None
    model_config = {"arbitrary_types_allowed": True}


class ExperimentConfig(BaseModel):
    name: str = None
    inference_model: Optional[Model] = None
    embedding_model: Optional[EmbeddingModel] = None
    prompt_template: Optional[PromptTemplate] = None
    agent_proxy: Optional[callable] = None
    dataset: Dataset
    evaluation: List[EvaluationConfig]
    model_config = {"arbitrary_types_allowed": True}


class TracerConfig(BaseModel):
    type: TracerType
    db_file: Optional[str] = None
    endpoint: Optional[str] = None
    jwt_token: Optional[str] = None

    @field_validator("db_file")
    def validate_db_file(cls, value):
        return Utils.sanitize_path(value)

    class Config:
        use_enum_values = True
