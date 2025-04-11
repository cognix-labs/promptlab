from promptlab import PromptLab
from promptlab.types import Dataset, PromptTemplate
from length import LengthEvaluator
from fluency import FluencyEvaluator

def create_prompt_lab(tracer_type: str, tracer_db_file_path: str) -> PromptLab:

    tracer_config = {
        "type": tracer_type,
        "db_file": tracer_db_file_path
    }
  
    prompt_lab = PromptLab(tracer_config)

    return prompt_lab

def create_prompt_template(prompt_lab: PromptLab, name, system_prompt, user_prompt) -> str:

    description = 'A prompt designed to generate feedback for essays.'
    
    prompt_template = PromptTemplate (
        name = name,
        description = description,
        system_prompt = system_prompt,
        user_prompt = user_prompt,
    )

    prompt_template = prompt_lab.asset.create(prompt_template) 

    return prompt_template

def create_dataset(prompt_lab: PromptLab, name, file_path: str) -> str:

    description = "dataset for evaluating the essay_feedback_prompt."

    dataset = Dataset (
        name = name,
        description = description,
        file_path = file_path,
    )

    dataset = prompt_lab.asset.create(dataset) 

    return dataset

def create_experiment(prompt_lab: PromptLab, prompt_template_name: str, prompt_template_version: int, dataset_name: str, dataset_version: int):

    # length_eval = LengthEvaluator()
    fluency_eval = FluencyEvaluator()

    experiment = {
            "inference_model" : {
                    "type": "ollama",
                    "inference_model_deployment": "llama3.2",
            },
            "embedding_model" : {
                    "type": "ollama",
                    "embedding_model_deployment": "nomic-embed-text:latest",
            },
            "prompt_template": {
                "name": prompt_template_name,
                "version": prompt_template_version
            },
            "dataset": {
                "name": dataset_name,
                "version": dataset_version
            },
            "evaluation": [
                    {
                        "metric": "LengthEvaluator",
                        "column_mapping": {
                            "response":"$inference",
                        },
                    },     
                    {
                        "metric": "FluencyEvaluator",
                        "column_mapping": {
                            "response":"$inference",
                        },
                        # "evaluator": fluency_eval
                    },                    
                    {
                        "metric": "SemanticSimilarityEvaluator",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"feedback"
                        },
                    }
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
    dataset_name = "essay_feedback_dataset9"
    eval_dataset_file_path = 'C:\work\promptlab\test\dataset\essay_feedback.jsonl'
    # dataset = create_dataset(prompt_lab, dataset_name, eval_dataset_file_path)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Create a prompt template.
    prompt_template_name = 'essay_feedback_prompt9'

    system_prompt = 'You are a helpful assistant who can provide feedback on essays.'
    user_prompt = '''The essay topic is - <essay_topic>.

    The submitted essay is - <essay>
    Now write feedback on this essay.
    '''

    # prompt_template = create_prompt_template(prompt_lab, prompt_template_name, system_prompt, user_prompt)
    
    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Create an experiment and run it with the first version of the prompt template.
    # create_experiment(prompt_lab, prompt_template.name, prompt_template.version, dataset.name, dataset.version)
    create_experiment(prompt_lab, prompt_template_name, 0, dataset_name, 0)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Let's launch the studio again and check the experiment and its result.
    prompt_lab.studio.start(8000)