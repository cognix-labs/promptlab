# Self-hosting

This sample ([hosted.py](hosted.py)) demonstrates how to use self-hosted PromptLab. 

## Installation and Setup

To host PromptLab in your environment, please follow this guide - [Self Hosting PromptLab](../../docs/self_hosting.md).

To interact with the hosted PromptLab service, locally install the PromptLab package in a virtual environment (try venv or conda or uv).

```bash
pip install promptlab
```

## Initialize PromptLab 

The first step to use PromptLab is to initialize the PromptLab object. Please check [Tracer](../../docs/README.md#tracer) to learn more about the tracer configuration.

```python
tracer_config = {
    "type": "api",
    "endpoint": "http://HOST-URL:8001",
    "jwt_token": "JWT_TOKEN",
}
pl = PromptLab(tracer_config)
```

- HOST-URL is the URL of the hosted service.
- JWT_TOKEN can be found in the PromptLab page. Copy it from the top right corner profile link.

Everything else for creating assets and running experiments are same as other examples.