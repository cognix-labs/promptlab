from promptlab._utils import Utils
from promptlab.evaluator.evaluator import Evaluator
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.tokenize import word_tokenize


class BleuScore(Evaluator):
    def __init__(self):    
        Utils.ensure_nltk_data_downloaded()
    
    def evaluate(self, data: dict):
        inference = data["response"]
        reference = data["reference"]

        # ground_truth = eval_input["ground_truth"]
        # response = eval_input["response"]

        reference_tokens = word_tokenize(reference)
        hypothesis_tokens = word_tokenize(inference)

        # NIST Smoothing
        smoothing_function = SmoothingFunction().method4
        score = sentence_bleu([reference_tokens], hypothesis_tokens, smoothing_function=smoothing_function)

        return score

bleu_score = BleuScore
