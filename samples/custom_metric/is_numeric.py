from promptlab.evaluator.evaluator import Evaluator

class IsNumericEvaluator(Evaluator):
    
    def evaluate(self, data: dict) -> str:
        inference = data.get("response")
        val = False
        if isinstance(inference, (int, float)):
            val = True
        elif isinstance(inference, str):
            try:
                float(inference)
                val = True
            except ValueError:
                pass
        
        return val