from promptlab.asset_service import AssetService
from promptlab._experiment import Experiment
from promptlab.studio.studio import Studio
from promptlab.tracer.tracer_factory import TracerFactory
from promptlab._config import ConfigValidator, TracerConfig
from promptlab._logging import logger


class PromptLab:
    def __init__(self, tracer_config: dict):
        self.tracer = TracerFactory.get_tracer(tracer_config)
        logger.info("Tracer initialized successfully.")

        self.asset = AssetService(self.tracer)
        self.experiment = Experiment(self.tracer)
        self.studio = Studio(self.tracer)
