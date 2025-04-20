from enum import Enum


class TracerType(Enum):
    SQLITE = "sqlite"


class ModelType(Enum):
    AZURE_OPENAI = "azure_openai"
    DEEPSEEK = "deepseek"  # For backward compatibility
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"


class AssetType(Enum):
    PROMPT_TEMPLATE = "prompt_template"
    DATASET = "dataset"


class EvaluationMetric(Enum):
    IS_NUMERIC = "is_numeric"
    LENGTH = "length"


class EvalLibrary(Enum):
    RAGAS = "ragas"
    CUSTOM = "custom"
