from typing import Any
import ollama

from promptlab.model.model import EmbeddingModel, Model
from promptlab.types import EmbeddingModelConfig, InferenceResult, InferenceModelConfig

class Ollama(Model):

    def __init__(self, model_config: InferenceModelConfig):

        super().__init__(model_config)

        self.model_config = model_config
        self.client = ollama
        
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

        chat_completion = self.client.chat(
            model=self.model_config.inference_model_deployment, 
            messages=payload
        )
        
        latency_ms = chat_completion.total_duration
        inference = chat_completion.message.content
        prompt_token = chat_completion.eval_count
        completion_token = chat_completion.prompt_eval_count

        return InferenceResult(
            inference=inference,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms
        )
    
class Ollama_Embedding(EmbeddingModel):

    def __init__(self, model_config: EmbeddingModelConfig):

        super().__init__(model_config)

        self.model_config = model_config
        self.client = ollama
    
    def __call__(self, text: str) -> Any:
        embedding = self.client.embed(
                    model=self.model_config.embedding_model_deployment,
                    input=text,
                    )["embeddings"]

        return embedding