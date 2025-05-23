from rouge_score import rouge_scorer
from abc import ABC, abstractmethod


# Simplified version of our evaluator for testing
class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, data: dict):
        pass


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
        """
        self.rouge_type = rouge_type
        self.precision_threshold = precision_threshold
        self.recall_threshold = recall_threshold
        self.f1_score_threshold = f1_score_threshold

    def evaluate(self, data: dict):
        """
        Calculate the ROUGE score between the response and reference text.
        """
        inference = data["response"]
        reference = data["reference"]

        # Initialize a ROUGE scorer with the specified rouge_type
        scorer = rouge_scorer.RougeScorer([self.rouge_type], use_stemmer=True)

        # Calculate ROUGE scores
        scores = scorer.score(reference, inference)

        # Extract the scores for the specified rouge_type
        rouge_scores = scores[self.rouge_type]

        # Return the F1 score as the primary score
        return rouge_scores.fmeasure


def test_rouge_score():
    # Test with perfect match
    evaluator = RougeScore()
    data = {
        "response": "The quick brown fox jumps over the lazy dog.",
        "reference": "The quick brown fox jumps over the lazy dog.",
    }

    score = evaluator.evaluate(data)
    print(f"Perfect match score: {score}")
    assert score == 1.0

    # Test with partial match
    data = {
        "response": "The quick brown fox jumps over the lazy dog.",
        "reference": "The fast brown fox jumps over the sleeping dog.",
    }

    score = evaluator.evaluate(data)
    print(f"Partial match score: {score}")
    assert 0 < score < 1.0

    # Test with no match
    data = {
        "response": "The quick brown fox jumps over the lazy dog.",
        "reference": "Completely different text with no matching words.",
    }

    score = evaluator.evaluate(data)
    print(f"No match score: {score}")
    assert score < 0.2

    # Test with rouge2
    evaluator2 = RougeScore(rouge_type="rouge2")
    data = {
        "response": "The quick brown fox jumps over the lazy dog.",
        "reference": "The quick brown fox jumps over the lazy dog.",
    }

    score2 = evaluator2.evaluate(data)
    print(f"Rouge2 score: {score2}")
    assert score2 == 1.0

    # Test with rougeL
    evaluatorL = RougeScore(rouge_type="rougeL")
    score_L = evaluatorL.evaluate(data)
    print(f"RougeL score: {score_L}")
    assert score_L == 1.0

    # Test with custom thresholds
    evaluator_custom = RougeScore(
        precision_threshold=0.7, recall_threshold=0.8, f1_score_threshold=0.75
    )
    assert evaluator_custom.precision_threshold == 0.7
    assert evaluator_custom.recall_threshold == 0.8
    assert evaluator_custom.f1_score_threshold == 0.75

    print("All tests passed!")


if __name__ == "__main__":
    test_rouge_score()
