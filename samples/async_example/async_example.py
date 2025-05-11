import asyncio
from promptlab import PromptLab
from promptlab.types import PromptTemplate, Dataset, ModelConfig
from promptlab.model.ollama import Ollama, Ollama_Embedding
from custom_evaluator import LengthEvaluator


async def main():
    # Initialize PromptLab with SQLite storage
    tracer_config = {"type": "sqlite", "db_file": "./promptlab.db"}
    pl = PromptLab(tracer_config)

    # Create a prompt template
    prompt_name = "async_example"
    prompt_template = PromptTemplate(
        name=prompt_name,
        description="A prompt for testing async functionality",
        system_prompt="You are a helpful assistant who can provide concise answers.",
        user_prompt="Please answer this question: <question>",
    )
    pt = pl.asset.create(prompt_template)

    # Create a dataset
    dataset_name = "async_questions"
    dataset = Dataset(
        name=dataset_name,
        description="Sample questions for async testing",
        file_path="./samples/async_example/questions.jsonl",
    )
    ds = pl.asset.create(dataset)

    # Retrieve assets
    pt = pl.asset.get(asset_name = prompt_name, version=0)
    ds = pl.asset.get(asset_name = dataset_name, version=0)

    # Initialize model objects
    inference_model = Ollama(model_config = ModelConfig(model_deployment="llama3.2"))
    embedding_model = Ollama_Embedding(model_config = ModelConfig(model_deployment="llama3.2"))

    length_evaluator = LengthEvaluator()

    # Run an experiment asynchronously
    experiment_config = {
        "inference_model": inference_model,
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

    # Start the PromptLab Studio asynchronously
    await pl.studio.start_async(8000)


if __name__ == "__main__":
    asyncio.run(main())
