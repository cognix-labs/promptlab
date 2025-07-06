from promptlab._utils import Utils
from promptlab.evaluator.evaluator import Evaluator
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.tokenize import word_tokenize


class BleuScore(Evaluator):
    def __init__(self):
        Utils.download_required_nltk_resources()

    def evaluate(self, data: dict):
        completion = data["response"]
        reference = data["reference"]

        reference_tokens = word_tokenize(reference)
        hypothesis_tokens = word_tokenize(completion)

        # NIST Smoothing
        smoothing_function = SmoothingFunction().method4
        score = sentence_bleu(
            [reference_tokens], hypothesis_tokens, smoothing_function=smoothing_function
        )

        return score


bleu_score = BleuScore
