# Async Example

This example demonstrates how to use the async functionality in PromptLab with various models including local models via Ollama and cloud models via OpenRouter.

## Overview

PromptLab now supports asynchronous operations for:

1. Running experiments
2. Invoking models
3. Starting the PromptLab Studio

This allows for more efficient processing, especially when dealing with large datasets or multiple concurrent operations.

## Prerequisites

Before running these examples, make sure you have:

1. Installed all required dependencies using the requirements.txt file:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up your API keys in the `.env` file

## Running the Example

### Using Ollama (Local Models)

To run this example with Ollama (local models):

```bash
cd samples/async_example
python async_example.py
```

### Using OpenRouter Models

To run this example with models available through OpenRouter:

1. First, copy the example environment file and add your OpenRouter API key:

```bash
cp .env.example .env
# Edit .env to add your OpenRouter API key
```

2. Run the example with OpenRouter:

```bash
python async_openrouter.py
```

You can also specify parameters via command line:

```bash
python async_openrouter.py --model "openai/gpt-4" --port 8000 --api-key "your_openrouter_api_key"
```

Available command-line options:

- `--model`: OpenRouter model to use for inference (e.g., "openai/gpt-4", "anthropic/claude-3-opus", "deepseek/deepseek-chat-v3-0324")
- `--embedding-model`: OpenRouter model to use for embeddings
- `--port`: Port for PromptLab Studio
- `--api-key`: OpenRouter API key

This will:

1. Create a prompt template and dataset
2. Create a custom evaluator for measuring response length
3. Run an experiment asynchronously with OpenRouter models
4. Start the PromptLab Studio asynchronously

## Key Features

### Async Model Invocation

Models now support asynchronous invocation through the `ainvoke` method:

```python
# Synchronous invocation
result = model.invoke(system_prompt, user_prompt)

# Asynchronous invocation
result = await model.ainvoke(system_prompt, user_prompt)
```

### Async Experiment Execution

Experiments can be run asynchronously:

```python
# Synchronous execution
pl.experiment.run(experiment_config)

# Asynchronous execution
await pl.experiment.run_async(experiment_config)
```

### Async Studio

The PromptLab Studio can be started asynchronously:

```python
# Synchronous start
pl.studio.start(8000)

# Asynchronous start
await pl.studio.start_async(8000)
```

### Custom Evaluators

This example also demonstrates how to use custom evaluators with async functionality:

```python
# Define a custom evaluator
class LengthEvaluator(Evaluator):
    def evaluate(self, data: dict) -> str:
        response = data.get("response", "")
        return str(len(response))

# Create an instance and use it in the experiment
length_evaluator = LengthEvaluator()

experiment_config = {
    # ...
    "evaluation": [
        {
            "metric": "LengthEvaluator",
            "column_mapping": {
                "response": "$inference"
            },
            "evaluator": length_evaluator
        }
    ]
}
```

## Benefits

- **Improved Performance**: Process multiple requests concurrently
- **Better Resource Utilization**: Make efficient use of system resources
- **Responsive Applications**: Keep your application responsive while processing large datasets
- **Scalability**: Handle more concurrent operations
- **Model Flexibility**: Use local models (Ollama) or cloud models via OpenRouter

## Using OpenRouter Models

This example demonstrates how to use various AI models through OpenRouter's API. OpenRouter provides a unified API for accessing a wide range of AI models from different providers.

## Troubleshooting

If you encounter errors when running the examples, check the following:

1. **Flask Async Support**: If you see errors like `RuntimeError: Install Flask with the 'async' extra in order to use async views`, install Flask with async support:
   ```bash
   pip install "flask[async]"
   ```

2. **Dataset Loading**: Make sure the `questions.jsonl` file exists in the correct location.

3. **API Keys**: Ensure you have set valid API keys in the `.env` file.

### Configuration

To use OpenRouter models, you need to:

1. Get an API key from [OpenRouter](https://openrouter.ai/)
2. Set the API key in the `.env` file or pass it via command line
3. Choose an OpenRouter model (default is `openai/gpt-3.5-turbo`)

### Available OpenRouter Models

Check the [OpenRouter documentation](https://openrouter.ai/models) for the most up-to-date list of available models.
