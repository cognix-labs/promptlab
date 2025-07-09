from typing import Any, overload, TypeVar
import json
import re

from promptlab.enums import AssetType
from promptlab.tracer.tracer import Tracer
from promptlab.types import Dataset, PromptTemplate
from promptlab._utils import Utils
from promptlab._logging import logger

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

    # @overload
    # def deploy(self, asset: PromptTemplate, target_dir: str) -> None: ...

    @staticmethod
    def is_valid_name(name: str) -> bool:
        """
        Check if the name is valid.
        """
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name))

    def create(self, asset: T) -> T:
        logger.info(f"Creating asset: {getattr(asset, 'name', str(asset))}")

        if not Asset.is_valid_name(asset.name):
            logger.warning(f"Invalid asset name: {asset.name}")
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
        logger.info(f"Updating asset: {getattr(asset, 'name', str(asset))}")

        if isinstance(asset, Dataset):
            return self._update_dataset(asset)

        elif isinstance(asset, PromptTemplate):
            return self._update_prompt_template(asset)

        else:
            raise TypeError(f"Unsupported asset type: {type(asset)}")

    def _create_dataset(self, dataset: Dataset) -> Dataset:
        logger.debug(f"Creating dataset asset: {dataset.name}")

        self.tracer.create_dataset(dataset)

        logger.debug(f"Dataset asset created: {dataset.name}")

        return dataset

    def _update_dataset(self, dataset: Dataset) -> Dataset:
        logger.debug(f"Updating dataset asset: {dataset.name}")

        prev = self.tracer.get_latest_asset(dataset.name)
        dataset.description = (
            prev.asset_description
            if dataset.description is None
            else dataset.description
        )
        dataset.version = prev.asset_version + 1

        self.tracer.create_dataset(dataset)

        logger.debug(f"Dataset asset created: {dataset.name}")

        return dataset

    def _create_prompt_template(self, template: PromptTemplate) -> PromptTemplate:
        logger.debug(f"Creating prompt template asset: {template.name}")

        self.tracer.create_prompttemplate(template)

        logger.debug(f"Prompt template asset created: {template.name}")

        return template

    def _update_prompt_template(self, template: PromptTemplate) -> PromptTemplate:
        logger.debug(f"Updating prompt template asset: {template.name}")

        prev = self.tracer.get_latest_asset(template.name)
        system_prompt, user_prompt, _ = Utils.split_prompt_template(prev.asset_binary)
        template.description = (
            prev.asset_description
            if template.description is None
            else template.description
        )
        template.system_prompt = (
            system_prompt if template.system_prompt is None else template.system_prompt
        )
        template.user_prompt = (
            user_prompt if template.user_prompt is None else template.user_prompt
        )
        template.version = prev.asset_version + 1

        self.tracer.create_prompttemplate(template)

        logger.debug(f"Prompt template asset updated: {template.name}")

        return template

    def get(self, asset_name: str, version: int) -> Any:
        logger.info(f"Fetching asset: {asset_name}, version: {version}")

        asset = self.tracer.get_asset(asset_name, version)
        asset_type = asset.asset_type

        if asset_type == AssetType.DATASET.value:
            binary = json.loads(asset.asset_binary)
            file_path = binary["file_path"]
            return Dataset(
                name=asset_name,
                version=version,
                description=asset.asset_description,
                file_path=file_path,
            )
        if asset_type == AssetType.PROMPT_TEMPLATE.value:
            system_prompt, user_prompt, _ = Utils.split_prompt_template(
                asset.asset_binary
            )
            return PromptTemplate(
                name=asset_name,
                version=version,
                description=asset.asset_description,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

    # def deploy(self, asset: T, target_dir: str) -> T:
    #     logger.info(
    #         f"Deploying asset: {getattr(asset, 'name', str(asset))} to {target_dir}"
    #     )
    #     if isinstance(asset, PromptTemplate):
    #         return self._handle_prompt_template_deploy(asset, target_dir)
    #     else:
    #         raise TypeError(f"Unsupported asset type: {type(asset)}")

    # def _handle_prompt_template_deploy(self, template: PromptTemplate, target_dir: str):
    #     logger.debug(
    #         f"Handling prompt template deploy: {template.name} to {target_dir}"
    #     )
    #     asset = self.tracer.db_client.get_asset(template.name, template.version)
    #     prompt_template_name = asset.asset_name
    #     prompt_template_binary = asset.asset_binary
    #     prompt_template_path = os.path.join(target_dir, prompt_template_name)
    #     with open(prompt_template_path, "w", encoding="utf-8") as file:
    #         file.write(prompt_template_binary)
    #     self.tracer.db_client.deploy_asset(template.name, template.version)
