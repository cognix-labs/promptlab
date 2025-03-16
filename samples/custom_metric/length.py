from promptlab.evaluator.evaluator import Evaluator

class LengthEvaluator(Evaluator):
    
    def evaluate(self, inference: str):
       
        return len(str(inference))