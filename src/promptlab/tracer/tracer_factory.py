from promptlab.types import TracerConfig
from promptlab.enums import TracerType
from promptlab.tracer.local_tracer import LocalTracer
from promptlab.tracer.api_tracer import ApiTracer
from promptlab.tracer.tracer import Tracer


class TracerFactory:
    @staticmethod
    def get_tracer(_tracer_config: dict) -> Tracer:
        tracer_config = TracerConfig(**_tracer_config)

        if tracer_config.type == TracerType.API.value:
            return ApiTracer(tracer_config)
        if tracer_config.type == TracerType.LOCAL.value:
            return LocalTracer(tracer_config)
        else:
            raise ValueError(f"Unknown tracer: {tracer_config.type}")
