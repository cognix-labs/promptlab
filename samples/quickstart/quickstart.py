import asyncio
from promptlab import PromptLab
from promptlab.types import PromptTemplate, Dataset

# Initialize PromptLab with local tracer
tracer_config = {"type": "local", "db_file": "./promptlab.db"}

pl = PromptLab(tracer_config)

# Create a prompt template
prompt_name = "essay_feedback"
prompt_description = "A prompt for generating feedback on essays"
system_prompt = "You are a helpful assistant who can provide feedback on essays."
user_prompt = """The essay topic is - <essay_topic>.
               The submitted essay is - <essay>
               Now write feedback on this essay."""
prompt_template = PromptTemplate(
    name=prompt_name,
    description=prompt_description,
    system_prompt=system_prompt,
    user_prompt=user_prompt,
)
pt = pl.asset.create(prompt_template)

# Create a dataset
dataset_name = "essay_samples"
dataset_description = "dataset for evaluating the essay_feedback prompt"
dataset_file_path = "./samples/data/essay_feedback.jsonl"
dataset = Dataset(
    name=dataset_name, description=dataset_description, file_path=dataset_file_path
)
ds = pl.asset.create(dataset)

# Retrieve assets
pt = pl.asset.get(asset_name=prompt_name, version=0)
ds = pl.asset.get(asset_name=dataset_name, version=0)

# Run an experiment
experiment_config = {
    "name": "quickstart_experimet",
    "completion_model_config": {"name": "ollama/llama3.2", "type": "completion"},
    "embedding_model_config": {
        "name": "ollama/nomic-embed-text:latest",
        "type": "embedding",
    },
    "prompt_template": pt,
    "dataset": ds,
    "evaluation": [
        {
            "metric": "semantic_similarity",
            "column_mapping": {"response": "$completion", "reference": "feedback"},
        },
        {
            "metric": "relevance",
            "column_mapping": {
                "response": "$completion",
                "query": "essay_topic",
            },
        },
    ],
}

# Uncomment the following line to run the experiment synchronously
# pl.experiment.run(experiment_config)

# Run the experiment asynchronously
asyncio.run(pl.experiment.run_async(experiment_config))

# Start the PromptLab Studio to view results
asyncio.run(pl.studio.start_async(8000))
