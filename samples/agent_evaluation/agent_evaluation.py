from promptlab import PromptLab
from promptlab.types import ModelResponse, Dataset


# Replace the implementation of the target function with coe that calls your agent/API and returns a ModelResponse.
def target(inputs: dict) -> ModelResponse:
    topic = inputs["essay_topic"]
    essay = inputs["essay"]

    return ModelResponse(
        response="This is a dummy response function that returns a static response.",
        prompt_tokens=0,
        completion_tokens=0,
        latency_ms=0,
    )


# Initialize PromptLab with SQLite storage
tracer_config = {"type": "sqlite", "db_file": "./promptlab.db"}
pl = PromptLab(tracer_config)

# Create a dataset
dataset_name = "essay_samples"
dataset_description = "dataset for evaluating the essay_feedback prompt"
dataset_file_path = "./samples/data/essay_feedback.jsonl"
dataset = Dataset(
    name=dataset_name, description=dataset_description, file_path=dataset_file_path
)
ds = pl.asset.create(dataset)

# Retrieve assets
ds = pl.asset.get(asset_name=dataset_name, version=0)

# Run an experiment
experiment_config = {
    "name": "demo_target_evaluation",
    "agent_proxy": target,
    "dataset": ds,
    "evaluation": [
        {
            "metric": "exact_match",
            "column_mapping": {
                "response": "$inference",
                "reference": "feedback",
            },
        },
    ],
}
pl.experiment.run(experiment_config)

# Start the PromptLab Studio to view results
pl.studio.start(8000)
