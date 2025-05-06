import json
import asyncio
from flask import Flask, jsonify
from flask_cors import CORS

from promptlab.db.sql import SQLQuery
from promptlab.types import TracerConfig
from promptlab._utils import Utils
from promptlab.enums import AssetType


class AsyncStudioApi:
    def __init__(self, tracer_config: TracerConfig):
        self.tracer_config = tracer_config
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})

        self._setup_routes()

    def _setup_routes(self):
        @self.app.route("/experiments", methods=["GET"])
        async def get_experiments():
            try:
                # Run blocking DB call in a separate thread
                experiments = await asyncio.to_thread(
                    self.tracer_config.db_client.fetch_data,
                    SQLQuery.SELECT_EXPERIMENTS_QUERY,
                )

                # Process experiments and remove asset_binary
                processed_experiments = []
                for experiment in experiments:
                    system_prompt, user_prompt, _ = Utils.split_prompt_template(
                        experiment["asset_binary"]
                    )
                    # Create new dict without asset_binary
                    experiment_data = {
                        k: v for k, v in experiment.items() if k != "asset_binary"
                    }
                    experiment_data["system_prompt_template"] = system_prompt
                    experiment_data["user_prompt_template"] = user_prompt
                    processed_experiments.append(experiment_data)

                return jsonify({"experiments": processed_experiments})

            except Exception as e:
                return jsonify(
                    {
                        "status": "error",
                        "message": "An unexpected error occurred",
                        "error": str(e),
                    }
                ), 500

        @self.app.route("/prompttemplates", methods=["GET"])
        async def get_prompt_templates():
            try:
                # Run blocking DB call in a separate thread
                prompt_templates = await asyncio.to_thread(
                    self.tracer_config.db_client.fetch_data,
                    SQLQuery.SELECT_ASSET_BY_TYPE_QUERY,
                    (AssetType.PROMPT_TEMPLATE.value,),
                )

                processed_templates = []
                for template in prompt_templates:
                    system_prompt, user_prompt, _ = Utils.split_prompt_template(
                        template["asset_binary"]
                    )

                    experiment_data = {
                        k: v for k, v in template.items() if k != "asset_binary"
                    }
                    experiment_data["system_prompt_template"] = system_prompt
                    experiment_data["user_prompt_template"] = user_prompt
                    processed_templates.append(experiment_data)

                return jsonify({"prompt_templates": processed_templates})

            except Exception as e:
                return jsonify(
                    {
                        "status": "error",
                        "message": "An unexpected error occurred",
                        "error": str(e),
                    }
                ), 500

        @self.app.route("/datasets", methods=["GET"])
        async def get_datasets():
            try:
                # Run blocking DB call in a separate thread
                datasets = await asyncio.to_thread(
                    self.tracer_config.db_client.fetch_data,
                    SQLQuery.SELECT_ASSET_BY_TYPE_QUERY,
                    (AssetType.DATASET.value,),
                )

                processed_datasets = []
                for dataset in datasets:
                    file_path = json.loads(dataset["asset_binary"])["file_path"]

                    data = {k: v for k, v in dataset.items() if k != "asset_binary"}
                    data["file_path"] = file_path
                    processed_datasets.append(data)

                return jsonify({"datasets": processed_datasets})

            except Exception as e:
                return jsonify(
                    {
                        "status": "error",
                        "message": "An unexpected error occurred",
                        "error": str(e),
                    }
                ), 500

    async def run(self, host: str = "127.0.0.1", port: int = 5000):
        # Use Flask's async support
        from werkzeug.serving import run_simple

        # Create a task to run the Flask app
        def run_flask_app():
            run_simple(host, port, self.app, use_reloader=False, threaded=True)

        # Run the Flask app in a separate thread
        await asyncio.to_thread(run_flask_app)
