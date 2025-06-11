from datetime import datetime
from typing import List
import json
import uuid
import asyncio

from promptlab._config import ConfigValidator, ExperimentConfig
from promptlab.db.sql import SQLQuery
from promptlab.evaluator.evaluator_factory import EvaluatorFactory
from promptlab.tracer.tracer import Tracer
from promptlab._utils import Utils


class Experiment:
    def __init__(self, tracer: Tracer):
        self.tracer = tracer

    def run(self, experiment_config: ExperimentConfig):
        """
        Synchronous version of experiment execution
        """
        (
            experiment_config,
            eval_dataset,
            system_prompt,
            user_prompt,
            prompt_template_variables,
        ) = self._prepare_experiment_data(experiment_config)

        exp_summary = self._init_batch_eval(
            eval_dataset,
            system_prompt,
            user_prompt,
            prompt_template_variables,
            experiment_config,
        )

        self.tracer.trace(experiment_config, exp_summary)

    async def run_async(self, experiment_config: ExperimentConfig):
        """
        Asynchronous version of experiment execution
        """
        (
            experiment_config,
            eval_dataset,
            system_prompt,
            user_prompt,
            prompt_template_variables,
        ) = self._prepare_experiment_data(experiment_config)

        exp_summary = await self._init_batch_eval_async(
            eval_dataset,
            system_prompt,
            user_prompt,
            prompt_template_variables,
            experiment_config,
        )

        self.tracer.trace(experiment_config, exp_summary)

    def _prepare_experiment_data(self, experiment_config: ExperimentConfig):
        """
        Prepare common experiment data used by both sync and async versions
        """
        experiment_config = ExperimentConfig(**experiment_config)
        ConfigValidator.validate_experiment_config(experiment_config)

        # if experiment_config.prompt_template is None:
        pt_asset_binary = None
        if experiment_config.prompt_template:
            prompt_template = self.tracer.db_client.fetch_data(
                SQLQuery.SELECT_ASSET_QUERY,
                (
                    experiment_config.prompt_template.name,
                    experiment_config.prompt_template.version,
                ),
            )[0]
            pt_asset_binary = prompt_template["asset_binary"]

        system_prompt, user_prompt, prompt_template_variables = (
            Utils.split_prompt_template(pt_asset_binary)
        )

        eval_dataset_path = self.tracer.db_client.fetch_data(
            SQLQuery.SELECT_DATASET_FILE_PATH_QUERY,
            (experiment_config.dataset.name, experiment_config.dataset.version),
        )[0]
        eval_dataset = Utils.load_dataset(eval_dataset_path["file_path"])

        return (
            experiment_config,
            eval_dataset,
            system_prompt,
            user_prompt,
            prompt_template_variables,
        )

    def _init_batch_eval(
        self,
        eval_dataset,
        system_prompt,
        user_prompt,
        prompt_template_variables,
        experiment_config: ExperimentConfig,
    ) -> List:
        """
        Synchronous version of batch evaluation with concurrency limit
        """
        inference_model = experiment_config.inference_model
        agent_proxy = experiment_config.agent_proxy
        experiment_id = (
            experiment_config.name if experiment_config.name else str(uuid.uuid4())
        )
        timestamp = datetime.now().isoformat()

        exp_summary = []

        for eval_record in eval_dataset:
            sys_prompt, usr_prompt = self._prepare_prompts(
                eval_record, system_prompt, user_prompt, prompt_template_variables
            )

            model_response = (
                agent_proxy(eval_record)
                if agent_proxy
                else inference_model(sys_prompt, usr_prompt)
            )
            evaluation = self._evaluate(
                model_response.response, eval_record, experiment_config
            )

            eval = dict()
            eval["experiment_id"] = experiment_id
            eval["dataset_record_id"] = eval_record["id"]
            eval["inference"] = model_response.response
            eval["prompt_tokens"] = model_response.prompt_tokens
            eval["completion_tokens"] = model_response.completion_tokens
            eval["latency_ms"] = model_response.latency_ms
            eval["evaluation"] = evaluation
            eval["created_at"] = timestamp

            exp_summary.append(eval)

        return exp_summary

    async def _init_batch_eval_async(
        self,
        eval_dataset,
        system_prompt,
        user_prompt,
        prompt_template_variables,
        experiment_config: ExperimentConfig,
    ) -> List:
        """
        Asynchronous version of batch evaluation with concurrency limit
        """
        inference_model = experiment_config.inference_model
        agent_proxy = experiment_config.agent_proxy

        experiment_id = (
            experiment_config.name if experiment_config.name else str(uuid.uuid4())
        )
        timestamp = datetime.now().isoformat()
        max_concurrent_tasks = getattr(inference_model, "max_concurrent_tasks", 5)

        exp_summary = []

        prepared_prompts = []
        for eval_record in eval_dataset:
            sys_prompt, usr_prompt = self._prepare_prompts(
                eval_record, system_prompt, user_prompt, prompt_template_variables
            )
            prepared_prompts.append((eval_record, sys_prompt, usr_prompt))

        # Process in batches with limited concurrency
        semaphore = asyncio.Semaphore(max_concurrent_tasks)

        async def process_with_semaphore(record, s_prompt, u_prompt):
            async with semaphore:
                return await self._process_record_async(
                    inference_model,
                    agent_proxy,
                    s_prompt,
                    u_prompt,
                    record,
                    experiment_id,
                    timestamp,
                    experiment_config,
                )

        # Create tasks for async execution with semaphore
        tasks = []
        for eval_record, sys_prompt, usr_prompt in prepared_prompts:
            task = asyncio.create_task(
                process_with_semaphore(eval_record, sys_prompt, usr_prompt)
            )
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        exp_summary.extend(results)

        return exp_summary

    def _evaluate(
        self, inference: str, row, experiment_config: ExperimentConfig
    ) -> str:
        evaluations = []
        for eval in experiment_config.evaluation:
            evaluator = EvaluatorFactory.get_evaluator(
                eval.metric,
                experiment_config.inference_model,
                experiment_config.embedding_model,
                eval.evaluator,
            )

            data = dict()
            for key, value in eval.column_mapping.items():
                if value == "$inference":
                    data[key] = inference
                else:
                    data[key] = row[value]

            evaluation_result = evaluator.evaluate(data)

            evaluations.append(
                {"metric": f"{eval.metric}", "result": evaluation_result}
            )
        return json.dumps(evaluations)

    async def _process_record_async(
        self,
        inference_model,
        agent_proxy,
        system_prompt,
        user_prompt,
        eval_record,
        experiment_id,
        timestamp,
        experiment_config,
    ):
        """
        Process a single record asynchronously
        """
        # model_response = await inference_model(system_prompt, user_prompt)
        model_response = (
            await agent_proxy(eval_record)
            if agent_proxy
            else await inference_model(system_prompt, user_prompt)
        )
        # Run potentially blocking evaluation in a separate thread
        evaluation = await asyncio.to_thread(
            self._evaluate, model_response.response, eval_record, experiment_config
        )

        eval_result = dict()
        eval_result["experiment_id"] = experiment_id
        eval_result["dataset_record_id"] = eval_record["id"]
        eval_result["inference"] = model_response.response
        eval_result["prompt_tokens"] = model_response.prompt_tokens
        eval_result["completion_tokens"] = model_response.completion_tokens
        eval_result["latency_ms"] = model_response.latency_ms
        eval_result["evaluation"] = evaluation
        eval_result["created_at"] = timestamp

        return eval_result

    def _prepare_prompts(
        self, item, system_prompt, user_prompt, prompt_template_variables
    ):
        for variable in prompt_template_variables:
            placeholder = f"<{variable}>"
            replacement = f"<{item[variable]}>"

            system_prompt = system_prompt.replace(placeholder, replacement)
            user_prompt = user_prompt.replace(placeholder, replacement)

        return system_prompt, user_prompt
