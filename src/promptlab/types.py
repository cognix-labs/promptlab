from dataclasses import dataclass
from typing import Any, List, Optional

from pydantic import BaseModel, HttpUrl, field_validator

from promptlab.enums import TracerType
from promptlab.evaluator.evaluator import Evaluator
from promptlab.utils import Utils

class InferenceModelConfig(BaseModel):
    
    type: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[HttpUrl] = None 
    inference_model_deployment: str

    class config:
        arbitrary_types_allowed=True

class EmbeddingModelConfig(BaseModel):
    
    type: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[HttpUrl] = None 
    embedding_model_deployment: str

    class config:
        arbitrary_types_allowed=True

class ModelConfig(BaseModel):
    
    type: str
    api_key: Optional[str] = None
    api_version: Optional[str] = None
    endpoint: Optional[HttpUrl] = None 
    model_deployment: str

    # class config:
    #     arbitrary_types_allowed=True

class EvaluationConfig(BaseModel):

    metric: str
    column_mapping: dict
    evaluator: Optional[Evaluator] = None

    model_config = {
        "arbitrary_types_allowed": True
    }
    
class AssetConfig(BaseModel):

    name: str
    version: int

class ExperimentConfig(BaseModel):

    # inference_model: InferenceModelConfig
    # embedding_model: EmbeddingModelConfig
    inference_model: Any
    embedding_model: Any
    prompt_template: AssetConfig
    dataset: AssetConfig
    evaluation: List[EvaluationConfig]

    class Config:
        extra = "forbid" 
    
class TracerConfig(BaseModel):

    type: TracerType  
    db_file: str

    @field_validator('db_file')
    def validate_db_server(cls, value):             
        return Utils.sanitize_path(value)
    
    class Config:
        use_enum_values = True 

@dataclass
class InferenceResult:
    inference: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: int

@dataclass
class Dataset:
    name: str
    description: str
    file_path: str
    version: int = 0

@dataclass
class PromptTemplate:
    name: str = None
    description: str = None
    system_prompt: str = None
    user_prompt: str = None
    version: int = 0
