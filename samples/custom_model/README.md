# Custom Metric

This sample ([custom_model.py](custom_model.py)) demonstrates how to use PromptLab to bring your own model to PromptLab. Here we shall use LMStudio API to build a new model class.

## Creating custom model 

The following code snippet implements a LMStudio based model.

    class LmStudio(Model):
        def __init__(self, model_config: ModelConfig):
            super().__init__(model_config)

            self.client = OpenAI(base_url=str(self.model_config.endpoint), api_key=self.model_config.api_key)

        def invoke(self, system_prompt: str, user_prompt: str) -> ModelResponse:
            """Synchronous invocation of the model"""
            payload = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            completion = self.client.chat.completions.create(
                model=self.model_config.model_deployment, messages=payload
            )

            latency_ms = 0
            response = completion.choices[0].message.content
            prompt_token = 0
            completion_token = 0

            return ModelResponse(
                response=response,
                prompt_tokens=prompt_token,
                completion_tokens=completion_token,
                latency_ms=latency_ms,
            )
        
        async def ainvoke(self, system_prompt: str, user_prompt: str) -> ModelResponse:
            """Asynchronous invocation of the model"""
            # Since OpenAI's Python client doesn't have native async support in this version,
            # we'll run the synchronous method in an executor
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, self.invoke, system_prompt, user_prompt
            )

## Using custom model

The following code snippet demonstrate how to use the custom model in the experiment.

    lmstudio = LmStudio(model_config = ModelConfig(model_deployment="llama-3.2-3b-instruct", api_key="lm-studio", api_version="v1", endpoint="http://localhost:1234/v1"))
    ollama_embedding = Ollama_Embedding(model_config = ModelConfig(model_deployment="nomic-embed-text:latest"))

    # Run an experiment
    experiment_config = {
        "inference_model": lmstudio,
        "embedding_model": ollama_embedding,
        "prompt_template": pt,
        "dataset": ds,
        "evaluation": [
            {
                "metric": "Fluency",
                "column_mapping": {"response": "$inference"},
            },
        ],
    }
    pl.experiment.run(experiment_config)