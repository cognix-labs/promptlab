from promptlab.evaluator.evaluator import Evaluator


class Groundedness(Evaluator):
    def evaluate(self, data: dict):
        system_prompt = """
        # Role
        You are an expert evaluator assessing the groundedness of AI-generated responses. Your task is to provide an objective scoring using a defined 5-point scale.
        
        # Approach
        - Analyze how well the claims in the response are supported by the provided context
        - Check if each factual statement in the response can be directly verified in the context
        - Identify any claims that lack explicit support in the context
        - Rate based on the groundedness levels from 1 (least grounded) to 5 (most grounded)
        """

        user_prompt = """
        # Groundedness Evaluation Framework
        
        ## Definition
        **Groundedness** measures how well the claims in an AI-generated response are supported by the provided context. A response is considered grounded only if its claims can be directly verified against the given sources (e.g., input documents or databases). Even factually accurate statements will be marked as ungrounded if they lack explicit support in the referenced context.
        
        ## Rating Scale
        
        ### [1] Ungrounded Response
        - Contains multiple claims with no support in the context
        - Includes significant fabrications or hallucinations
        - Presents information contradictory to the context
        
        **Example**
        Context: "The company was founded in 2010 and specializes in renewable energy solutions."
        Response: "The company was established in 1995 and is a leader in artificial intelligence and machine learning technologies."
        
        ### [2] Minimally Grounded Response
        - Contains mostly ungrounded claims with few supported statements
        - Includes notable fabrications beyond reasonable completion
        - Shows minimal relationship to the provided context
        
        **Example**
        Context: "The electric vehicle has a range of 300 miles and can be charged in 45 minutes at fast-charging stations."
        Response: "The electric vehicle can travel 300 miles on a single charge. It features leather seats, voice recognition, and can park itself automatically. Charging takes less than an hour."
        
        ### [3] Partially Grounded Response
        - Contains a mix of grounded and ungrounded claims
        - Makes some reasonable completions but goes beyond context in places
        - Has clear connections to the context but includes unsupported details
        
        **Example**
        Context: "Studies show that regular exercise can reduce the risk of heart disease by up to 30%."
        Response: "Research indicates that regular physical activity can lower heart disease risk by up to 30%. Exercise also improves mental health and helps with weight management."
        
        ### [4] Mostly Grounded Response
        - Contains predominantly grounded claims with minimal unsupported information
        - Makes reasonable completions closely tied to the context
        - Presents information largely aligned with the provided context
        
        **Example**
        Context: "The new policy will take effect on January 1, 2023, and will require all employees to complete cybersecurity training quarterly instead of annually."
        Response: "Starting January 1, 2023, the policy will change to mandate quarterly cybersecurity training for all staff members, replacing the previous annual requirement."
        
        ### [5] Fully Grounded Response
        - Contains only claims directly supported by the context
        - Makes no unsupported statements or fabrications
        - Presents information that can be completely verified from the context
        
        **Example**
        Context: "Paris, the capital of France, is known for the Eiffel Tower which was completed in 1889 and stands at 324 meters tall."
        Response: "Paris is France's capital city and home to the Eiffel Tower, a structure that was finished in 1889 and has a height of 324 meters."
        
        # Evaluation Task
        
        ## Input Data
        {query_section}
        RESPONSE: {{response}}
        CONTEXT: {{context}}
        
        ## Output
        Determine the appropriate groundedness score for the RESPONSE above based on the provided scale. Your evaluation MUST yield a single integer rating (e.g., "1", "2", etc.) corresponding to the defined levels. Provide ONLY the numerical score without any accompanying explanation or commentary.

        """

        # Check if query is provided and create the query section accordingly
        query_section = ""
        if "query" in data:
            query_section = "QUERY: {{query}}\n"
            user_prompt = user_prompt.replace("{{query}}", data["query"])
        else:
            # Remove the query section placeholder if no query is provided
            user_prompt = user_prompt.replace("{query_section}", "")

        completion = data["response"]
        context = data["context"]

        user_prompt = user_prompt.replace("{{response}}", completion)
        user_prompt = user_prompt.replace("{{context}}", context)

        if query_section:
            user_prompt = user_prompt.replace("{query_section}", query_section)

        model_response = self.completion(system_prompt, user_prompt)

        return model_response.response


groundedness = Groundedness
