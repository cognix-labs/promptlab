from promptlab._utils import Utils
from promptlab.evaluator.evaluator import Evaluator
from rouge_score import rouge_scorer


class RougeScore(Evaluator):
    def __init__(
        self,
        rouge_type="rouge1",
        precision_threshold=0.5,
        recall_threshold=0.5,
        f1_score_threshold=0.5,
    ):
        """
        Initialize the RougeScore evaluator.

        Args:
            rouge_type (str): Type of ROUGE score to calculate (default: "rouge1").
            precision_threshold (float): Minimum acceptable precision (default: 0.5).
            recall_threshold (float): Minimum acceptable recall (default: 0.5).
            f1_score_threshold (float): Minimum acceptable F1 score (default: 0.5).
        """
        self.rouge_type = rouge_type
        self.precision_threshold = precision_threshold
        self.recall_threshold = recall_threshold
        self.f1_score_threshold = f1_score_threshold
        Utils.download_required_nltk_resources()

    def evaluate(self, data: dict):
        """
        Calculate the ROUGE score between the response and reference text.

        Args:
            data (dict): A dictionary containing:
                - response: The model's generated text
                - reference: The reference text to compare against

        Returns:
            float: The ROUGE F1 score for the specified rouge_type
        """
        completion = data["response"]
        reference = data["reference"]

        scorer = rouge_scorer.RougeScorer([self.rouge_type], use_stemmer=True)
        scores = scorer.score(reference, completion)
        rouge_scores = scores[self.rouge_type]

        return rouge_scores.fmeasure


rouge_score = RougeScore
