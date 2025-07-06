from promptlab.evaluator.evaluator import Evaluator


class LengthEvaluator(Evaluator):
    def evaluate(self, data: dict):
        completion = data["response"]

        return len(str(completion))
