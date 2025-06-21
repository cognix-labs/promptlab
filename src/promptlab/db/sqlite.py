from sqlalchemy.orm import Session
from .session import get_session, init_engine
from .models import Asset, Experiment, ExperimentResult
from promptlab.db.sql import SQLQuery
from datetime import datetime
from sqlalchemy import text


class SQLAlchemyClient:
    def __init__(self, db_file: str):
        db_url = f"sqlite:///{db_file}"
        init_engine(db_url)

    def add_asset(self, asset: Asset):
        session = get_session()
        try:
            session.add(asset)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_asset(self, asset_name: str, asset_version: int):
        session = get_session()
        try:
            return (
                session.query(Asset)
                .filter_by(asset_name=asset_name, asset_version=asset_version)
                .first()
            )
        finally:
            session.close()

    def get_latest_asset(self, asset_name: str):
        session = get_session()
        try:
            return (
                session.query(Asset)
                .filter_by(asset_name=asset_name)
                .order_by(Asset.asset_version.desc())
                .first()
            )
        finally:
            session.close()

    def get_assets_by_type(self, asset_type: str):
        session = get_session()
        try:
            return session.query(Asset).filter_by(asset_type=asset_type).all()
        finally:
            session.close()

    def deploy_asset(self, asset_name: str, asset_version: int):
        session = get_session()
        try:
            asset = (
                session.query(Asset)
                .filter_by(asset_name=asset_name, asset_version=asset_version)
                .first()
            )
            if asset:
                asset.is_deployed = True
                asset.deployment_time = datetime.utcnow()
                session.commit()
        finally:
            session.close()

    def add_experiment(self, experiment: Experiment):
        session = get_session()
        try:
            session.add(experiment)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def add_experiment_results(self, results: list):
        session = get_session()
        try:
            session.add_all(results)
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()

    def get_experiments(self):
        session = get_session()
        try:
            # return session.query(Experiment).all()
            return session.execute(text(SQLQuery.SELECT_EXPERIMENTS_QUERY)).mappings().all()

        finally:
            session.close()

    def get_experiment_results(self, experiment_id: str):
        session = get_session()
        try:
            return (
                session.query(ExperimentResult)
                .filter_by(experiment_id=experiment_id)
                .all()
            )
        finally:
            session.close()
