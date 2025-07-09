from promptlab.evaluator.evaluator import Evaluator


class ExactMatch(Evaluator):
    def evaluate(self, data: dict):
        completion = data["response"]
        reference = data["reference"]

        return completion == reference


exact_match = ExactMatch
