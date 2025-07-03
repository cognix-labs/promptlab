from datetime import datetime, timezone
from typing import Any, Dict, List
import json

from promptlab._config import ExperimentConfig, TracerConfig
from promptlab.sqlite.session import get_session, init_engine
from promptlab.enums import AssetType
from promptlab.sqlite.sql import SQLQuery
from promptlab.tracer.tracer import Tracer
from promptlab.sqlite.models import Experiment as ExperimentModel, ExperimentResult as ExperimentResultModel, User
from promptlab.types import Dataset, PromptTemplate
from promptlab.sqlite.models import Asset as AssetModel
from sqlalchemy import text
from sqlalchemy.orm import joinedload

class LocalTracer(Tracer):
    def __init__(self, tracer_config: TracerConfig):
        db_url = f"sqlite:///{tracer_config.db_file}"
        init_engine(db_url)

    def create_dataset(self, dataset: Dataset):
        dataset.version = 0
        binary = {"file_path": dataset.file_path}
        asset = AssetModel(
            asset_name=dataset.name,
            asset_version=dataset.version,
            asset_description=dataset.description,
            asset_type=AssetType.DATASET.value,
            asset_binary=json.dumps(binary),
            created_at=datetime.now(timezone.utc),
            user_id=self.get_user_by_username(dataset.user).id
        )     
    
        self._create_asset(asset)

    def create_prompttemplate(self, template: PromptTemplate):
        template.version = 0
        binary = f"""
            <<system>>
                {template.system_prompt}
            <<user>>
                {template.user_prompt}
        """
        asset = AssetModel(
            asset_name=template.name,
            asset_version=template.version,
            asset_description=template.description,
            asset_type=AssetType.PROMPT_TEMPLATE.value,
            asset_binary=binary,
            created_at=datetime.now(timezone.utc),
            user_id=self.get_user_by_username(template.user).id
        )

        self._create_asset(asset)

    def _create_asset(self, asset: AssetModel):
        session = get_session()
        try:
            session.add(asset)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def trace_experiment(
        self, experiment_config: ExperimentConfig, experiment_summary: List[Dict]
    ) -> None:
        session = get_session()
        try:
            timestamp = datetime.now().isoformat()
            experiment_id = experiment_summary[0]["experiment_id"]

            model = {
                "inference_model_config": experiment_config.completion_model_config.model_dump(),
                "embedding_model_config": experiment_config.embedding_model_config.model_dump(),
            }

            asset = {
                "prompt_template_name": experiment_config.prompt_template.name
                if experiment_config.prompt_template
                else None,
                "prompt_template_version": experiment_config.prompt_template.version
                if experiment_config.prompt_template
                else None,
                "dataset_name": experiment_config.dataset.name,
                "dataset_version": experiment_config.dataset.version,
            }

            exp = ExperimentModel(
                experiment_id=experiment_id,
                model=json.dumps(model),
                asset=json.dumps(asset),
                created_at=datetime.utcnow(),
                user_id=1,
            )
            session.add(exp)
            results = [
                ExperimentResultModel(
                    experiment_id=record["experiment_id"],
                    dataset_record_id=record["dataset_record_id"],
                    inference=record["inference"],
                    prompt_tokens=record["prompt_tokens"],
                    completion_tokens=record["completion_tokens"],
                    latency_ms=record["latency_ms"],
                    evaluation=json.dumps(record["evaluation"])
                    if isinstance(record["evaluation"], (dict, list))
                    else record["evaluation"],
                    created_at=datetime.utcnow(),
                )
                for record in experiment_summary
            ]
            session.add_all(results)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_asset(self, asset_name: str, asset_version: int) -> AssetModel:
        session = get_session()
        try:
            asset = session.query(AssetModel).filter_by(
                asset_name=asset_name, asset_version=asset_version).first()
            if not asset:
                raise ValueError(f"Asset {asset_name} with version {asset_version} not found.")
            return asset
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_assets_by_type(self, asset_type: str) -> List[Any]:
        session = get_session()
        try:
            if asset_type not in AssetType._value2member_map_:
                raise ValueError(f"Invalid asset type: {asset_type}")
            assets = session.query(AssetModel).options(joinedload(AssetModel.user)).filter(AssetModel.asset_type == asset_type).all()
            return assets
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_latest_asset(self, asset_name: str) -> AssetModel:
        session = get_session()
        try:
            asset = session.query(AssetModel).filter_by(asset_name=asset_name).order_by(
                AssetModel.asset_version.desc()).first()
            return asset
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_user_by_username(self, username: str) -> User:
        session = get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                raise ValueError(f"User {username} not found.")
            return user
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_experiments(self):
        session = get_session()
        try:
            return session.execute(text(SQLQuery.SELECT_EXPERIMENTS_QUERY)).mappings().all()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_users(self):
        session = get_session()
        try:
            return session.query(User).filter(User.status == 1).all()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def create_user(self, user: User):
        session = get_session()
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def deactivate_user_by_username(self, username: str):
        session = get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                raise ValueError(f"User {username} not found.")
            user.status = 0  # Deactivate user
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def me(self) -> User:
        _current_user_name = 'admin'  # This should be replaced with the actual current user logic
        session = get_session()
        try:
            user = session.query(User).filter_by(username=_current_user_name).first()  # Assuming user with ID 1 is the current user
            if not user:
                raise ValueError("Current user not found.")
            return user
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()