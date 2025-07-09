from promptlab.asset import Asset
from promptlab._experiment import Experiment
from promptlab.studio.studio import Studio
from promptlab.tracer.tracer_factory import TracerFactory
from promptlab._logging import logger


class PromptLab:
    def __init__(self, tracer_config: dict):
        self.tracer = TracerFactory.get_tracer(tracer_config)
        logger.info("Tracer initialized successfully.")

        self.asset = Asset(self.tracer)
        self.experiment = Experiment(self.tracer)
        self.studio = Studio(self.tracer)
