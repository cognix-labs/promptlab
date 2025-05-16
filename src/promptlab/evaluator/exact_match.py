from promptlab.evaluator.evaluator import Evaluator


class ExactMatch(Evaluator):
    def evaluate(self, data: dict):
        inference = data["response"]
        reference = data["reference"]

        return inference == reference


exact_match = ExactMatch
