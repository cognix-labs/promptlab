from typing import Any, overload, TypeVar
from datetime import datetime
import json
import re
import os

from promptlab.enums import AssetType
from promptlab.db.sql import SQLQuery
from promptlab.tracer.tracer import Tracer
from promptlab.types import Dataset, PromptTemplate
from promptlab._utils import Utils

T = TypeVar("T", Dataset, PromptTemplate)


class Asset:
    def __init__(self, tracer: Tracer):
        self.tracer = tracer

    @overload
    def create(self, asset: PromptTemplate) -> PromptTemplate: ...

    @overload
    def create(self, asset: Dataset) -> Dataset: ...

    @overload
    def update(self, asset: PromptTemplate) -> PromptTemplate: ...

    @overload
    def update(self, asset: Dataset) -> Dataset: ...

    @overload
    def deploy(self, asset: PromptTemplate, target_dir: str) -> None: ...

    @staticmethod
    def is_valid_name(name: str) -> bool:
        """
        Check if the name is valid.
        """
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name))

    def create(self, asset: T) -> T:
        """
        Create a new asset with a given name.
        """
        if not Asset.is_valid_name(asset.name):
            raise ValueError(
                "Name must begin with a letter and use only alphanumeric, underscore, or hyphen."
            )

        if isinstance(asset, Dataset):
            return self._create_dataset(asset)

        elif isinstance(asset, PromptTemplate):
            return self._create_prompt_template(asset)

        else:
            raise TypeError(f"Unsupported asset type: {type(asset)}")

    def update(self, asset: T) -> T:
        """
        Create a new version of an existing asset.
        """
        if isinstance(asset, Dataset):
            return self._update_dataset(asset)

        elif isinstance(asset, PromptTemplate):
            return self._update_prompt_template(asset)

        else:
            raise TypeError(f"Unsupported asset type: {type(asset)}")

    def _create_dataset(self, dataset: Dataset) -> Dataset:
        dataset.version = 0
        binary = {"file_path": dataset.file_path}
        timestamp = datetime.now().isoformat()

        self.tracer.db_client.execute_query(
            SQLQuery.INSERT_ASSETS_QUERY,
            (
                dataset.name,
                dataset.version,
                dataset.description,
                AssetType.DATASET.value,
                json.dumps(binary),
                timestamp,
            ),
        )

        return dataset

    def _update_dataset(self, dataset: Dataset) -> Dataset:
        dataset_record = self.tracer.db_client.fetch_data(
            SQLQuery.SELECT_ASSET_BY_NAME_QUERY, (dataset.name, dataset.name)
        )[0]

        dataset.description = (
            dataset_record["asset_description"]
            if dataset.description is None
            else dataset.description
        )
        dataset.version = dataset_record["asset_version"] + 1
        binary = (
            dataset_record["asset_binary"]
            if dataset.file_path is None
            else {"file_path": dataset.file_path}
        )
        timestamp = datetime.now().isoformat()

        self.tracer.db_client.execute_query(
            SQLQuery.INSERT_ASSETS_QUERY,
            (
                dataset.name,
                dataset.description,
                dataset.version,
                AssetType.DATASET.value,
                json.dumps(binary),
                timestamp,
            ),
        )

        return dataset

    def _create_prompt_template(self, template: PromptTemplate) -> PromptTemplate:
        template.version = 0
        binary = f"""
            <<system>>
                {template.system_prompt}
            <<user>>
                {template.user_prompt}
        """
        timestamp = datetime.now().isoformat()

        self.tracer.db_client.execute_query(
            SQLQuery.INSERT_ASSETS_QUERY,
            (
                template.name,
                template.version,
                template.description,
                AssetType.PROMPT_TEMPLATE.value,
                binary,
                timestamp,
            ),
        )

        return template

    def _update_prompt_template(self, template: PromptTemplate) -> PromptTemplate:
        timestamp = datetime.now().isoformat()

        prompt_template = self.tracer.db_client.fetch_data(
            SQLQuery.SELECT_ASSET_BY_NAME_QUERY, (template.name, template.name)
        )[0]
        system_prompt, user_prompt, prompt_template_variables = (
            Utils.split_prompt_template(prompt_template["asset_binary"])
        )

        template.description = (
            prompt_template["asset_description"]
            if template.description is None
            else template.description
        )
        template.system_prompt = (
            system_prompt if template.system_prompt is None else template.system_prompt
        )
        template.user_prompt = (
            user_prompt if template.user_prompt is None else template.user_prompt
        )
        template.version = prompt_template["asset_version"] + 1
        binary = f"""
            <<system>>
                {template.system_prompt}
            <<user>>
                {template.user_prompt}
        """

        self.tracer.db_client.execute_query(
            SQLQuery.INSERT_ASSETS_QUERY,
            (
                template.name,
                template.version,
                template.description,
                AssetType.PROMPT_TEMPLATE.value,
                binary,
                timestamp,
            ),
        )

        return template

    def get(self, asset_name: str, version: int) -> Any:
        asset = self.tracer.db_client.fetch_data(
            SQLQuery.SELECT_ASSET_QUERY, (asset_name, version)
        )[0]
        asset_type = asset["asset_type"]

        if asset_type == AssetType.DATASET.value:
            binary = json.loads(asset["asset_binary"])
            file_path = binary["file_path"]
            return Dataset(
                name=asset_name,
                version=version,
                description=asset["asset_description"],
                file_path=file_path,
            )

        if asset_type == AssetType.PROMPT_TEMPLATE.value:
            system_prompt, user_prompt, _ = Utils.split_prompt_template(
                asset["asset_binary"]
            )
            return PromptTemplate(
                name=asset_name,
                version=version,
                description=asset["asset_description"],
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

    def deploy(self, asset: T, target_dir: str) -> T:
        if isinstance(asset, PromptTemplate):
            return self._handle_prompt_template_deploy(asset, target_dir)
        else:
            raise TypeError(f"Unsupported asset type: {type(asset)}")

    def _handle_prompt_template_deploy(self, template: PromptTemplate, target_dir: str):
        prompt_template = self.tracer.db_client.fetch_data(
            SQLQuery.SELECT_ASSET_QUERY, (template.name, template.version)
        )[0]

        prompt_template_name = prompt_template["asset_name"]
        prompt_template_binary = prompt_template["asset_binary"]

        prompt_template_path = os.path.join(target_dir, prompt_template_name)

        with open(prompt_template_path, "w", encoding="utf-8") as file:
            file.write(prompt_template_binary)

        self.tracer.db_client.execute_query(
            SQLQuery.DEPLOY_ASSET_QUERY, (template.name, template.version)
        )
