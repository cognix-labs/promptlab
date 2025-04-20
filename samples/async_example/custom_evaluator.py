from promptlab.evaluator.evaluator import Evaluator


class LengthEvaluator(Evaluator):
    """
    A simple evaluator that measures the length of the response
    """

    def evaluate(self, data: dict) -> str:
        """
        Evaluate the length of the response
        """
        response = data.get("response", "")
        return str(len(response))
