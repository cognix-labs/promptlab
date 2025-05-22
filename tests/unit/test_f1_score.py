import pytest
from promptlab.evaluator.f1_score import F1Score


def test_f1_score_exact_match():
    """Test F1Score with exactly matching response and reference."""
    evaluator = F1Score()
    data = {"response": "This is a test", "reference": "This is a test"}
    score = evaluator.evaluate(data)
    assert score == 1.0  # Perfect match should yield a score of 1.0


def test_f1_score_partial_match():
    """Test F1Score with partially matching response and reference."""
    evaluator = F1Score()
    data = {"response": "This is a test", "reference": "This is a sample"}
    score = evaluator.evaluate(data)
    assert 0.0 < score < 1.0  # Partial match should be between 0 and 1


def test_f1_score_no_match():
    """Test F1Score with completely different response and reference."""
    evaluator = F1Score()
    data = {"response": "This is a test", "reference": "Something completely different"}
    score = evaluator.evaluate(data)
    assert score == 0.0  # No common tokens should yield a score of 0.0


def test_f1_score_empty_inputs():
    """Test F1Score with empty inputs."""
    evaluator = F1Score()
    data = {"response": "", "reference": "This is a test"}
    score = evaluator.evaluate(data)
    assert score == 0.0  # Empty response should yield a score of 0.0

    data = {"response": "This is a test", "reference": ""}
    score = evaluator.evaluate(data)
    assert score == 0.0  # Empty reference should yield a score of 0.0

    data = {"response": "", "reference": ""}
    score = evaluator.evaluate(data)
    assert score == 0.0  # Both empty should yield a score of 0.0


def test_f1_score_case_insensitivity():
    """Test F1Score is case insensitive."""
    evaluator = F1Score()
    data = {"response": "This is a test", "reference": "THIS IS A TEST"}
    score = evaluator.evaluate(data)
    assert score == 1.0  # Case-insensitive match should yield a score of 1.0