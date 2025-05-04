import os
import sqlite3
from promptlab import PromptLab
from promptlab.model.ollama import Ollama, Ollama_Embedding
from promptlab.types import ModelConfig, PromptTemplate, Dataset

# Initialize PromptLab with SQLite storage
tracer_config = {"type": "sqlite", "db_file": "./promptlab.db"}
pl = PromptLab(tracer_config)

# Create a prompt template
prompt_template = PromptTemplate(
    name="essay_feedback",
    description="A prompt for generating feedback on essays",
    system_prompt="You are a helpful assistant who can provide feedback on essays.",
    user_prompt="""The essay topic is - <essay_topic>.
        The submitted essay is - <essay>
        Now write feedback on this essay.
        """,
)
try:
    pt = pl.asset.create(prompt_template)
except sqlite3.IntegrityError as e:
    print(f"Asset already exists: {e}")

# Create a dataset
dataset = Dataset(
    name="essay_samples",
    description="dataset for evaluating the essay_feedback prompt",
    file_path="./samples/data/essay_feedback.jsonl",
)
try:
    ds = pl.asset.create(dataset)
except sqlite3.IntegrityError as e:
    print(f"Asset already exists: {e}")

# Get assets
pt = pl.asset.get(
    asset_name="essay_feedback",
    version=0
)

ds = pl.asset.get(
    asset_name="essay_samples",
    version=0
)

# model instnace
model = Ollama(
            model_config = ModelConfig(model_deployment="llama3.2")
        )

embedding_model = Ollama_Embedding(
            model_config = ModelConfig(model_deployment="nomic-embed-text:latest")
        )

# Run an experiment
experiment_config = {
    "inference_model": model,
    "embedding_model": embedding_model,
    "prompt_template": pt,
    "dataset": ds,
    "evaluation": [
        {
            "metric": "semantic_similarity",
            "column_mapping": {"response": "$inference", "reference": "feedback"},
        },
        {
            "metric": "fluency",
            "column_mapping": {"response": "$inference"},
        },
    ],
}
pl.experiment.run(experiment_config)

# Start the PromptLab Studio to view results
pl.studio.start(8000)
