from typing import List
import ollama
import asyncio

from promptlab.model.model import EmbeddingModel, Model, ModelResponse, ModelConfig


class Ollama(Model):
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)

        self.client = ollama
        self.model_name = self.model_config.name.split("/")[1]

    def invoke(self, system_prompt: str, user_prompt: str):
        payload = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        chat_completion = self.client.chat(model=self.model_name, messages=payload)

        latency_ms = chat_completion.total_duration / 1000000
        response = chat_completion.message.content
        prompt_token = chat_completion.eval_count
        completion_token = chat_completion.prompt_eval_count

        return ModelResponse(
            response=response,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms,
        )

    async def ainvoke(self, system_prompt: str, user_prompt: str) -> ModelResponse:
        """
        Asynchronous invocation of the Ollama model
        Note: Ollama doesn't have a native async API, so we run it in a thread pool
        """
        payload = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Run the synchronous Ollama call in a thread pool
        loop = asyncio.get_event_loop()
        chat_completion = await loop.run_in_executor(
            None,
            lambda: self.client.chat(model=self.model_name, messages=payload),
        )

        latency_ms = chat_completion.total_duration / 1000000
        response = chat_completion.message.content
        prompt_token = chat_completion.eval_count
        completion_token = chat_completion.prompt_eval_count

        return ModelResponse(
            response=response,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms,
        )


class Ollama_Embedding(EmbeddingModel):
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)

        self.client = ollama
        self.model_name = self.model_config.name.split("/")[1]

    def __call__(self, text: str) -> List[float]:
        embedding = self.client.embed(
            model=self.model_name,
            input=text,
        )["embeddings"]

        return embedding


ollama_completion = Ollama
ollama_embedding = Ollama_Embedding
