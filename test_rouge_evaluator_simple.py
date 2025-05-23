import sys
import os

# Add the src directory to the path so we can import promptlab modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from promptlab.evaluator.rouge import RougeScore


def test_rouge_evaluator():
    # Create evaluator
    evaluator = RougeScore()

    # Test with perfect match
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

    # Test with different types
    evaluator_rouge2 = RougeScore(rouge_type="rouge2")
    score_rouge2 = evaluator_rouge2.evaluate(
        {
            "response": "The quick brown fox jumps over the lazy dog.",
            "reference": "The quick brown fox jumps over the lazy dog.",
        }
    )
    print(f"Rouge2 score: {score_rouge2}")
    assert score_rouge2 == 1.0

    print("All tests passed!")


if __name__ == "__main__":
    test_rouge_evaluator()
