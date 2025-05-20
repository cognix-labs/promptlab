<div align="center">
    <img alt="logo" src="https://github.com/imum-ai/promptlab/blob/main/img/logo.png" style="height:300px">
    <h1>PromptLab</h1>
    <p>A free, lightweight, open-source experimentation tool for Gen AI applications</p>
    <a href="https://pypi.org/project/promptlab/"><img src="https://img.shields.io/pypi/v/promptlab.svg" alt="PyPI Version"></a>
    <a href="https://github.com/imum-ai/promptlab/blob/main/LICENSE"><img src="https://img.shields.io/github/license/imum-ai/promptlab.svg" alt="License"></a>
    <a href="https://github.com/imum-ai/promptlab/stargazers"><img src="https://img.shields.io/github/stars/imum-ai/promptlab.svg" alt="GitHub Stars"></a>
</div>

## 📋 Table of Contents

- [Overview](#overview-)
- [Features](#features-)
- [Installation](#installation-)
- [Quick Start](#quick-start-)
- [Core Concepts](#core-concepts-)
- [Documentation](#documentation-)
- [Supported Models](#supported-models-)
- [Examples](#examples-)
- [Articles & Tutorials](#articles--tutorials-)
- [Contributing](#contributing-)
- [License](#license-)

## Overview 🔍

PromptLab is a free, lightweight, open-source experimentation tool for Gen AI applications. It streamlines prompt engineering, making it easy to set up experiments, evaluate prompts, and track them in production - all without requiring any cloud services or complex infrastructure.

With PromptLab, you can:

- Create and manage prompt templates with versioning
- Build and maintain evaluation datasets
- Run experiments with different models and prompts
- Evaluate model and prompt performance using built-in and custom metrics
- Compare experiment results side-by-side
- Deploy optimized prompts to production

<div align="center">
    <img alt="PromptLab Studio" src="img/studio-exp.png" style="max-width:800px">
</div>

## Features ✨

- **Truly Lightweight**: No cloud subscription, no additional servers, not even Docker - just a simple Python package
- **Easy to Adopt**: No ML or Data Science expertise required
- **Self-contained**: No need for additional cloud services for tracking or collaboration
- **Seamless Integration**: Works within your existing web, mobile, or backend project
- **Flexible Evaluation**: Use built-in metrics or bring your own custom evaluators
- **Web Interface**: Compare experiments and track assets through a web interface
- **Multiple Model Support**: Works with Azure OpenAI, Ollama, DeepSeek and more. You can also bring your ownd model.
- **Version Control**: Automatic versioning of all assets for reproducibility
- **Async Support**: Run experiments and invoke models asynchronously for improved performance

## Installation 📦

```bash
pip install promptlab
```

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install promptlab
```

## Quick Start 🚀

Check the quick start example here - [samples/quickstart](https://github.com/imum-ai/promptlab/blob/main/samples/quickstart/README.md)

## Core Concepts 🧩

### Tracer

Tracer is responsible for persisting and updating assets and experiments in the storage layer. At present, only SQLite is supported.

### Assets

Immutable artifacts used in experiments, with automatic versioning:

- **Prompt Templates**: Prompts with optional placeholders for dynamic content
- **Datasets**: JSONL files containing evaluation data

### Experiments

Evaluate prompts against datasets using specified models and metrics.

### PromptLab Studio

A web interface for visualizing experiments and comparing results.

## Documentation 📖

For comprehensive documentation, visit our [Documentation Page](https://github.com/imum-ai/promptlab/blob/main/docs/README.md).

Key documentation:
- [Core Concepts](docs/README.md#core-concepts)
- [Evaluators](docs/evaluators.md) - Detailed information about built-in and custom evaluators

## Supported Models 🤖

- **Azure OpenAI**: Connect to Azure-hosted OpenAI models
- **Ollama**: Run experiments with locally-hosted models
- **OpenRouter**: Access a wide range of AI models (OpenAI, Anthropic, DeepSeek, Mistral, etc.) via OpenRouter API
- **Custom Models**: Integrate your own model implementations

## Examples 📚

- [Quickstart](https://github.com/imum-ai/promptlab/tree/main/samples/quickstart): Getting started with PromptLab
- [Asset versioning](https://github.com/imum-ai/promptlab/tree/main/samples/asset_versioning): Versioning Prompts and Datasets
- [Custom Metric](https://github.com/imum-ai/promptlab/tree/main/samples/custom_metric): Creating custom evaluation metrics
- [Async Example](https://github.com/imum-ai/promptlab/tree/main/samples/async_example): Using async functionality with Ollama and OpenRouter models for improved performance
- [Custom Model](https://github.com/imum-ai/promptlab/tree/main/samples/custom_model): Bring your own model for evaluation

## Articles & Tutorials 📝

- [Evaluating prompts locally with Ollama and PromptLab](https://www.linkedin.com/pulse/evaluating-prompts-locally-ollama-promptlab-raihan-alam-i2iic)
- [Creating custom prompt evaluation metrics with PromptLab](https://www.linkedin.com/pulse/promptlab-creating-custom-metric-prompt-evaluation-raihan-alam-o0slc)

## CI/CD 🔄

PromptLab uses GitHub Actions for continuous integration and testing:

- **Unit Tests**: Run unit tests for all components of PromptLab
- **Integration Tests**: Run integration tests that test the interaction between components
- **Performance Tests**: Run performance tests to ensure performance requirements are met

The tests are organized into the following directories:

- `tests/unit/`: Unit tests for individual components
- `tests/integration/`: Tests that involve multiple components working together
- `tests/performance/`: Tests that measure performance
- `tests/fixtures/`: Common test fixtures and utilities

You can find more information about the CI/CD workflows in the [.github/workflows](https://github.com/imum-ai/promptlab/tree/main/.github/workflows) directory.

## Contributing 👥

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
