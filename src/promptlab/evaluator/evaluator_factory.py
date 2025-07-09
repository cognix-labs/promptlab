import os
import importlib
import pkgutil

from promptlab.evaluator.evaluator import Evaluator
from promptlab.model.model import Model


def import_evaluators():
    """Dynamically import all evaluator modules"""
    evaluator_classes = {}
    package = "promptlab.evaluator"

    for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if module_name != "evaluator_factory" and module_name != "evaluator":
            module = importlib.import_module(f"{package}.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Evaluator)
                    and attr != Evaluator
                ):
                    evaluator_classes[attr_name] = attr

    return evaluator_classes


class EvaluatorFactory:
    _evaluator_classes = import_evaluators()

    @staticmethod
    def get_evaluator(
        metric: str,
        completion_model: Model,
        embedding_model: Model,
        evaluator: Evaluator = None,
    ) -> Evaluator:
        if evaluator is None:
            evaluator_class = EvaluatorFactory._evaluator_classes.get(metric)
            if evaluator_class is None:
                raise ValueError(f"Unknown evaluator: {metric}")
            evaluator = evaluator_class()

        evaluator.completion = completion_model
        evaluator.embedding = embedding_model

        return evaluator
