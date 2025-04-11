from promptlab.evaluator.evaluator import Evaluator

class LengthEvaluator(Evaluator):
    
    def evaluate(self, data: dict):
        
        inference = data["response"]
        
        return len(str(inference))