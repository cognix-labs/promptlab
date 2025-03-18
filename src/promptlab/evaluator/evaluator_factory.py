import os
from typing import Any
from ragas import SingleTurnSample
import ragas
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings

from promptlab.enums import EvalLibrary, ModelType
from promptlab.evaluator.evaluator import Evaluator
from promptlab.model.model_factory import ModelFactory
from promptlab.types import ModelConfig

class RagasMetricEval(Evaluator):

    def __init__(self, metric_class):

        self.metric_class = metric_class

    def evaluate(self, data: dict) -> str:

        sample = SingleTurnSample(**data)
        val = self.metric_class.single_turn_score(sample)

        return val
    
class EvaluatorFactory:
    
    @staticmethod
    def get_evaluator(eval_library: str, metric:str, model:ModelConfig, evaluator:Evaluator = None) -> Evaluator:
        
        if eval_library == EvalLibrary.RAGAS.value:
    
            if model.type == ModelType.AZURE_OPENAI.value:
                
                os.environ["AZURE_OPENAI_API_KEY"] = model.api_key

                evaluator_llm = LangchainLLMWrapper(AzureChatOpenAI(
                    openai_api_version=model.api_version,
                    azure_endpoint=str(model.endpoint),
                    azure_deployment=model.inference_model_deployment,
                    model=model.inference_model_deployment,
                    validate_base_url=False,
                ))

                evaluator_embeddings = LangchainEmbeddingsWrapper(AzureOpenAIEmbeddings(
                    openai_api_version=model.api_version,
                    azure_endpoint=str(model.endpoint),
                    azure_deployment=model.embedding_model_deployment,
                    model=model.embedding_model_deployment,
                ))

            if model.type == ModelType.OLLAMA.value:

                evaluator_llm = LangchainLLMWrapper(ChatOllama(model=model.inference_model_deployment))
                evaluator_embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(model=model.embedding_model_deployment))

            metric_params = {
                "LLMContextPrecisionWithoutReference": {"llm": evaluator_llm},
                "LLMContextPrecisionWithReference": {"llm": evaluator_llm},
                "NonLLMContextPrecisionWithReference": {},
                "LLMContextRecall": {"llm": evaluator_llm},
                "NonLLMContextRecall": {},
                "ContextEntityRecall": {"llm": evaluator_llm},
                "NoiseSensitivity": {"llm": evaluator_llm},
                "ResponseRelevancy": {"llm": evaluator_llm, "embeddings":evaluator_embeddings},
                "Faithfulness": {"llm": evaluator_llm},
                "FaithfulnesswithHHEM": {"llm": evaluator_llm},
                "FactualCorrectness": {"llm": evaluator_llm},
                "SemanticSimilarity": {"embeddings": evaluator_embeddings},
                "NonLLMStringSimilarity": {},
                "BleuScore": {},
                "RougeScore": {},
                "ExactMatch": {},
                "StringPresence": {},
                "DataCompyScore": {},
                "LLMSQLEquivalence": {"llm": evaluator_llm},
                "AspectCritic": {"llm": evaluator_llm},
                "SimpleCriteriaScore": {"llm": evaluator_llm},
                "SummarizationScore": {"llm": evaluator_llm},
            }
            constructor_params = metric_params.get(metric, {})

            metric_class = getattr(ragas.metrics, metric)
            metric_class = metric_class(**constructor_params)

            return RagasMetricEval(metric_class)    
        
        if eval_library == EvalLibrary.CUSTOM.value:
            inference_model = ModelFactory.get_model(model)
            evaluator.inference_model = inference_model
            return evaluator
        else:
            raise ValueError(f"Unknown evaluation strategy: {eval_library}")