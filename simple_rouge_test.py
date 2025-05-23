from rouge_score import rouge_scorer


def test_rouge_library():
    # Test the rouge library directly
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(
        "The quick brown fox jumps over the lazy dog.",
        "The quick brown fox jumps over the lazy dog.",
    )

    # Print scores for debugging
    print(f"ROUGE Scores: {scores}")

    # Check scores
    assert scores["rouge1"].fmeasure == 1.0
    assert scores["rouge2"].fmeasure == 1.0
    assert scores["rougeL"].fmeasure == 1.0


if __name__ == "__main__":
    test_rouge_library()
    print("All tests passed!")
