from datetime import datetime
from typing import Dict, List
import requests

from promptlab.types import ExperimentConfig, TracerConfig
from promptlab.tracer.tracer import Tracer
from promptlab.sqlite.models import Asset as ORMAsset
from promptlab.types import Dataset, PromptTemplate


class ApiTracer(Tracer):
    def __init__(self, tracer_config: TracerConfig):
        self.endpoint = tracer_config.endpoint
        self.jwt_token = tracer_config.jwt_token

    def create_dataset(self, dataset: Dataset):
        headers = {"Content-Type": "application/json"}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"

        response = requests.post(
            f"{self.endpoint}/datasets", json=dataset.model_dump(), headers=headers
        )
        response.raise_for_status()

    def create_prompttemplate(self, template: PromptTemplate):
        headers = {"Content-Type": "application/json"}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"

        response = requests.post(
            f"{self.endpoint}/templates", json=template.model_dump(), headers=headers
        )
        response.raise_for_status()

    def trace_experiment(
        self, experiment_config: ExperimentConfig, experiment_summary: List[Dict]
    ):
        headers = {"Content-Type": "application/json"}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"

        experiment_config.completion_model_config.model = None
        experiment_config.embedding_model_config.model = None

        payload = {
            "experiment_config": experiment_config.model_dump(),
            "experiment_summary": experiment_summary,
        }

        response = requests.post(
            f"{self.endpoint}/experiments", json=payload, headers=headers
        )
        response.raise_for_status()

    def get_asset(self, asset_name: str, asset_version: int) -> ORMAsset:
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"

        params = {"asset_name": asset_name, "asset_version": asset_version}

        response = requests.get(
            f"{self.endpoint}/assets", params=params, headers=headers
        )
        response.raise_for_status()

        asset_data = response.json()
        if asset_data and "asset" in asset_data:
            # Convert the JSON response back to ORMAsset
            asset_info = asset_data["asset"]

            created_at = None
            if ts := asset_info.get("created_at"):
                try:
                    created_at = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    pass

            deployment_time = None
            if ts := asset_info.get("deployment_time"):
                try:
                    deployment_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    pass

            return ORMAsset(
                asset_name=asset_info["asset_name"],
                asset_version=asset_info["asset_version"],
                asset_description=asset_info.get("asset_description"),
                asset_type=asset_info["asset_type"],
                asset_binary=asset_info.get("asset_binary"),
                created_at=created_at,
                user_id=asset_info.get("user_id"),
                is_deployed=asset_info.get("is_deployed"),
                deployment_time=deployment_time,
            )
        else:
            raise ValueError(
                f"Asset {asset_name} with version {asset_version} not found."
            )

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

    def me(self):
        raise NotImplementedError("me method not implemented")
