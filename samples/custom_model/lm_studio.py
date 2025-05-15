from openai import OpenAI
import asyncio

from promptlab.model.model import Model
from promptlab.types import InferenceResult, ModelConfig


class LmStudio(Model):
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)

        self.client = OpenAI(
            base_url=str(self.model_config.endpoint), api_key=self.model_config.api_key
        )

    def invoke(self, system_prompt: str, user_prompt: str) -> InferenceResult:
        """Synchronous invocation of the model"""
        payload = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        completion = self.client.chat.completions.create(
            model=self.model_config.model_deployment, messages=payload
        )

        latency_ms = 0
        inference = completion.choices[0].message.content
        prompt_token = 0
        completion_token = 0

        return InferenceResult(
            inference=inference,
            prompt_tokens=prompt_token,
            completion_tokens=completion_token,
            latency_ms=latency_ms,
        )
    
    async def ainvoke(self, system_prompt: str, user_prompt: str) -> InferenceResult:
        """Asynchronous invocation of the model"""
        # Since OpenAI's Python client doesn't have native async support in this version,
        # we'll run the synchronous method in an executor
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.invoke, system_prompt, user_prompt
        )
