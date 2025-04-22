import asyncio
import os
import time
import argparse
import dotenv
from promptlab import PromptLab
from promptlab.types import PromptTemplate, Dataset, ModelConfig
from promptlab.model.deepseek import DeepSeek, DeepSeek_Embedding
from custom_evaluator import LengthEvaluator

# Load environment variables from .env file
dotenv.load_dotenv()


async def main():
    # Initialize PromptLab with SQLite storage
    tracer_config = {"type": "sqlite", "db_file": "./promptlab.db"}
    pl = PromptLab(tracer_config)

    # Create a prompt template
    prompt_template = PromptTemplate(
        name="async_deepseek_example_"
        + str(int(time.time())),  # Add timestamp to make name unique
        description="A prompt for testing async functionality with DeepSeek",
        system_prompt="You are a helpful assistant who can provide concise answers.",
        user_prompt="Please answer this question: <question>",
    )
    pt = pl.asset.create(prompt_template)

    # Create a dataset
    dataset = Dataset(
        name="async_questions_"
        + str(int(time.time())),  # Add timestamp to make name unique
        description="Sample questions for async testing",
        file_path="./questions.jsonl",
    )
    ds = pl.asset.create(dataset)

    # Create DeepSeek model instance using OpenRouter
    # Get API key from environment variable
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable is not set. Please set it in the .env file."
        )

    # Get model name from environment variable or use default
    model_name = os.environ.get("DEEPSEEK_MODEL", "deepseek/deepseek-chat-v3-0324")

    inference_model_config = ModelConfig(
        type="deepseek",
        api_key=openrouter_api_key,
        endpoint="https://openrouter.ai/api/v1",
        inference_model_deployment=model_name,
    )

    # Initialize model object
    deepseek_model = DeepSeek(model_config=inference_model_config)

    # Create embedding model config
    # Get embedding model name from environment variable or use the same as inference model
    embedding_model_name = os.environ.get("DEEPSEEK_EMBEDDING_MODEL", model_name)

    embedding_model_config = ModelConfig(
        type="deepseek",
        api_key=openrouter_api_key,
        endpoint="https://openrouter.ai/api/v1",
        embedding_model_deployment=embedding_model_name,
    )

    # Initialize embedding model
    embedding_model = DeepSeek_Embedding(model_config=embedding_model_config)

    # Create the length evaluator instance
    length_evaluator = LengthEvaluator()

    # Run an experiment asynchronously
    experiment_config = {
        "inference_model": deepseek_model,
        "embedding_model": embedding_model,
        "prompt_template": pt,
        "dataset": ds,
        "evaluation": [
            {
                "metric": "LengthEvaluator",
                "column_mapping": {"response": "$inference"},
                "evaluator": length_evaluator,
            }
        ],
    }

    # Run the experiment asynchronously
    await pl.experiment.run_async(experiment_config)

    # Get port from environment variable or use default
    port = int(os.environ.get("PROMPTLAB_PORT", 8000))

    # Start the PromptLab Studio asynchronously
    await pl.studio.start_async(port)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run PromptLab in async mode with DeepSeek models"
    )
    parser.add_argument("--model", type=str, help="DeepSeek model name")
    parser.add_argument(
        "--embedding-model", type=str, help="DeepSeek embedding model name"
    )
    parser.add_argument("--port", type=int, help="Port for PromptLab Studio")
    parser.add_argument("--api-key", type=str, help="OpenRouter API key")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Set environment variables from command line arguments if provided
    if args.model:
        os.environ["DEEPSEEK_MODEL"] = args.model
    if args.embedding_model:
        os.environ["DEEPSEEK_EMBEDDING_MODEL"] = args.embedding_model
    if args.port:
        os.environ["PROMPTLAB_PORT"] = str(args.port)
    if args.api_key:
        os.environ["OPENROUTER_API_KEY"] = args.api_key

    asyncio.run(main())
