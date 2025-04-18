import asyncio
import time
from unittest.mock import MagicMock
from promptlab.model.model import Model
from promptlab.types import InferenceResult, ModelConfig

class MockModel(Model):
    """A mock model for testing async functionality"""
    
    def __init__(self, model_config: ModelConfig = None, delay_seconds: float = 0.1):
        # Provide a default mock config if none is passed
        if model_config is None:
            model_config = ModelConfig(type="mock", inference_model_deployment="mock-sync-async")
        super().__init__(model_config)
        self.delay_seconds = delay_seconds
        self.latency_ms = int(delay_seconds * 1000)

    async def ainvoke(self, system_prompt, user_prompt) -> InferenceResult:
        """Async invocation that simulates a delay"""
        await asyncio.sleep(self.delay_seconds) # Simulate network delay
        return InferenceResult(
            inference=f"Async response to: {user_prompt}",
            prompt_tokens=10,
            completion_tokens=20,
            latency_ms=self.latency_ms
        )
    
    def invoke(self, system_prompt, user_prompt) -> InferenceResult:
        """Synchronous invocation"""
        time.sleep(self.delay_seconds) # Simulate network delay
        return InferenceResult(
            inference=f"Sync response to: {user_prompt}",
            prompt_tokens=10,
            completion_tokens=20,
            latency_ms=self.latency_ms
        )

def create_mock_experiment_config():
    """Create a mock experiment config for testing"""
    config = MagicMock()
    config.prompt_template = MagicMock()
    config.prompt_template.name = "test"
    config.prompt_template.version = "1.0"
    config.dataset = MagicMock()
    config.dataset.name = "test"
    config.dataset.version = "1.0"
    config.evaluation = []
    config.model = MagicMock()
    return config

def create_mock_tracer():
    """Create a mock tracer for testing"""
    tracer = MagicMock()
    tracer.db_client.fetch_data.return_value = [{"asset_binary": "system: test\nuser: test", "file_path": "test.jsonl"}]
    return tracer
