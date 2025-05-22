import pytest
from promptlab.evaluator.rouge import RougeScore


def test_rouge_score_basic():
    """Test basic functionality of RougeScore evaluator."""
    # Setup
    evaluator = RougeScore()
    data = {
        "response": "The quick brown fox jumps over the lazy dog.",
        "reference": "The quick brown fox jumps over the lazy dog."
    }
    
    # Execute
    score = evaluator.evaluate(data)
    
    # Assert
    assert score == 1.0, "Perfect match should give score of 1.0"


def test_rouge_score_partial_match():
    """Test RougeScore with partially matching texts."""
    # Setup
    evaluator = RougeScore()
    data = {
        "response": "The quick brown fox jumps over the lazy dog.",
        "reference": "The fast brown fox jumps over the sleeping dog."
    }
    
    # Execute
    score = evaluator.evaluate(data)
    
    # Assert
    assert 0 < score < 1, "Partial match should give score between 0 and 1"


def test_rouge_score_no_match():
    """Test RougeScore with completely different texts."""
    # Setup
    evaluator = RougeScore()
    data = {
        "response": "The quick brown fox jumps over the lazy dog.",
        "reference": "Completely different text with no matching words."
    }
    
    # Execute
    score = evaluator.evaluate(data)
    
    # Assert
    assert score < 0.2, "No significant match should give low score"


def test_rouge_score_different_types():
    """Test RougeScore with different ROUGE types."""
    # Setup
    reference = "The quick brown fox jumps over the lazy dog."
    response = "The quick brown fox jumps over the lazy dog."
    
    # Test rouge1
    evaluator1 = RougeScore(rouge_type="rouge1")
    score1 = evaluator1.evaluate({"response": response, "reference": reference})
    
    # Test rouge2
    evaluator2 = RougeScore(rouge_type="rouge2")
    score2 = evaluator2.evaluate({"response": response, "reference": reference})
    
    # Test rougeL
    evaluatorL = RougeScore(rouge_type="rougeL")
    scoreL = evaluatorL.evaluate({"response": response, "reference": reference})
    
    # Assert all are perfect matches
    assert score1 == 1.0, "Perfect match for rouge1 should be 1.0"
    assert score2 == 1.0, "Perfect match for rouge2 should be 1.0"
    assert scoreL == 1.0, "Perfect match for rougeL should be 1.0"


def test_rouge_score_custom_thresholds():
    """Test RougeScore with custom threshold parameters."""
    # Setup
    evaluator = RougeScore(
        precision_threshold=0.7,
        recall_threshold=0.8,
        f1_score_threshold=0.75
    )
    
    # Assert custom thresholds were set
    assert evaluator.precision_threshold == 0.7
    assert evaluator.recall_threshold == 0.8
    assert evaluator.f1_score_threshold == 0.75