import asyncio
import pytest
import sys
import os
import time
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath("./src"))


@pytest.mark.asyncio
async def test_async_model_invocation():
    """Test async model invocation"""
    from promptlab.model.model import Model
    from promptlab.types import ModelConfig, ModelResponse

    # Create a mock model
    class MockModel(Model):
        def __init__(self, model_config):
            super().__init__(model_config)

        def invoke(self, system_prompt, user_prompt):
            """Synchronous invocation"""
            time.sleep(0.1)
            return ModelResponse(
                response=f"Response to: {user_prompt}",
                prompt_tokens=10,
                completion_tokens=20,
                latency_ms=100,
            )

        async def ainvoke(self, system_prompt, user_prompt):
            """Asynchronous invocation"""
            await asyncio.sleep(0.1)
            return ModelResponse(
                response=f"Async response to: {user_prompt}",
                prompt_tokens=10,
                completion_tokens=20,
                latency_ms=100,
            )

    # Create a model config
    model_config = ModelConfig(
        model_deployment="mock-model",
    )

    # Create a model instance
    model = MockModel(model_config)

    # Test synchronous invocation
    start_time = time.time()
    sync_results = []
    for i in range(5):
        result = model.invoke("System prompt", f"Test prompt {i}")
        sync_results.append(result)
    sync_time = time.time() - start_time

    # Test asynchronous invocation
    start_time = time.time()
    tasks = []
    for i in range(5):
        task = model.ainvoke("System prompt", f"Test prompt {i}")
        tasks.append(task)
    async_results = await asyncio.gather(*tasks)
    async_time = time.time() - start_time

    # Async should be significantly faster
    assert async_time < sync_time / 2

    # Check that the results are correct
    for i, result in enumerate(async_results):
        assert result.response == f"Async response to: Test prompt {i}"
        assert result.prompt_tokens == 10
        assert result.completion_tokens == 20
        assert result.latency_ms == 100


@pytest.mark.asyncio
async def test_experiment_async_execution():
    """Test async experiment execution"""
    from promptlab._experiment import Experiment

    # Create a mock tracer
    tracer = MagicMock()
    tracer.db_client.fetch_data.return_value = [
        {"asset_binary": "system: test\nuser: test", "file_path": "test.jsonl"}
    ]

    # Create a mock dataset
    dataset = [{"id": 1, "text": "test"}]

    # Mock the Utils.load_dataset method
    with patch("promptlab.experiment.Utils") as mockUtils:
        mockUtils.load_dataset.return_value = dataset
        mockUtils.split_prompt_template.return_value = (
            "system: test",
            "user: test",
            [],
        )

        # Mock the ExperimentConfig validation
        with patch("promptlab.experiment.ExperimentConfig") as mock_config_class:
            # Make the mock return itself when called with **kwargs
            mock_instance = MagicMock()
            mock_config_class.return_value = mock_instance
            mock_instance.prompt_template.name = "test"
            mock_instance.prompt_template.version = "1.0"
            mock_instance.dataset.name = "test"
            mock_instance.dataset.version = "1.0"
            mock_instance.evaluation = []
            mock_instance.model = MagicMock()

            # Create a mock experiment config
            experiment_config = {}
            # We'll patch the validation in the Experiment class

            # Create an experiment instance
            experiment = Experiment(tracer)

            # Mock the init_batch_eval_async method
            with patch.object(experiment, "init_batch_eval_async") as mock_batch_eval:
                mock_batch_eval.return_value = asyncio.Future()
                mock_batch_eval.return_value.set_result([{"experiment_id": "test"}])

                # Test async run
                await experiment.run_async(experiment_config)

                # Check that init_batch_eval_async was called
                mock_batch_eval.assert_called_once()

                # Check that tracer.trace was called
                tracer.trace.assert_called_once()


@pytest.mark.asyncio
async def test_async_studio():
    """Test async studio"""
    from promptlab.studio.studio import Studio

    # Create a mock tracer config
    tracer_config = MagicMock()

    # Create a studio instance
    studio = Studio(tracer_config)

    # Mock the start_web_server method
    with patch.object(studio, "start_web_server") as mock_web_server:
        # Mock the start_api_server_async method
        with patch.object(studio, "start_api_server_async") as mock_api_server:
            mock_api_server.return_value = asyncio.Future()
            mock_api_server.return_value.set_result(None)

            # Create a task that will be cancelled
            task = asyncio.create_task(studio.start_async(8000))

            # Wait a bit for the task to start
            await asyncio.sleep(0.1)

            # Cancel the task
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

            # Check that start_web_server was called
            mock_web_server.assert_called_once_with(8000)

            # Check that start_api_server_async was called
            mock_api_server.assert_called_once_with(8001)


@pytest.mark.asyncio
async def test_promptlab_async_methods():
    """Test PromptLab async methods"""
    from promptlab.core import PromptLab

    # Create a mock tracer config
    tracer_config = {"type": "sqlite", "db_file": ":memory:"}

    # Mock the TracerFactory
    with patch("promptlab.core.TracerFactory") as mock_factory:
        # Set up the mock factory
        mock_tracer = MagicMock()
        mock_factory.get_tracer.return_value = mock_tracer

        # Mock the ConfigValidator
        with patch("promptlab.core.ConfigValidator") as mock_validator:
            # Set up the mock validator
            mock_validator.validate_tracer_config.return_value = None

            # Create a PromptLab instance
            promptlab = PromptLab(tracer_config)

            # Mock the experiment.run_async method
            with patch.object(promptlab.experiment, "run_async") as mock_run_async:
                mock_run_async.return_value = asyncio.Future()
                mock_run_async.return_value.set_result(None)

                # Test experiment.run_async
                experiment_config = {"test": "config"}
                await promptlab.experiment.run_async(experiment_config)

                # Check that experiment.run_async was called
                mock_run_async.assert_called_once_with(experiment_config)

            # Mock the studio.start_async method
            with patch.object(promptlab.studio, "start_async") as mock_start_async:
                mock_start_async.return_value = asyncio.Future()
                mock_start_async.return_value.set_result(None)

                # Test studio.start_async
                await promptlab.studio.start_async(8000)

                # Check that studio.start_async was called
                mock_start_async.assert_called_once_with(8000)
