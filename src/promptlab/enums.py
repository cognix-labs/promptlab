from enum import Enum


class TracerType(Enum):
    REMOTE = "remote"
    LOCAL = "local"


class AssetType(Enum):
    PROMPT_TEMPLATE = "prompt_template"
    DATASET = "dataset"
