from promptlab.enums import ModelType
from promptlab.model.azure_openai import AzOpenAI, AzOpenAI_Embedding
from promptlab.model.model import EmbeddingModel
from promptlab.model.model import Model
from promptlab.model.ollama import Ollama, Ollama_Embedding
from promptlab.model.deepseek import DeepSeek, DeepSeek_Embedding
from promptlab.model.openrouter import OpenRouter, OpenRouter_Embedding
from promptlab.model.model import ModelConfig


class ModelFactory:
    @staticmethod
    def get_model(model_config: ModelConfig) -> Model:
        connection_type = model_config.type

        if connection_type == ModelType.AZURE_OPENAI.value:
            return AzOpenAI(model_config=model_config)
        if connection_type == ModelType.OLLAMA.value:
            return Ollama(model_config=model_config)
        if connection_type == ModelType.DEEPSEEK.value:
            return DeepSeek(model_config=model_config)
        if connection_type == ModelType.OPENROUTER.value:
            return OpenRouter(model_config=model_config)
        else:
            raise ValueError(f"Unknown connection type: {connection_type}")

    @staticmethod
    def get_embedding_model(model_config: ModelConfig) -> EmbeddingModel:
        connection_type = model_config.type

        if connection_type == ModelType.OLLAMA.value:
            return Ollama_Embedding(model_config=model_config)
        if connection_type == ModelType.AZURE_OPENAI.value:
            return AzOpenAI_Embedding(model_config=model_config)
        if connection_type == ModelType.DEEPSEEK.value:
            return DeepSeek_Embedding(model_config=model_config)
        if connection_type == ModelType.OPENROUTER.value:
            return OpenRouter_Embedding(model_config=model_config)
        else:
            raise ValueError(f"Unknown connection type: {connection_type}")
