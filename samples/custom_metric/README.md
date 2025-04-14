# Custom Metric

This sample ([custom_metric.py](custom_metric.py)) demonstrates how to use PromptLab to use a custom evaluation metric. This also open ups the opprtunity to use external evaluation libraries like Ragas or Azure Evaluation SDK to use with PromptLab.

## Creating custom metric 

The following code snippet implements a metric using the evaluation library Ragas

    class RagasFactualCorrectness(Evaluator):
        
        def evaluate(self, data: dict):

            inference = data["response"]
            reference = data["reference"]
            
            sample = SingleTurnSample(
                response=inference,
                reference=reference
            )
            
            evaluator_llm = LangchainLLMWrapper(ChatOllama(model=self.inference.model_config.inference_model_deployment))

            scorer = FactualCorrectness(llm = evaluator_llm)
            return scorer.single_turn_score(sample)

## Using custom metric

The following code snippet demonstrate how to use the custom metric in the experiment.

    length = LengthEvaluator()
    factual_correctness = RagasFactualCorrectness()

    experiment_config = {
        "inference_model" : {
                "type": "ollama",
                "inference_model_deployment": "llama3.2",
        },
        "embedding_model" : {
                "type": "ollama",
                "embedding_model_deployment": "nomic-embed-text:latest",
        },
        "prompt_template": {
            "name": pt.name,
            "version": pt.version
        },
        "dataset": {
            "name": ds.name,
            "version": ds.version
        },
        "evaluation": [
                {
                    "metric": "LengthEvaluator",
                    "column_mapping": {
                        "response":"$inference",
                    },
                    "evaluator": length,
                },   
                {
                    "metric": "RagasFactualCorrectness",
                    "column_mapping": {
                        "response":"$inference",
                        "reference":"feedback"
                    },
                    "evaluator": factual_correctness,
                },                    
            ],    
    }
    pl.experiment.run(experiment_config)