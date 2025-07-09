from promptlab.evaluator.evaluator import Evaluator


class Relevance(Evaluator):
    def evaluate(self, data: dict):
        system_prompt = """
        # Role
        You are an expert evaluator assessing the relevance of responses from language models. Your task is to provide objective scoring using a defined 5-point scale.
        
        # Approach
        - Analyze how well the response addresses the key points of the input query
        - Evaluate the response's understanding of the query context and intent
        - Assess whether the response provides information that is appropriate and useful
        - Rate based on defined relevance levels from 1 (least relevant) to 5 (most relevant)
        """

        user_prompt = """
        # Relevance Evaluation Framework
        
        ## Definition
        **Relevance** measures how well a response addresses the key points of the input query. A relevant response demonstrates strong understanding of the query and context, resulting in coherent and appropriate outputs that meet the user's intent.
        
        ## Rating Scale
        
        ### [1] Completely Irrelevant Response
        - Fails to address any aspect of the query
        - Contains information entirely unrelated to the question
        - Shows no understanding of the user's intent
        
        **Example**
        Query: What are the environmental benefits of electric vehicles?
        Response: Basketball was invented in 1891 by James Naismith. The first game used a peach basket and a soccer ball.
        
        ### [2] Mostly Irrelevant Response
        - Addresses the query topic superficially or tangentially
        - Contains mostly unrelated information with minimal relevance
        - Misinterprets the main focus of the question
        
        **Example**
        Query: How can I improve my public speaking skills?
        Response: Communication can happen through various channels. Some people prefer written forms like email, while others use body language to express themselves.
        
        ### [3] Partially Relevant Response
        - Addresses some aspects of the query but misses key points
        - Contains a mix of relevant and irrelevant information
        - Partially misinterprets the intent or scope of the question
        
        **Example**
        Query: What are the health benefits of a Mediterranean diet?
        Response: Diets are important for health maintenance. The Mediterranean region has nice weather and beautiful coastlines. Some foods in this region include olive oil and fish.
        
        ### [4] Mostly Relevant Response
        - Addresses most aspects of the query effectively
        - Contains predominantly relevant information with minor gaps
        - Demonstrates good understanding of the intent behind the question
        
        **Example**
        Query: What causes climate change and how can individuals help reduce it?
        Response: Climate change is primarily caused by greenhouse gas emissions from burning fossil fuels. Individuals can help by reducing energy consumption, using public transportation, and recycling.
        
        ### [5] Highly Relevant Response
        - Comprehensively addresses all aspects of the query
        - Contains precisely relevant information without unnecessary tangents
        - Demonstrates complete understanding of the intent and nuances of the question
        
        **Example**
        Query: What are the pros and cons of remote work?
        Response: Remote work offers several advantages, including flexibility in schedule and location, elimination of commuting time and costs, and potential for better work-life balance. However, it also presents challenges such as isolation, difficulty separating work from personal life, potential communication barriers, and technical issues. Some workers also report missing the social aspects and spontaneous collaboration of office environments.
        
        # Evaluation Task
        
        ## Input Data
        QUERY: {{query}}
        RESPONSE: {{response}}
        
        ## Output Requirements
        Provide your evaluation using an integer score (1-5) based on the relevance rating scale. Reply with only the score without any additional text or explanation.
        """

        query = data["query"]
        completion = data["response"]

        user_prompt = user_prompt.replace("{{response}}", completion)
        user_prompt = user_prompt.replace("{{query}}", query)

        model_response = self.completion(system_prompt, user_prompt)

        return model_response.response


relevance = Relevance
