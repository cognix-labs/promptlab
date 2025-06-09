from promptlab.evaluator.evaluator import Evaluator
from promptlab.model.model import Model
import json


class Faithfulness(Evaluator):
    def evaluate(self, data: dict,
                 auxilary_llm: dict = None,
                 judge_llm: dict = None):
        
        """
        The Faithfulness metric measures how factually consistent a response is with the retrieved context.
        It ranges from 0 to 1, with higher scores indicating better consistency.
        A response is considered faithful if all its claims can be supported by the retrieved context.

        To calculate this:
        1. Identify all the claims in the response via LLM call using the auxilary_llm model
        2. Check each claim to see if it can be inferred from the retrieved context using the judge_llm model
        3. Compute the faithfulness score using the formula:
        
        Let, A = # of claims identified by claim_generator
        B = # of claims supported by the retrieved context as found by the llm_as_judge
        
        faithfulness = B/A
        """
        
        if "query" not in data or "context" not in data or "response" not in data:
            raise ValueError("data dictionary must contain 'query', 'context' and 'response' keys")
        
        if judge_llm is None:
            raise ValueError("Faithfulness uses LLM as a Judge framework. Please provide a judge_llm")
        
        # If auxilary_llm is not provided, use judge_llm as fallback
        if auxilary_llm is None:
            print("Warning: No claim generation model is provided. Using judge_llm for claim generation.")
            auxilary_llm = judge_llm
        
        try:
            claims = self.claim_generation(data["answer"], auxilary_llm.model)
            return self.faithfulness_evaluation(data["retrieved_context"], claims, judge_llm.model)
        except Exception as e:
            raise RuntimeError(f"Error during faithfulness evaluation: {str(e)}") from e
        
    def claim_generation(self,
                         query: str,
                         claim_generator_llm: Model) -> list[str]:
        
        claim_generator_system_prompt = """
        ## Task
        Read the supplied query passage and list only the factual claims it explicitly asserts.
        ### Include
        Concrete statements about specific entities, events, quantities, properties, or relations found verbatim or paraphrased from the text.
        ### Exclude
        Background knowledge, definitions, truisms, universal facts, or anything merely implied.
        ## Output
        - Return a numbered list.
        - Each item must be one atomic claim.
        - Each claim should not use any pronouns.
        - No commentary, duplicates or assumtions.
        ## Example
        <query_passage>
        "The first ever FIFA world cup took place in 1930 in Uruguay. The first ever champions of the world cup were Uruguay captained by Jose Nasazzi. The runner up was Argentina National Team captained by Juan Jose Higuain."
        </query_passage>
        <output_claims>
        1. The first ever FIFA world cup took place in 1930 in Uruguay
        2. The first ever champions of the world cup were Uruguay
        3. The first ever FIFA world cup winning captain was Jose Nasazzi
        4. The runner up was Argentina National Team
        5. The runner up of the first ever FIFA world cup was captained by Juan Jose Higuain
        </output_claims>
        """
        
        claim_generator_user_prompt = """
        ### Input Query Passage
        {query_passage}
        
        ### Output Claims
        Determine the claims in the query passage and output them in a numbered list.
        """
        
        claim_generator_user_prompt = claim_generator_user_prompt.replace("{{query_passage}}", query)
        
        claim_generator_response = claim_generator_llm.invoke(
            system_prompt=claim_generator_system_prompt,
            user_prompt=claim_generator_user_prompt
        )
        
        numbered_claims = claim_generator_response.inference.split("\n")
        
        return numbered_claims
    
    def faithfulness_evaluation(self,
                                context: str,
                                claims: list[str],
                                judge_llm: Model) -> float:
        
        if not claims:
            raise ValueError("No claims provided for evaluation")
            
        if not context:
            raise ValueError("No context provided for evaluation")
            
        judge_system_prompt = """
        ## Role
        You are an impartial fact checker. You are provided with a pair of a claim and a context. You must return verdict as 1 if the claim can be directly inferred based on the provided contex. You must return verdict as 0 if the claim cannot be directly inferred based on the provided context.
        You conduct this fact checker by reasoning step by step.
        ## Output
        - Output the judgement as a JSON with two keys: "verdict" and "reasoning"
        - "verdict" is a boolean value.
        - "reasoning" is a string that explains your reasoning.
        - Nothing other than the JSON output is allowed.
        ## Example
        <example>
        <input>
        "context": "Robert is a CS student with a particularly strong command in compilers, data structure and algorithms"
        "claim": "Robert is majoring in Music Theory"
        </input>
        <output>
        {"verdict": 0, "reasoning": "Robert is a CS student. There is no mention of Robert doing dual majors. Therefore, Robert is not majoring in Music Theory."}
        </output>
        """
        
        judge_user_prompt = """
        Below is the context and claim pair to be checked.
        ### Context
        {context}
        ### Claim
        {claim}
        """
        
        num_supported_claims = 0
        
        for claim in claims:
            try:
                formatted_prompt = judge_user_prompt.replace("{{context}}", context)
                formatted_prompt = formatted_prompt.replace("{{claims}}", claim)
                
                judgement = judge_llm.invoke(
                    system_prompt=judge_system_prompt,
                    user_prompt=formatted_prompt
                ).inference
                
                try:
                    verdict = json.loads(judgement)["verdict"]
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON response from judge_llm: {judgement}") from e
                except KeyError as e:
                    raise ValueError(f"Missing 'verdict' key in judge_llm response: {judgement}") from e
                
                if verdict == 1:
                    num_supported_claims += 1
                    
            except Exception as e:
                raise RuntimeError(f"Error evaluating claim '{claim}': {str(e)}") from e
                
        if len(claims) == 0:
            raise ValueError("No claims were evaluated")
            
        return num_supported_claims / len(claims)
            
            
        
        
        