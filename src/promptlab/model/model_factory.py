import os
import importlib
import pkgutil
from typing import Union
from promptlab.types import ModelConfig
from promptlab.model.model import Model, EmbeddingModel


def import_model_classes():
    """Dynamically import all model classes from the model package"""
    model_classes = {}
    embedding_classes = {}
    package = "promptlab.model"

    for _, module_name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if module_name not in ["model_factory", "model", "__init__"]:
            try:
                module = importlib.import_module(f"{package}.{module_name}")
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and hasattr(attr, "__mro__")  # Ensure it's a class
                        and attr != Model
                        and attr != EmbeddingModel
                    ):
                        # Check if it's a Model subclass
                        if Model in attr.__mro__:
                            model_classes[attr_name] = attr
                        # Check if it's an EmbeddingModel subclass
                        elif EmbeddingModel in attr.__mro__:
                            embedding_classes[attr_name] = attr
            except ImportError:
                # Skip modules that can't be imported (e.g., missing dependencies)
                continue

    return model_classes, embedding_classes


class ModelFactory:
    _model_classes, _embedding_classes = import_model_classes()

    @staticmethod
    def get_model(
        model_config: ModelConfig, completion: bool = True, model: Model = None
    ) -> Union[Model, EmbeddingModel]:
        if model:
            return model

        available_model_classes = (
            ModelFactory._model_classes
            if completion
            else ModelFactory._embedding_classes
        )

        class_name = f"{model_config.name.split('/')[0]}_{model_config.type}"

        model_class = available_model_classes[class_name]

        return model_class(model_config)
