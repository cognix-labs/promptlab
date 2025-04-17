# Custom Metric

This sample ([custom_metric.py](custom_model.py)) demonstrates how to use PromptLab to bring your own model to PromptLab. Here we shall use LMStudio API to build a new model class.

## Creating custom model 

The following code snippet implements a LMStudio based model.

class LmStudio(Model):

    def __init__(self, model_config: InferenceModelConfig):

        super().__init__(model_config)

        self.client = OpenAI(base_url=str(self.config.endpoint), api_key=self.config.api_key)

    def __call__(self, system_prompt: str, user_prompt: str)->InferenceResult:

        payload = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        completion = self.client.chat.completions.create(
            model=self.config.model_deployment,
            messages=payload
        )
       
        latency_ms = 0
        inference = completion.choices[0].message.content
        prompt_token = 0
        completion_token = 0

        return InferenceResult(
            inference=inference,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms
        )

## Using custom model

The following code snippet demonstrate how to use the custom model in the experiment.

    experiment_config = {
        "inference_model" : lmstudio,
        "embedding_model" : ollama_embedding,
        "prompt_template": pt,
        "dataset": ds,
        "evaluation": [
                {
                    "metric": "Fluency",
                    "column_mapping": {
                        "response":"$inference"
                    },
                },                
            ],    
    }
    pl.experiment.run(experiment_config)