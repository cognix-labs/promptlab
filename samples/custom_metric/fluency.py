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

                    # Ratings
                    ## [Fluency: 1] (Emergent Fluency)
                    **Definition:** The feedback shows minimal command of the language. It contains pervasive grammatical errors, extremely limited vocabulary, and fragmented or incoherent sentences. The message is largely incomprehensible, making understanding very difficult.

                    **Examples:**
                    **FEEDBACK:** Free time I. Go park. Not fun. Alone.

                    **FEEDBACK:** Like food pizza. Good cheese eat.

                    ## [Fluency: 2] (Basic Fluency)
                    **Definition:** The feedback communicates simple ideas but has frequent grammatical errors and limited vocabulary. Sentences are short and may be improperly constructed, leading to partial understanding. Repetition and awkward phrasing are common.

                    **Examples:**
                    **FEEDBACK:** I like play soccer. I watch movie. It fun.

                    **FEEDBACK:** My town small. Many people. We have market.

                    ## [Fluency: 3] (Competent Fluency)
                    **Definition:** The feedback clearly conveys ideas with occasional grammatical errors. Vocabulary is adequate but not extensive. Sentences are generally correct but may lack complexity and variety. The text is coherent, and the message is easily understood with minimal effort.

                    **Examples:**
                    **FEEDBACK:** I'm planning to visit friends and maybe see a movie together.

                    **FEEDBACK:** I try to eat healthy food and exercise regularly by jogging.

                    ## [Fluency: 4] (Proficient Fluency)
                    **Definition:** The feedback is well-articulated with good control of grammar and a varied vocabulary. Sentences are complex and well-structured, demonstrating coherence and cohesion. Minor errors may occur but do not affect overall understanding. The text flows smoothly, and ideas are connected logically.

                    **Examples:**
                    **FEEDBACK:** My interest in mathematics and problem-solving inspired me to become an engineer, as I enjoy designing solutions that improve people's lives.

                    **FEEDBACK:** Environmental conservation is crucial because it protects ecosystems, preserves biodiversity, and ensures natural resources are available for future generations.

                    ## [Fluency: 5] (Exceptional Fluency)
                    **Definition:** The feedback demonstrates an exceptional command of language with sophisticated vocabulary and complex, varied sentence structures. It is coherent, cohesive, and engaging, with precise and nuanced expression. Grammar is flawless, and the text reflects a high level of eloquence and style.

                    **Examples:**
                    **FEEDBACK:** Globalization exerts a profound influence on cultural diversity by facilitating unprecedented cultural exchange while simultaneously risking the homogenization of distinct cultural identities, which can diminish the richness of global heritage.

                    **FEEDBACK:** Technology revolutionizes modern education by providing interactive learning platforms, enabling personalized learning experiences, and connecting students worldwide, thereby transforming how knowledge is acquired and shared.


                    # Data
                    FEEDBACK: {{feedback}}


                    # Tasks
                    ## Please provide your assessment Score for the previous FEEDBACK based on the Definitions above. The Score you give MUST be a integer score (i.e., "1", "2"...) based on the levels of the definitions. Only reply with the numeric score. Do not add any other text or explanation score.
                        """
        
        inference = data["response"]

        user_prompt = user_prompt.replace("{{feedback}}", inference)

        inference_result = self.inference_model.invoke(system_prompt, user_prompt)

        return inference_result.inference    