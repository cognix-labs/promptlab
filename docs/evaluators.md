# PromptLab Evaluators

Evaluators are a crucial component of PromptLab that help measure the quality of model responses. They allow you to quantitatively compare different prompt templates, models, or parameters based on objective metrics. PromptLab offers several built-in evaluators, and you can also create custom evaluators to fit your specific needs.

- General Purpose
    - [BLEU Score](#bleu-score-bleuscore)
    - [Exact Match](#exact-match-exactmatch)
    - [Fluency](#fluency-fluency)
    - [Coherence](#coherence-coherence)
    - [F1 Score](#f1-score-f1score)
    - [ROUGE](#rouge-score-rougescore)
- RAG (Retrieval Augmented Generation)
    - [Semantic Similarity](#semantic-similarity-semanticsimilarity)
    - [Groundedness](#groundedness-groundedness)
    - [Relevance](#relevance-relevance)
    - Context Precision
    - Context Recall
- Agents
    - Intent Resolution
    - Task Adherence
    - Tool Call Accuracy

## Built-in Evaluators

PromptLab comes with the following built-in evaluators, grouped according tor their primary use case:

### General Purpose
#### BLEU Score (`BleuScore`)

[BLEU (Bilingual Evaluation Understudy)](../src/promptlab/evaluator/bleu.py) is a metric for evaluating machine-translated text. In PromptLab, it's used to compare the similarity between model responses and reference answers.

- **Input**: 
  - `response`: The model's generated text
  - `reference`: The reference text to compare against
- **Output**: A score between 0 and 1, where higher values indicate better matches
- **Usage**: Particularly useful for tasks where the exact wording matters (e.g., translation, summarization)

The implementation uses NLTK's sentence_bleu function with NIST smoothing (method4).

#### Exact Match (`ExactMatch`)

The [Exact Match](../src/promptlab/evaluator/exact_match.py) evaluator compares whether the model's response perfectly matches the reference text.

- **Input**: 
  - `response`: The model's generated text
  - `reference`: The reference text to compare against
- **Output**: `True` if both texts match exactly, otherwise `False`
- **Usage**: Useful for tasks requiring precise answers (e.g., factual questions, math problems)

#### Fluency (`Fluency`)

The [Fluency](../src/promptlab/evaluator/fluency.py) is a LLM-as-a-Judge evaluator which measures how well-written and linguistically articulate a generated response is, regardless of its content.

- **Input**: 
  - `response`: The model's generated text to evaluate
- **Output**: An integer score from 1 to 5, where:
  - 1: Rudimentary Expression
  - 2: Developing Expression
  - 3: Functional Expression
  - 4: Refined Expression
  - 5: Masterful Expression
- **Usage**: Useful for evaluating the linguistic quality and readability of generated content

This evaluator uses another inference model to rate the text's fluency based on a detailed linguistic assessment rubric.

#### Coherence (`Coherence`)

The [Coherence](../src/promptlab/evaluator/coherence.py) is a LLM-as-a-Judge evaluator which assesses how logically organized and connected the ideas in a response are, evaluating the flow and structure of the text.

- **Input**: 
  - `query`: The original query that prompted the response
  - `response`: The model's generated text to evaluate
- **Output**: An integer score from 1 to 5, where:
  - 1: Incoherent Response
  - 2: Poorly Coherent Response
  - 3: Partially Coherent Response
  - 4: Coherent Response
  - 5: Highly Coherent Response
- **Usage**: Useful for evaluating how well a response presents information in a logical, connected manner that directly addresses the query

This evaluator uses another inference model to rate the text's coherence based on a detailed assessment framework that examines logical flow, transitions between ideas, and overall organization.

#### F1 Score (`F1Score`)

The [F1 Score](../src/promptlab/evaluator/f1_score.py) evaluator calculates the F1 score for a given response and ground truth, which measures the overlap between the generated response and the ground truth by combining precision and recall into a single metric.

- **Input**: 
  - `response`: The model's generated text
  - `reference`: The reference text to compare against
- **Output**: A float between 0 and 1, where 0 indicates no overlap and 1 indicates a perfect match
- **Usage**: Useful for evaluating how well a response captures the correct information, balancing both completeness (recall) and accuracy (precision)

This evaluator calculates precision (proportion of shared words relative to the total words in the response) and recall (proportion of shared words relative to the total words in the ground truth), then computes the F1 score as the harmonic mean of these two values.

#### F1 Score (`F1Score`)

The [F1 Score](../src/promptlab/evaluator/f1_score.py) evaluator calculates the F1 score for a given response and ground truth, which measures the overlap between the generated response and the ground truth by combining precision and recall into a single metric.

- **Input**: 
  - `response`: The model's generated text
  - `reference`: The reference text to compare against
- **Output**: A float between 0 and 1, where 0 indicates no overlap and 1 indicates a perfect match
- **Usage**: Useful for evaluating how well a response captures the correct information, balancing both completeness (recall) and accuracy (precision)

This evaluator calculates precision (proportion of shared words relative to the total words in the response) and recall (proportion of shared words relative to the total words in the ground truth), then computes the F1 score as the harmonic mean of these two values.

#### ROUGE Score (`RougeScore`)

[ROUGE (Recall-Oriented Understudy for Gisting Evaluation)](../src/promptlab/evaluator/rouge.py) measures the similarity between generated text and reference text based on n-gram overlaps and sequence matching.

- **Input**: 
  - `response`: The model's generated text
  - `reference`: The reference text to compare against
- **Output**: A float value between 0 and 1, where higher scores indicate better matches
- **Parameters**:
  - `rouge_type`: Type of ROUGE score to calculate (default: "rouge1")
  - `precision_threshold`: Minimum acceptable precision (default: 0.5)
  - `recall_threshold`: Minimum acceptable recall (default: 0.5)
  - `f1_score_threshold`: Minimum acceptable F1 score (default: 0.5)
- **Usage**: Useful for evaluating text summarization, machine translation, or any scenario where capturing relevant content from a reference is critical—especially with a focus on recall

The implementation supports several ROUGE variants:
  - rouge1: Unigram overlap
  - rouge2: Bigram overlap
  - rougeL: Longest common subsequence matching

### RAG (Retrieval Augmented Generation)

#### Semantic Similarity (`SemanticSimilarity`)

This evaluator computes the semantic similarity between the model response and a reference text using vector embeddings.

- **Input**: 
  - `response`: The model's generated text
  - `reference`: The reference text to compare against
- **Output**: A float value indicating the cosine similarity (typically between -1 and 1)
- **Usage**: Useful when the meaning matters more than the exact wording

The evaluator uses embeddings to represent both texts and calculates their cosine similarity.

#### Groundedness (`Groundedness`)

The [Groundedness](../src/promptlab/evaluator/groundedness.py) is a LLM-as-a-Judge evaluator which assesses how well the claims in an AI-generated response are supported by the provided context.

- **Input**: 
  - `query`: (Optional) The original query that prompted the response
  - `response`: The model's generated text to evaluate
  - `context`: The reference context that should support the response
- **Output**: A JSON object containing:
  - A score from 1 to 5, where:
    - 1: Ungrounded Response
    - 2: Minimally Grounded Response
    - 3: Partially Grounded Response
    - 4: Mostly Grounded Response
    - 5: Fully Grounded Response
  - Reasoning that explains the score
- **Usage**: Useful for evaluating how well RAG systems ensure that responses are factually supported by the provided context

This evaluator uses another inference model to assess groundedness based on how well each claim in the response can be verified from the given context.

#### Relevance (`Relevance`)

The [Relevance](../src/promptlab/evaluator/relevance.py) evaluator assesses how well a response addresses the key points of the input query, along with reasoning.

- **Input**: 
  - `query`: The original query that prompted the response
  - `response`: The model's generated text to evaluate
- **Output**: An integer score from 1 to 5, where:
  - 1: Completely Irrelevant Response
  - 2: Mostly Irrelevant Response
  - 3: Partially Relevant Response
  - 4: Mostly Relevant Response
  - 5: Highly Relevant Response
- **Usage**: Useful for evaluating how effectively an AI system interprets inputs and generates meaningful, context-aware responses that meet the user's intent

This evaluator uses an inference model to rate the relevance of the response based on how well it addresses the query content and intent.

## Evaluator Architecture

All evaluators in PromptLab:

1. Inherit from the `Evaluator` base class defined in `src/promptlab/evaluator/evaluator.py`
2. Implement the required `evaluate(data: dict)` method
3. Can be dynamically loaded through the `EvaluatorFactory` mechanism

The `EvaluatorFactory` class automatically discovers and imports all evaluator modules, making them available for use in experiments.

## Creating Custom Evaluators

You can create your own evaluators by following these steps:

1. Create a new Python file in your project
2. Define a class that inherits from `promptlab.evaluator.evaluator.Evaluator`
3. Implement the required `evaluate(data: dict)` method
4. Return a meaningful score or result from your evaluation

Here's a simple example:

```python
from promptlab.evaluator.evaluator import Evaluator

class MyCustomEvaluator(Evaluator):
    def evaluate(self, data: dict):
        response = data["response"]
        reference = data["reference"]
        
        # Your custom evaluation logic here
        score = your_evaluation_function(response, reference)
        
        return score

# Export the evaluator class
my_custom_evaluator = MyCustomEvaluator
```

For more examples, see the [Custom Metric Examples](../samples/custom_metric/) in the samples directory.

## Using Evaluators in Experiments

Evaluators can be specified when creating an experiment:

```python
import promptlab as pl

# Create an experiment with multiple evaluators
experiment = pl.Experiment(
    name="My Experiment",
    evaluators=["BleuScore", "SemanticSimilarity", "my_custom_evaluator"]
)
```

## Accessing Evaluation Results

After running an experiment, you can access the evaluation results:

```python
# Run the experiment
results = experiment.run()

# Get evaluation metrics
for result in results:
    print(f"Prompt: {result.prompt_name}")
    for metric_name, metric_value in result.metrics.items():
        print(f"  {metric_name}: {metric_value}")
```

You can also compare evaluation results across different experiments using PromptLab Studio.
