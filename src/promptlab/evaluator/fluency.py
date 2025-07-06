from promptlab.evaluator.evaluator import Evaluator


class Fluency(Evaluator):
    def evaluate(self, data: dict):
        system_prompt = """
                        # Evaluation Guidelines
                        ## Primary Objective
                        ### You are a linguistic expert specializing in assessing the language quality of AI-generated RESPONSES. Your assessment will follow the framework provided below.
                        - **Evaluation Framework**: You will use the detailed linguistic criteria provided to guide your scoring.
                        - **Input Material**: You will analyze a RESPONSE text passage.
                        - **Evaluation Process**: Your assessment must result in a precise numerical rating based strictly on the provided criteria.
                    """

        user_prompt = """
                    # Conceptual Framework
                    **Linguistic Articulacy** measures how effectively and elegantly ideas are communicated in writing. It encompasses syntactic precision, lexical diversity, structural sophistication, textual flow, and overall comprehensibility. This metric quantifies how seamlessly thoughts are articulated and how readily the content can be processed by readers.

                    # Assessment Scale
                    ## [Linguistic Articulacy: 1] (Rudimentary Expression)
                    **Definition:** The response exhibits elementary language control with prevalent syntactical errors, severely restricted vocabulary, and disconnected or incomplete sentence structures. The content is predominantly unclear, creating significant comprehension barriers.

                    **Examples:**
                    **RESPONSE:** Yesterday go concert. Sound bad. People many. Leave early.

                    **RESPONSE:** Computer problem have. Screen black. Try button many time.

                    ## [Linguistic Articulacy: 2] (Developing Expression)
                    **Definition:** The response conveys basic concepts but contains numerous grammatical inconsistencies and limited word choices. Sentences tend to be simplistic and occasionally malformed, resulting in partial message clarity. Redundancy and awkward constructions predominate.

                    **Examples:**
                    **RESPONSE:** I read book yesterday. Story was good. Main character have problem.

                    **RESPONSE:** Weather today very cold. Need wear jacket. Sky have clouds.

                    ## [Linguistic Articulacy: 3] (Functional Expression)
                    **Definition:** The response effectively communicates ideas with periodic grammatical lapses. Vocabulary is sufficient though not particularly rich. Sentence construction is generally accurate but lacks variation and complexity. The text maintains coherence and the message is readily comprehensible.

                    **Examples:**
                    **RESPONSE:** The conference offered several interesting workshops about digital marketing strategies.

                    **RESPONSE:** I found the historical documentary informative, although some parts were overly simplified.

                    ## [Linguistic Articulacy: 4] (Refined Expression)
                    **Definition:** The response is skillfully crafted with strong grammatical control and diverse vocabulary. Sentences exhibit complexity and structural variety, demonstrating clear logical progression. Occasional minor language imperfections do not hinder comprehension. The narrative flows naturally with effective transitional elements.

                    **Examples:**
                    **RESPONSE:** The integration of artificial intelligence into healthcare systems presents both promising opportunities for improved diagnostics and significant challenges regarding patient privacy.

                    **RESPONSE:** Throughout history, artistic movements have often emerged as responses to societal changes, reflecting the cultural values and political tensions of their respective eras.

                    ## [Linguistic Articulacy: 5] (Masterful Expression)
                    **Definition:** The response showcases exemplary language mastery with sophisticated lexical choices and intricate, varied syntactic patterns. It demonstrates impeccable coherence, compelling rhetorical flow, and precise expression of nuanced concepts. Grammatical execution is flawless, and the text exhibits remarkable eloquence and stylistic refinement.

                    **Examples:**
                    **RESPONSE:** The inexorable advancement of quantum computing portends a paradigmatic shift in cryptographic security protocols, necessitating the development of post-quantum algorithms capable of withstanding computational approaches that exploit fundamental quantum mechanical principles.

                    **RESPONSE:** Contemporary literary criticism increasingly acknowledges the intricate interplay between authorial intent and reader interpretation, recognizing how cultural contexts and individual experiences inevitably influence the construction of textual meaning in ways that transcend traditional hermeneutic frameworks.


                    # Evaluation Material
                    RESPONSE: {{feedback}}


                    # Assessment Task
                    ## Determine the appropriate Linguistic Articulacy score for the RESPONSE above based on the provided scale. Your evaluation MUST yield a single integer rating (e.g., "1", "2", etc.) corresponding to the defined levels. Provide ONLY the numerical score without any accompanying explanation or commentary.
                        """

        completion = data["response"]

        user_prompt = user_prompt.replace("{{feedback}}", completion)

        model_response = self.completion(system_prompt, user_prompt)

        return model_response.response


fluency = Fluency
