from abc import ABC, abstractmethod
from typing import Dict, List

from promptlab._config import ExperimentConfig, TracerConfig
from promptlab.sqlite.models import Asset

class Tracer(ABC):
    def __init__(self, tracer_config: TracerConfig):
        pass

    @abstractmethod
    def create_asset(self, asset: Asset): pass

    @abstractmethod
    def trace_experiment(self, asset: Asset): pass

    @abstractmethod
    def get_asset(self, asset_name: str, asset_version: int): pass

    @abstractmethod
    def get_assets_by_type(self, asset_type: str): pass

    @abstractmethod
    def get_latest_asset(self, asset_name: str): pass

    @abstractmethod
    def get_user_by_username(self, username: str): pass

    @abstractmethod
    def get_experiments(self): pass

    @abstractmethod
    def get_users(self): pass

    @abstractmethod
    def create_user(self): pass

    @abstractmethod
    def deactivate_user_by_username(self): pass