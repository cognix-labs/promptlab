from promptlab import PromptLab
from promptlab.types import Dataset, PromptTemplate

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

def update_prompt_template(prompt_lab: PromptLab, name, version, system_prompt, user_prompt) -> str:

    name = 'essay_feedback_prompt'
    description = 'A prompt designed to generate feedback for essays.'
    
    prompt_template = PromptTemplate (
        name = name,
        version = version,
        description = description,
        system_prompt = system_prompt,
        user_prompt = user_prompt,
    )

    prompt_template = prompt_lab.asset.update(prompt_template) 

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

    experiment = {
            "model" : {
                    "type": "ollama",
                    "inference_model_deployment": "llama3.2",
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
                        "type": "ragas",
                        "metric": "SemanticSimilarity",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"feedback"
                        },
                    },
                    {
                        "type": "ragas",
                        "metric": "NonLLMStringSimilarity",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"feedback",
                        },
                    },
                    {
                        "type": "ragas",
                        "metric": "RougeScore",
                        "column_mapping": {
                            "response":"$inference",
                            "reference":"feedback",
                        },
                    },
                ],    
    }

    prompt_lab.experiment.run(experiment)

def deploy_prompt_template(prompt_lab: PromptLab, deployment_dir: str, prompt_template_name: str, prompt_template_version: int):
    
    prompt = PromptTemplate (
        name = prompt_template_name,
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
    dataset_name = "essay_feedback_dataset"
    eval_dataset_file_path = 'C:\work\promptlab\test\dataset\essay_feedback.jsonl'
    dataset = create_dataset(prompt_lab, dataset_name, eval_dataset_file_path)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Create a prompt template.
    prompt_template_name = 'essay_feedback_prompt'

    system_prompt_v1 = 'You are a helpful assistant who can provide feedback on essays.'
    user_prompt_v1 = '''The essay topic is - <essay_topic>.

    The submitted essay is - <essay>
    Now write feedback on this essay.
    '''

    prompt_template_v1 = create_prompt_template(prompt_lab, prompt_template_name, system_prompt_v1, user_prompt_v1)

    # Create the second version of the prompt template.
    system_prompt_v2 = '''You are a helpful assistant who can provide feedback on essays. You follow the criteria below while writing feedback.                    
    Grammar & Spelling - The essay should have correct grammar, punctuation, and spelling.
    Clarity & Fluency - Ideas should be expressed clearly, with smooth transitions between sentences and paragraphs.
    Content & Relevance - The essay should stay on topic, answer the prompt effectively, and include well-developed ideas with supporting details or examples.
    Structure & Organization - The essay should have a clear introduction, body paragraphs, and conclusion. Ideas should be logically arranged, with a strong thesis statement and supporting arguments.
    '''
    user_prompt_v2 = '''The essay topic is - <essay_topic>.

    The submitted essay is - <essay>
    Now write feedback on this essay.
    '''
    prompt_template_v2 = update_prompt_template(prompt_lab, prompt_template_v1.name, prompt_template_v1.version, system_prompt_v2, user_prompt_v2)
    
    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Create an experiment and run it with the first version of the prompt template.
    create_experiment(prompt_lab, prompt_template_v1.name, prompt_template_v1.version, dataset.name, dataset.version)

    # Create an experiment and run it with the second version of the prompt template.
    create_experiment(prompt_lab, prompt_template_v2.name, prompt_template_v2.version, dataset.name, dataset.version)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Let's launch the studio again and check the experiment and its result.
    prompt_lab.studio.start(8000)

    #-------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------#

    # Let's deploy the second version of the prompt template to a directory in production.
    deployment_dir = 'C:\work\prompt_templates'
    deploy_prompt_template(prompt_lab, deployment_dir, prompt_template_name, 1)



