from datetime import datetime
from typing import Dict, List
import json
import requests

from promptlab._config import ExperimentConfig, TracerConfig
from promptlab.tracer.tracer import Tracer
from promptlab.sqlite.models import Experiment as ExperimentModel, ExperimentResult as ExperimentResultModel
from promptlab.types import Asset


class ApiTracer(Tracer):
    def __init__(self, tracer_config: TracerConfig):
        self.endpoint = tracer_config.endpoint
        self.jwt_token = tracer_config.jwt_token

    def create_asset(self, asset: Asset):
        asset_data = {
            "name": asset.name,
            "version": asset.version,
            "description": asset.description,
            "type": asset.type,
            "asset_binary": asset.asset_binary if isinstance(asset.asset_binary, str) else json.dumps(asset.asset_binary),
            "is_deployed": asset.is_deployed,
            "created_at": datetime.utcnow().isoformat(),
            "user_id": getattr(asset, 'user_id', None)
        }
        
        headers = {"Content-Type": "application/json"}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
            
        response = requests.post(f"{self.endpoint}/assets", json=asset_data, headers=headers)
        response.raise_for_status()

    def trace_experiment(self, asset: Asset):
        raise NotImplementedError("trace_experiment method not implemented")

    def get_asset(self, asset_name: str, asset_version: int):
        raise NotImplementedError("get_asset method not implemented")

    def get_assets_by_type(self, asset_type: str):
        raise NotImplementedError("get_assets_by_type method not implemented")

    def get_latest_asset(self, asset_name: str):
        raise NotImplementedError("get_latest_asset method not implemented")

    def get_user_by_username(self, username: str):
        raise NotImplementedError("get_user_by_username method not implemented")

    def get_experiments(self):
        raise NotImplementedError("get_experiments method not implemented")

    def get_users(self):
        raise NotImplementedError("get_users method not implemented")

    def create_user(self):
        raise NotImplementedError("create_user method not implemented")

    def deactivate_user_by_username(self):
        raise NotImplementedError("deactivate_user_by_username method not implemented")