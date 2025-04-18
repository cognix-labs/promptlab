from promptlab.evaluator.evaluator import Evaluator
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics._factual_correctness import FactualCorrectness
from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper

class RagasFactualCorrectness(Evaluator):
    
    def evaluate(self, data: dict):

        inference = data["response"]
        reference = data["reference"]
        
        sample = SingleTurnSample(
            response=inference,
            reference=reference
        )
        
        evaluator_llm = LangchainLLMWrapper(ChatOllama(model=self.inference.model_config.inference_model_deployment))

        scorer = FactualCorrectness(llm = evaluator_llm)
        return scorer.single_turn_score(sample)