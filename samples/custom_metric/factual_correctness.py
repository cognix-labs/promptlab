from promptlab.evaluator.evaluator import Evaluator
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics._factual_correctness import FactualCorrectness
from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper


class RagasFactualCorrectness(Evaluator):
    def evaluate(self, data: dict):
        completion = data["response"]
        reference = data["reference"]

        sample = SingleTurnSample(response=completion, reference=reference)

        evaluator_llm = LangchainLLMWrapper(
            ChatOllama(model=self.completion.model_config.model_deployment)
        )

        scorer = FactualCorrectness(llm=evaluator_llm)
        return scorer.single_turn_score(sample)
