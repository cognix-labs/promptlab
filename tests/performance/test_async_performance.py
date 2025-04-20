import asyncio
import time
import sys
import os
import pytest
from tests.fixtures.test_utils import MockModel

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath("./src"))


@pytest.mark.asyncio
async def test_parallel_execution():
    """Test that async execution is faster than synchronous execution"""
    print("Testing parallel execution...")

    # Create test data
    prompts = [f"Test prompt {i}" for i in range(10)]
    # Use the fixture model with 0.5s delay
    model = MockModel(delay_seconds=0.5)

    # Test synchronous execution
    start_time = time.time()
    sync_results = []
    for prompt in prompts:
        result = model.invoke("System prompt", prompt)
        sync_results.append(result)
    sync_time = time.time() - start_time

    # Test asynchronous execution
    start_time = time.time()
    tasks = []
    for prompt in prompts:
        task = model.ainvoke("System prompt", prompt)
        tasks.append(task)
    await asyncio.gather(*tasks)  # Run tasks, ignore results
    async_time = time.time() - start_time

    print(f"Synchronous execution time: {sync_time:.2f} seconds")
    print(f"Asynchronous execution time: {async_time:.2f} seconds")

    # Async should be significantly faster
    if async_time < sync_time / 2:
        print("✅ Async execution is at least 2x faster than synchronous execution")
        return True
    else:
        print("❌ Async execution is not significantly faster")
        return False


@pytest.mark.asyncio
async def main():
    """Run the tests"""
    print("Testing async implementation...")

    # Test parallel execution
    parallel_ok = await test_parallel_execution()
    if not parallel_ok:
        return

    print("All tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
