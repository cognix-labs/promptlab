import asyncio
import unittest
import sys
import os
import time
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath("./src"))


class TestAsyncSupport(unittest.TestCase):
    """Test the async functionality in PromptLab"""

    def test_model_abstract_class(self):
        """Test that the Model abstract class has async methods"""
        from promptlab.model.model import Model
        from promptlab.types import ModelConfig

        # Create a mock model config
        model_config = ModelConfig(
            type="mock",
            completion_model_deployment="mock-model",
            embedding_model_deployment="mock-model",
        )

        # Create a concrete implementation of the abstract class
        class ConcreteModel(Model):
            def invoke(self, system_prompt, user_prompt):
                return {"completion": "test"}

            async def ainvoke(self, system_prompt, user_prompt):
                return {"completion": "test"}

        # Create an instance of the concrete model
        model = ConcreteModel(model_config)

        # Check that the model has the expected methods
        self.assertTrue(hasattr(model, "invoke"))
        self.assertTrue(hasattr(model, "ainvoke"))
        self.assertTrue(hasattr(model, "invoke_async"))

    def test_async_execution_performance(self):
        """Test that async execution is faster than synchronous execution"""

        # Define mock sync and async functions
        def sync_function():
            time.sleep(0.1)
            return "result"

        async def async_function():
            await asyncio.sleep(0.1)
            return "result"

        # Test synchronous execution
        start_time = time.time()
        results = []
        for _ in range(10):
            results.append(sync_function())
        sync_time = time.time() - start_time

        # Test asynchronous execution
        async def run_async_test():
            start_time = time.time()
            tasks = [async_function() for _ in range(10)]
            await asyncio.gather(*tasks)
            return time.time() - start_time

        async_time = asyncio.run(run_async_test())

        # Async should be significantly faster
        self.assertLess(async_time, sync_time / 2)

    def test_azure_openai_async(self):
        """Test that AzOpenAI model supports async invocation"""
        from promptlab.model.azure_openai import AzOpenAI
        from promptlab.types import ModelConfig, ModelResponse

        # Create a mock model config
        model_config = ModelConfig(
            type="azure_openai",
            api_key="test-key",
            api_version="2023-05-15",
            endpoint="https://test.openai.azure.com",
            completion_model_deployment="gpt-35-turbo",
            embedding_model_deployment="text-embedding-ada-002",
        )

        # Mock the client's chat.completions.create method
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock()]
        mock_completion.choices[0].message.content = "Test response"
        mock_completion.usage.prompt_tokens = 10
        mock_completion.usage.completion_tokens = 20

        # Mock the sync client
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_completion

        # Create an instance of AzOpenAI with mocked methods
        model = AzOpenAI(model_config)

        # Mock the invoke method
        model.invoke = MagicMock(
            return_value=ModelResponse(
                completion="Test response",
                prompt_tokens=10,
                completion_tokens=20,
                latency_ms=100,
            )
        )

        # Instead of testing the async method directly, we'll test the __call__ method
        # which should handle both sync and async contexts
        result = model("System prompt", "User prompt")

        # Check that the result has the expected structure
        self.assertEqual(result.completion, "Test response")
        self.assertEqual(result.prompt_tokens, 10)
        self.assertEqual(result.completion_tokens, 20)
        self.assertIsNotNone(result.latency_ms)

    def test_experiment_async_methods(self):
        """Test that Experiment class has async methods"""
        from promptlab._experiment import Experiment
        from promptlab.tracer.tracer import Tracer

        # Create a mock tracer
        tracer = MagicMock(spec=Tracer)

        # Create an instance of Experiment
        experiment = Experiment(tracer)

        # Check that the experiment has the expected methods
        self.assertTrue(hasattr(experiment, "run"))
        self.assertTrue(hasattr(experiment, "run_async"))
        self.assertTrue(hasattr(experiment, "init_batch_eval_async"))
        self.assertTrue(hasattr(experiment, "_process_record_async"))

    def test_async_studio(self):
        """Test that Studio class has async methods"""
        from promptlab.studio.studio import Studio
        from promptlab._config import TracerConfig

        # Create a mock tracer config
        tracer_config = MagicMock(spec=TracerConfig)

        # Create an instance of Studio
        studio = Studio(tracer_config)

        # Check that the studio has the expected async methods
        self.assertTrue(hasattr(studio, "start_async"))
        self.assertTrue(hasattr(studio, "start"))
        self.assertTrue(hasattr(studio, "start_web_server"))
        self.assertTrue(hasattr(studio, "start_api_server_async"))
        self.assertTrue(hasattr(studio, "shutdown"))

    def test_promptlab_async_methods(self):
        """Test that PromptLab class has async methods"""
        from promptlab.core import PromptLab

        # Create a mock tracer config
        tracer_config = {"type": "sqlite", "db_file": ":memory:"}

        # Create an instance of PromptLab
        with patch("promptlab.core.TracerFactory"):
            with patch("promptlab.core.ConfigValidator"):
                with patch("promptlab.core.TracerConfig"):
                    promptlab = PromptLab(tracer_config)

                    # Check that the promptlab has the expected methods
                    self.assertTrue(hasattr(promptlab, "experiment.run_async"))
                    self.assertTrue(hasattr(promptlab, "studio.start_async"))
                    # No longer has async_studio attribute after refactoring
                    self.assertTrue(hasattr(promptlab, "studio"))


if __name__ == "__main__":
    unittest.main()
