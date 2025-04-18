import asyncio
from promptlab import PromptLab
from promptlab.types import PromptTemplate, Dataset, ModelConfig
from promptlab.model.ollama import Ollama, Ollama_Embedding

async def main():
    # Initialize PromptLab with SQLite storage
    tracer_config = {
        "type": "sqlite",
        "db_file": "./promptlab.db"
    }
    pl = PromptLab(tracer_config)

    # Create a prompt template
    prompt_template = PromptTemplate(
        name="async_example",
        description="A prompt for testing async functionality",
        system_prompt="You are a helpful assistant who can provide concise answers.",
        user_prompt="Please answer this question: <question>"
    )
    pt = pl.asset.create(prompt_template)

    # Create a dataset
    dataset = Dataset(
        name="async_questions",
        description="Sample questions for async testing",
        file_path="./questions.jsonl"
    )
    ds = pl.asset.create(dataset)

    # Create model instances
    inference_model_config = ModelConfig(
        type="ollama",
        inference_model_deployment="llama2"
    )
    embedding_model_config = ModelConfig(
        type="ollama",
        embedding_model_deployment="llama2"
    )

    # Initialize model objects
    ollama = Ollama(model_config=inference_model_config)
    ollama_embedding = Ollama_Embedding(model_config=embedding_model_config)

    # Run an experiment asynchronously
    experiment_config = {
        "inference_model": ollama,
        "embedding_model": ollama_embedding,
        "prompt_template": pt,
        "dataset": ds,
        "evaluation": [
            {
                "type": "custom",
                "metric": "length",
                "column_mapping": {
                    "response": "$inference"
                }
            }
        ]
    }

    # Run the experiment asynchronously
    await pl.run_experiment_async(experiment_config)

    # Start the PromptLab Studio asynchronously
    await pl.start_studio_async(8000)

if __name__ == "__main__":
    asyncio.run(main())
