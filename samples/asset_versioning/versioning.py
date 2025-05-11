from promptlab import PromptLab
from promptlab.types import PromptTemplate

# Initialize PromptLab with SQLite storage
tracer_config = {"type": "sqlite", "db_file": "./promptlab.db"}
pl = PromptLab(tracer_config)

# Create a prompt template
prompt_name = "essay_feedback"
prompt_description = "A prompt for generating feedback on essays"
system_prompt = "You are a helpful assistant who can provide feedback on essays."
user_prompt = """The essay topic is - <essay_topic>.
               The submitted essay is - <essay>
               Now write feedback on this essay."""
prompt_template = PromptTemplate(name=prompt_name, description=prompt_description, system_prompt=system_prompt, user_prompt=user_prompt)
pt = pl.asset.create(prompt_template)

# Create a new version of the prompt template
system_prompt="""You are a helpful assistant who can provide feedback on essays. You follow the criteria below while writing feedback.                    
    Grammar & Spelling - The essay should have correct grammar, punctuation, and spelling.
    Clarity & Fluency - Ideas should be expressed clearly, with smooth transitions between sentences and paragraphs.
    Content & Relevance - The essay should stay on topic, answer the prompt effectively, and include well-developed ideas with supporting details or examples.
    Structure & Organization - The essay should have a clear introduction, body paragraphs, and conclusion. Ideas should be logically arranged, with a strong thesis statement and supporting arguments.
    """
user_prompt="""The essay topic is - <essay_topic>.
    The submitted essay is - <essay>
    Now write feedback on this essay.
    """
prompt_template = PromptTemplate(name=prompt_name, description=prompt_description, system_prompt=system_prompt, user_prompt=user_prompt)
pt = pl.asset.update(prompt_template)

# Start the PromptLab Studio to view results
pl.studio.start(8000)
