from promptlab._config import TracerConfig
from promptlab.enums import TracerType
from promptlab.tracer.sqlite_tracer import SQLiteTracer
from promptlab.tracer.tracer import Tracer


class TracerFactory:
    @staticmethod
    def get_tracer(tracer_config: TracerConfig) -> Tracer:
        if tracer_config.type == TracerType.SQLITE.value:
            return SQLiteTracer(tracer_config)
        else:
            raise ValueError(f"Unknown tracer: {tracer_config.type}")
