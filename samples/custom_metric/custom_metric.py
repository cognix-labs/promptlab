from promptlab import PromptLab
from promptlab.types import Dataset, PromptTemplate
from length import LengthEvaluator

def create_prompt_lab(tracer_type: str, tracer_db_file_path: str) -> PromptLab:

    tracer_config = {
        "type": tracer_type,
        "db_file": tracer_db_file_path
    }
  
    prompt_lab = PromptLab(tracer_config)

    return prompt_lab

def create_prompt_template(prompt_lab: PromptLab, prompt_template_id, system_prompt, user_prompt) -> str:

    name = 'essay_feedback_prompt'
    description = 'A prompt designed to generate feedback for essays.'
    
    prompt_template = PromptTemplate (
        id = prompt_template_id,
        name = name,
        description = description,
        system_prompt = system_prompt,
        user_prompt = user_prompt,
    )

    prompt_template = prompt_lab.asset.create_or_update(prompt_template)

    return (prompt_template.id, prompt_template.version)

def create_dataset(prompt_lab: PromptLab, file_path: str) -> str:

    name = "essay_feedback_dataset"
    description = "dataset for evaluating the essay_feedback_prompt."

    dataset = Dataset (
        name = name,
        description = description,
        file_path = file_path,
    )

    dataset = prompt_lab.asset.create_or_update(dataset) 

    return (dataset.id, dataset.version)

def create_experiment(prompt_lab: PromptLab, prompt_template_id: str, prompt_template_version: int, dataset_id: str, dataset_version: int):

    length_eval = LengthEvaluator()

    experiment = {
            "model" : {
                    "type": "ollama",
                    "inference_model_deployment": "llama3.2",
                    "embedding_model_deployment": "nomic-embed-text:latest",
            },
            "prompt_template": {
                "id": prompt_template_id,
                "version": prompt_template_version
            },
            "dataset": {
                "id": dataset_id,
                "version": dataset_version
            },
            "evaluation": [
                    {
                        "type": "custom",
                        "metric": "LengthEvaluator",
                        "column_mapping": {
                            "response":"$inference",
                        },
                        "evaluator": length_eval
                    },                    
                    {
                        "type": "ragas",
                        "metric": "SemanticSimilarity",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"feedback"
                        },
                    },
                ],    
    }

    prompt_lab.experiment.run(experiment)

def deploy_prompt_template(prompt_lab: PromptLab, deployment_dir: str, prompt_template_id: str, prompt_template_version: int):
    
    prompt = PromptTemplate (
        id = prompt_template_id,
        version = prompt_template_version,
        )
    
    prompt_lab.asset.deploy(prompt, deployment_dir)

if __name__ == "__main__":

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Create prompt_lab object which will be used to access different functionalities of the library.
    tracer_type = 'sqlite'
    tracer_db_file_path = 'C:\work\promptlab\test\trace_target\promptlab.db'

    prompt_lab = create_prompt_lab(tracer_type, tracer_db_file_path)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Create a dataset.
    eval_dataset_file_path = 'C:\work\promptlab\test\dataset\essay_feedback.jsonl'
    dataset_id, dataset_version = create_dataset(prompt_lab, eval_dataset_file_path)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Create a prompt template.
    system_prompt = 'You are a helpful assistant who can provide feedback on essays.'
    user_prompt = '''The essay topic is - <essay_topic>.

    The submitted essay is - <essay>
    Now write feedback on this essay.
    '''

    prompt_template_id, prompt_template_version = create_prompt_template(prompt_lab, None, system_prompt, user_prompt)
    
    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    prompt_template_id = 'c395330a-78af-4f3a-84c6-a386773b30a8'
    prompt_template_version = 1
    dataset_id = '0a6f739e-090f-47ae-a2b9-ed50e8e96586'
    dataset_version = 0
    # Create an experiment and run it with the first version of the prompt template.
    create_experiment(prompt_lab, prompt_template_id, prompt_template_version, dataset_id, dataset_version)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Let's launch the studio again and check the experiment and its result.
    prompt_lab.studio.start(8000)



