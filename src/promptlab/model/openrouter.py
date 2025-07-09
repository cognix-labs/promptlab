import time
from typing import List
from openai import OpenAI
from openai import AsyncOpenAI

from promptlab.model.model import Model, EmbeddingModel
from promptlab.types import ModelResponse, ModelConfig


class OpenRouter(Model):
    """
    OpenRouter model implementation that provides access to various AI models
    through the OpenRouter API.
    """

    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)
        self.client = OpenAI(
            api_key=model_config.api_key, base_url=str(model_config.endpoint)
        )
        self.async_client = AsyncOpenAI(
            api_key=model_config.api_key, base_url=str(model_config.endpoint)
        )
        self.model_name = self.model_config.name.split("/")[1]

    def invoke(self, system_prompt: str, user_prompt: str):
        """
        Synchronous invocation of the OpenRouter model
        """
        payload = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Add OpenRouter-specific headers
        extra_headers = {
            "HTTP-Referer": "https://promptlab.local",  # Replace with your actual site URL
            "X-Title": "PromptLab",  # Replace with your actual site name
        }

        start_time = time.time()
        chat_completion = self.client.chat.completions.create(
            model=self.model_name, messages=payload, extra_headers=extra_headers
        )
        end_time = time.time()
        response = chat_completion.choices[0].message.content

        # Some providers might not return usage info
        prompt_token = getattr(chat_completion.usage, "prompt_tokens", 0)
        completion_token = getattr(chat_completion.usage, "completion_tokens", 0)

        # Calculate latency
        latency_ms = (end_time - start_time) * 1000

        return ModelResponse(
            response=response,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms,
        )

    async def ainvoke(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        """
        Asynchronous invocation of the OpenRouter model
        """
        payload = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Add OpenRouter-specific headers
        extra_headers = {
            "HTTP-Referer": "https://promptlab.local",  # Replace with your actual site URL
            "X-Title": "PromptLab",  # Replace with your actual site name
        }

        start_time = time.time()

        chat_completion = await self.async_client.chat.completions.create(
            model=self.model_name, messages=payload, extra_headers=extra_headers
        )

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000

        response = chat_completion.choices[0].message.content

        # Some providers might not return usage info
        prompt_token = getattr(chat_completion.usage, "prompt_tokens", 0)
        completion_token = getattr(chat_completion.usage, "completion_tokens", 0)

        return ModelResponse(
            response=response,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms,
        )


class OpenRouter_Embedding(EmbeddingModel):
    """
    OpenRouter embedding model implementation that provides access to various
    embedding models through the OpenRouter API.
    """

    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)

        self.client = OpenAI(
            api_key=model_config.api_key, base_url=str(model_config.endpoint)
        )
        self.model_name = self.model_config.name.split("/")[1]

    def __call__(self, text: str) -> List[float]:
        # Add OpenRouter-specific headers
        extra_headers = {
            "HTTP-Referer": "https://promptlab.local",
            "X-Title": "PromptLab",
        }

        try:
            # Try to use the embedding API
            response = self.client.embeddings.create(
                model=self.model_name,
                input=text,
                extra_headers=extra_headers,
            )
            embedding = response.data[0].embedding
        except Exception as e:
            # If embedding fails, return a dummy embedding
            # This is a fallback for models that don't support embeddings
            print(f"Warning: Embedding failed with error: {e}")
            # Return a dummy embedding of 1536 dimensions (common size)
            import numpy as np

            embedding = np.zeros(1536).tolist()

        return embedding


openrouter_completion = OpenRouter
openrouter_embedding = OpenRouter_Embedding
