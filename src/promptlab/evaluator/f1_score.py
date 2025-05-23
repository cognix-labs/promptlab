from promptlab._utils import Utils
from promptlab.evaluator.evaluator import Evaluator
from nltk.tokenize import word_tokenize


class F1Score(Evaluator):
    def __init__(self):
        Utils.download_required_nltk_resources()

    def evaluate(self, data: dict):
        """
        Calculate the F1 score between the response and reference texts.

        F1 score is the harmonic mean of precision and recall.
        Precision is the proportion of shared words relative to total words in response.
        Recall is the proportion of shared words relative to total words in reference.

        Args:
            data: A dictionary containing 'response' and 'reference' keys.

        Returns:
            A float between 0 and 1 representing the F1 score.
        """
        response = data["response"]
        reference = data["reference"]

        response_tokens = set(word_tokenize(response.lower()))
        reference_tokens = set(word_tokenize(reference.lower()))

        # Handle edge case of empty inputs
        if not response_tokens or not reference_tokens:
            return 0.0

        common_tokens = response_tokens.intersection(reference_tokens)

        precision = len(common_tokens) / len(response_tokens) if response_tokens else 0
        recall = len(common_tokens) / len(reference_tokens) if reference_tokens else 0

        # Calculate F1 score as harmonic mean of precision and recall
        if precision + recall > 0:
            f1_score = 2 * precision * recall / (precision + recall)
        else:
            f1_score = 0.0

        return f1_score


f1_score = F1Score
