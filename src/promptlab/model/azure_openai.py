from typing import Any
from openai import AzureOpenAI

from promptlab.model.model import EmbeddingModel, Model, InferenceResult, ModelConfig
# from promptlab.types import InferenceResult, ModelConfig
import time


class AzOpenAI(Model):

    def __init__(self, model_config: ModelConfig):

        super().__init__(model_config)
        
        self.client = AzureOpenAI(
            api_key=model_config.api_key,  
            api_version=model_config.api_version,
            azure_endpoint=str(model_config.endpoint)
        )
        
    def invoke(self, system_prompt: str, user_prompt: str):

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

        start_time = time.time()

        chat_completion = self.client.chat.completions.create(
            model=self.config.model_deployment, 
            messages=payload
        )
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        inference = chat_completion.choices[0].message.content
        prompt_token = chat_completion.usage.prompt_tokens
        completion_token = chat_completion.usage.completion_tokens

        return InferenceResult(
            inference=inference,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms
        )
    
class AzOpenAI_Embedding(EmbeddingModel):

    def __init__(self, model_config: ModelConfig):

        super().__init__(model_config)

        self.client = AzureOpenAI(
            api_key=model_config.api_key,  
            api_version=model_config.api_version,
            azure_endpoint=str(model_config.endpoint)
        )
    
    def __call__(self, text: str) -> Any:
        
        embedding = self.client.embeddings.create(
                                                    input =text, 
                                                    model=self.config.model_deployment
                                                 ).data[0].embedding

        return embedding