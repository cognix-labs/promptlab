from datetime import datetime
from typing import Dict, List
import json

from promptlab._config import ExperimentConfig, TracerConfig
from promptlab.db.sqlite import SQLAlchemyClient
from promptlab.tracer.tracer import Tracer
from promptlab.db.models import Experiment as ExperimentModel, ExperimentResult as ExperimentResultModel


class SQLiteTracer(Tracer):
    def __init__(self, tracer_config: TracerConfig):
        self.db_client = SQLAlchemyClient(tracer_config.db_file)

    def init_db(self):
        # Tables are created by SQLAlchemyClient/init_engine
        pass

    def trace(
        self, experiment_config: ExperimentConfig, experiment_summary: List[Dict]
    ) -> None:
        timestamp = datetime.now().isoformat()
        experiment_id = experiment_summary[0]["experiment_id"]

        # Convert model_config objects to dict for JSON serialization
        inference_model_config = (
            vars(experiment_config.inference_model.model_config)
            if experiment_config.inference_model
            else None
        )
        embedding_model_config = (
            vars(experiment_config.embedding_model.model_config)
            if experiment_config.embedding_model
            else None
        )

        model = {
            "inference_model_config": inference_model_config,
            "embedding_model_config": embedding_model_config,
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
        )
        self.db_client.add_experiment(exp)
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
        self.db_client.add_experiment_results(results)
