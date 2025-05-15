from promptlab.asset import Asset
from promptlab._experiment import Experiment
from promptlab.studio.studio import Studio
from promptlab.tracer.tracer_factory import TracerFactory
from promptlab._config import ConfigValidator, TracerConfig


class PromptLab:
    def __init__(self, tracer_config: dict):
        tracer_config = TracerConfig(**tracer_config)
        ConfigValidator.validate_tracer_config(tracer_config)

        self.tracer = TracerFactory.get_tracer(tracer_config)
        self.tracer.init_db()

        self.asset = Asset(self.tracer)
        self.experiment = Experiment(self.tracer)
        self.studio = Studio(self.tracer)
