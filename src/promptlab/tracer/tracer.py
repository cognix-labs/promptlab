from abc import ABC, abstractmethod
from typing import Dict, List

from promptlab._config import ExperimentConfig, TracerConfig


class Tracer(ABC):
    def __init__(self, tracer_config: TracerConfig):
        pass

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def trace(
        self, experiment_config: ExperimentConfig, experiment_summary: List[Dict]
    ):
        pass
