# Quickstart

This sample ([custom_metric.py](custom_metric.py)) demonstrates how to use PromptLab to use a custom evaluation metric. 

## Install python package

Install the python package using pip. It's highly recommended to use a virtual environment. 

    pip install promptlab

## Initialize PromptLab 

The frist step to use PromptLab, is to initialize the PromptLab object. PromptLab uses `sqlite` for database. Please check [Tracer](../../docs/README.md#tracer) to learn more about it.

In the [custom_metric.py](custom_metric.py), the `def create_prompt_lab(tracer_type: str, tracer_db_file_path: str) -> PromptLab:` function creates the PromptLab object.

Once the PromptLab object is ready, you can start the PromptLab Studio to check the assets and experiments.

    prompt_lab.studio.start(8000)

## Create a prompt template

A prompt template is a prompt with or without placeholders. Please check [Prompt Template](../../docs/README.md#prompt-template) to learn more about it.

In the [quickstart.py](quickstart.py), the `def create_prompt_template(prompt_lab: PromptLab) -> str:` method demonstrates how to create a prompt template.

A  prompt template has two main attributes - `system_prompt` and `user_prompt`. The sample prompt used in this example is -

    system_prompt = 'You are a helpful assistant who can provide feedback on essays.'
    user_prompt = '''The essay topic is - <essay_topic>.

    The submitted essay is - <essay>
    Now write feedback on this essay.
    '''

Here, `<context>` and `<question>` are placeholders that will be replaced with real data before sending to the LLM. PromptLab will search the dataset for columns with these exact names and use their values to replace the corresponding placeholders. Ensure that the dataset contains columns named `context` and `question` to avoid errors.

![PromptLab Studio](../../img/studio-pt.png)

## Create dataset

A dataset is a jsonl file to design the experiment. Please check [Dataset](../../docs/README.md#dataset) to learn more about it.

In the [custom_metric.py](custom_metric.py), the `def create_dataset(prompt_lab: PromptLab, file_path: str) -> str:` method demonstrates how to create a dataset.

![PromptLab Studio](../../img/studio-ds.png)

## Create custom evaluator

In this example, we are going to build a custom evaluator to calculate the length of the response. The code is in the [length.py](length.py) file. The class needs to implement the Evaluator interface. This is a very basic custom evaluator that calculates the length of the output from LLM.

    from promptlab.evaluator.evaluator import Evaluator

    class LengthEvaluator(Evaluator):
        
        def evaluate(self, inference: str):
        
            return len(str(inference))

We can also use LLM as a judge to evaluate our prompt. The [fluency.py](fluency.py) implements an evaluator to calculate the fluency of the Feedback.

from promptlab.evaluator.evaluator import Evaluator

class FluencyEvaluator(Evaluator):
    
    def evaluate(self, data: dict):

        system_prompt = """
                        # Instruction
                        ## Goal
                        ### You are an expert in evaluating the quality of a FEEDBACK from an intelligent system based on provided definition and data. Your goal will involve answering the questions below using the information provided.
                        - **Definition**: You are given a definition of the communication trait that is being evaluated to help guide your Score.
                        - **Data**: Your input data include a FEEDBACK.
                        - **Tasks**: To complete your evaluation you will be asked to evaluate the Data in different ways.
                    """

        user_prompt = """
                    # Definition
                    **Fluency** refers to the effectiveness and clarity of written communication, focusing on grammatical accuracy, vocabulary range, sentence complexity, coherence, and overall readability. It assesses how smoothly ideas are conveyed and how easily the text can be understood by the reader.
                    .................................
                    .................................
                    .................................

                    # Data
                    FEEDBACK: {{feedback}}


                    # Tasks
                    ## Please provide your assessment Score for the previous FEEDBACK based on the Definitions above. The Score you give MUST be a integer score (i.e., "1", "2"...) based on the levels of the definitions. Only reply with the numeric score. Do not add any other text or explanation score.
                        """
        
        inference = data["response"]

        user_prompt = user_prompt.replace("{{feedback}}", inference)

        inference_result = self.inference_model.invoke(system_prompt, user_prompt)

        return inference_result.inference    

## Create experiment

An experiment evaluates the outcome of a prompt against a set of metrics for a given dataset. Developers can modify hyperparameters (such as prompt template and models) and compare experiment results to determine the best prompt for deployment in production. Please check [Experiment](../../docs/README.md#experiment) to learn more about it.

In the [custom_metric.py](custom_metric.py), we are using the prompt template and dataset created in the previous steps to design an experiment. The `def create_experiment(prompt_lab: PromptLab, endpoint:str, prompt_template_id: str, prompt_template_version: int, dataset_id: str, dataset_version: int):
` method demonstrates how to create and run an expriment.

![PromptLab Studio](../../img/studio-home.png)

You can compare multiple experiments.

![PromptLab Studio](../../img/studio-exp-compare.png)