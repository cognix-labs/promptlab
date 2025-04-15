from typing import Any
from openai import OpenAI

from promptlab.model.model import EmbeddingModel, Model
from promptlab.types import EmbeddingModelConfig, InferenceResult, InferenceModelConfig

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
    
# class LmStudio_Embedding(EmbeddingModel):

#     def __init__(self, model_config: EmbeddingModelConfig):

#         super().__init__(model_config)

#         self.client = AzureOpenAI(
#             api_key = self.config.api_key,  
#             azure_endpoint=str(self.config.endpoint)
#         )    

#     def __call__(self, text: str) -> Any:
#         embedding = self.client.embed(
#                     model=self.model_config.embedding_model_deployment,
#                     input=text,
#                     )["embeddings"]

#         return embedding