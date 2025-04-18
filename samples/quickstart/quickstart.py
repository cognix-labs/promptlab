from promptlab import PromptLab
from promptlab.model.ollama import Ollama, Ollama_Embedding
from promptlab.types import PromptTemplate, Dataset

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
pt = pl.asset.create(prompt_template)

# Create a dataset
dataset = Dataset(
    name="essay_samples",
    description="dataset for evaluating the essay_feedback prompt",
    file_path="./samples/data/essay_feedback.jsonl",
)
ds = pl.asset.create(dataset)

# model instnace
model_config = {"type": "ollama", "model_deployment": "llama3.2"}
ollama = Ollama(model_config=model_config)

embedding_model_config = {
    "type": "ollama",
    "model_deployment": "nomic-embed-text:latest",
}
ollama_embedding = Ollama_Embedding(model_config=embedding_model_config)

# Run an experiment
experiment_config = {
    "inference_model": ollama,
    "embedding_model": ollama_embedding,
    "prompt_template": pt,
    "dataset": ds,
    "evaluation": [
        {
            "metric": "SemanticSimilarity",
            "column_mapping": {"response": "$inference", "reference": "feedback"},
        },
        {
            "metric": "Fluency",
            "column_mapping": {"response": "$inference"},
        },
    ],
}
pl.experiment.run(experiment_config)

# Start the PromptLab Studio to view results
pl.studio.start(8000)
