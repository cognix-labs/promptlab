from enum import Enum


class TracerType(Enum):
    SQLITE = "sqlite"
    API = "api"  # upcoming


class AssetType(Enum):
    PROMPT_TEMPLATE = "prompt_template"
    DATASET = "dataset"
