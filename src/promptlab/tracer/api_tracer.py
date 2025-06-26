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
        response = requests.post(f"{self.endpoint}/assets", json=asset_data)
        response.raise_for_status()