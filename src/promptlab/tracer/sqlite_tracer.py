from datetime import datetime
from typing import Dict, List
import json

from promptlab.config import ExperimentConfig, TracerConfig
from promptlab.db.sqlite import SQLiteClient
from promptlab.tracer.tracer import Tracer
from promptlab.db.sql import SQLQuery

class SQLiteTracer(Tracer):
    
    def __init__(self, tracer_config: TracerConfig):

        self.db_client = SQLiteClient(tracer_config.db_file)

    def init_db(self):
        
        self.db_client.execute_query(SQLQuery.CREATE_ASSETS_TABLE_QUERY)
        self.db_client.execute_query(SQLQuery.CREATE_EXPERIMENTS_TABLE_QUERY)   
        self.db_client.execute_query(SQLQuery.CREATE_EXPERIMENT_RESULT_TABLE_QUERY)

    def trace(self, experiment_config: ExperimentConfig, experiment_summary: List[Dict]) -> None:

        timestamp = datetime.now().isoformat()
        experiment_id = experiment_summary[0]['experiment_id']

        model = {
            "type": experiment_config.model.type,
            "api_version": experiment_config.model.api_version,
            "endpoint": str(experiment_config.model.endpoint),
            "inference_model_deployment": experiment_config.model.inference_model_deployment,
            "embedding_model_deployment": experiment_config.model.embedding_model_deployment
        }

        asset = {
            "prompt_template_name": experiment_config.prompt_template.name,
            "prompt_template_version": experiment_config.prompt_template.version,
            "dataset_name": experiment_config.dataset.name,
            "dataset_version": experiment_config.dataset.version
        }

        self.db_client.execute_query(SQLQuery.INSERT_EXPERIMENT_QUERY, (experiment_id, json.dumps(model), json.dumps(asset), timestamp))
        self.db_client.execute_query_many(SQLQuery.INSERT_BATCH_EXPERIMENT_RESULT_QUERY, experiment_summary)