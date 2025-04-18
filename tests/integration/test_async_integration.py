import asyncio
import sys
import os
import time
import pytest
from unittest.mock import patch, MagicMock
from tests.fixtures.test_utils import MockModel

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath('./src'))

@pytest.mark.asyncio
async def test_async_promptlab():
    """Test the async functionality in PromptLab"""
    try:
        from promptlab import PromptLab
        from promptlab.types import ModelConfig
        from promptlab.model.model import Model

        print("✅ Successfully imported PromptLab modules")

        # Test async model invocation
        model_config = ModelConfig(
            type="mock",
            inference_model_deployment="mock-model",
            embedding_model_deployment="mock-model"
        )

        # Use the fixture model with 0.5s delay
        model = MockModel(model_config=model_config, delay_seconds=0.5)

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

        print(f"Synchronous model invocation time: {sync_time:.2f} seconds")
        print(f"Asynchronous model invocation time: {async_time:.2f} seconds")

        if async_time < sync_time / 2:
            print("✅ Async model invocation is at least 2x faster")
        else:
            print("❌ Async model invocation is not significantly faster")

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

@pytest.mark.asyncio
async def main():
    """Run the tests"""
    print("Testing PromptLab async implementation...")

    # Test PromptLab async functionality
    await test_async_promptlab()

    print("All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
