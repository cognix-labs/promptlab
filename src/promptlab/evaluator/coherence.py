from promptlab.evaluator.evaluator import Evaluator


class Coherence(Evaluator):
    def evaluate(self, data: dict):
        system_prompt = """
        # Role
        You are an expert evaluator assessing the coherence quality of responses from language models. Your task is to provide objective scoring using a defined 5-point scale.
        
        # Approach
        - Analyze how logically organized the ideas are in the response
        - Evaluate if there's a clear flow of thoughts that directly addresses the query
        - Assess the use of transitions between ideas and paragraphs
        - Rate based on defined coherence levels from 1 (incoherent) to 5 (highly coherent)
        """

        user_prompt = """
        # Coherence Evaluation Framework
        
        ## Definition
        **Coherence** is the logical and ordered presentation of ideas with clear connections between concepts, enabling readers to follow the writer's thought process. A coherent response directly addresses the question with proper transitions and logical sequencing.
        
        ## Rating Scale
        
        ### [1] Incoherent Response
        - Contains disjointed words/phrases without meaningful sentences
        - No logical connection to the query
        - Completely incomprehensible
        
        **Example**
        Query: What are the benefits of renewable energy?
        Response: Wind sun green jump apple silence over.
        
        ### [2] Poorly Coherent Response
        - Shows minimal coherence with fragmented sentences
        - Contains relevant keywords but lacks logical structure
        - Difficult to understand overall message
        
        **Example**
        Query: How does vaccination work?
        Response: Vaccines protect disease. Immune system fight. Health better.
        
        ### [3] Partially Coherent Response
        - Partially addresses the query with some relevant information
        - Has issues in logical flow and organization
        - Contains unclear connections requiring reader completion
        
        **Example**
        Query: What causes earthquakes?
        Response: Earthquakes happen when tectonic plates move suddenly. Energy builds up then releases. Ground shakes and can cause damage.
        
        ### [4] Coherent Response
        - Effectively addresses the query with logical organization
        - Has clear connections between sentences and paragraphs
        - Uses appropriate transitions making it easy to follow
        
        **Example**
        Query: Describe the role of mitochondria in cellular function.
        Response: Mitochondria are organelles that produce energy for the cell. They convert nutrients into ATP through cellular respiration. This energy powers various cellular activities, making mitochondria vital for cell survival.
        
        ### [5] Highly Coherent Response
        - Exceptionally coherent with sophisticated organization
        - Presents ideas logically with excellent transitions
        - Enhances understanding through clear concept connections
        
        **Example**
        Query: Analyze the economic impacts of climate change on coastal cities.
        Response: Climate change significantly affects the economies of coastal cities through rising sea levels, increased flooding, and more intense storms. These environmental changes can damage infrastructure, disrupt businesses, and lead to costly repairs. For instance, frequent flooding can hinder transportation and commerce, while the threat of severe weather may deter investment and tourism. Consequently, cities may face increased expenses for disaster preparedness and mitigation efforts, straining municipal budgets and impacting economic growth.
        
        # Evaluation Task
        
        ## Input Data
        QUERY: {{query}}
        RESPONSE: {{response}}
        
        ## Output Requirements
        Provide your evaluation using an integer score (1-5) based on the coherence rating scale. Reply with only the score without any additional text or explanation.
        """

        query = data["query"]
        completion = data["response"]

        user_prompt = user_prompt.replace("{{response}}", completion)
        user_prompt = user_prompt.replace("{{query}}", query)

        model_response = self.completion(system_prompt, user_prompt)

        return model_response.response


coherence = Coherence
