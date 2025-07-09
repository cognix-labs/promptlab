from promptlab.evaluator.evaluator import Evaluator
import numpy as np


class SemanticSimilarity(Evaluator):
    def evaluate(self, data: dict):
        completion = data["response"]
        reference = data["reference"]

        embedding_1 = np.array(self.embedding(completion))
        embedding_2 = np.array(self.embedding(reference))

        # Normalization factors of the above embeddings
        norms_1 = np.linalg.norm(embedding_1, keepdims=True)
        norms_2 = np.linalg.norm(embedding_2, keepdims=True)
        embedding_1_normalized = embedding_1 / norms_1
        embedding_2_normalized = embedding_2 / norms_2
        similarity = embedding_1_normalized @ embedding_2_normalized.T
        score = similarity.flatten()

        return score.tolist()[0]


semantic_similarity = SemanticSimilarity
