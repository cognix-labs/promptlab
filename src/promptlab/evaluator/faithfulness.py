from promptlab.evaluator.evaluator import Evaluator
from promptlab.model.model import Model
from typing import List
import json


class Faithfulness(Evaluator):
    # Class-level prompt templates
    CLAIM_GENERATOR_SYSTEM_PROMPT = """
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

    CLAIM_GENERATOR_USER_PROMPT = """
    ### Input Query Passage
    {query_passage}

    ### Output Claims
    Determine the claims in the query passage and output them in a numbered list.
    """

    JUDGE_SYSTEM_PROMPT = """
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

    JUDGE_USER_PROMPT = """
    Below is the context and claim pair to be checked.
    ### Context
    {context}
    ### Claim
    {claim}
    """

    def __init__(self, judge_llm: Model = None, claimify_llm: Model = None):
        """
        Initialize the Faithfulness evaluator.

        Args:
            judge_llm: Dictionary containing the model for claim verification
            claimify_llm: Dictionary containing the model for claim generation
        """
        # Validate judge_llm
        if judge_llm is None:
            raise ValueError("Faithfulness evaluation requires a judge_llm model")

        # If claimify_llm is not provided, use judge_llm as fallback
        if claimify_llm is None:
            print(
                "Warning: No claim generation model is provided. Using judge_llm for claim generation."
            )
            claimify_llm = judge_llm

        self.judge_llm = judge_llm
        self.claimify_llm = claimify_llm

    def evaluate(self, data: dict) -> float:
        """
        Evaluate the faithfulness of a response against its context.

        Args:
            data: Dictionary containing:
                - query: The original query
                - context: The context to evaluate against
                - response: The response to evaluate

        Returns:
            float: Faithfulness score between 0 and 1
        """
        # Validate input data
        required_keys = ["query", "context", "response"]
        if not all(key in data for key in required_keys):
            raise ValueError(
                f"data dictionary must contain {', '.join(required_keys)} keys"
            )

        try:
            claims = self._claim_generation(data["response"])
            return self._faithfulness_evaluation(data["context"], claims)
        except Exception as e:
            raise RuntimeError(f"Error during faithfulness evaluation: {str(e)}") from e

    def _claim_generation(self, response: str) -> List[str]:
        """
        Generate claims from the response using the provided LLM.

        Args:
            response: The response text to generate claims from

        Returns:
            List of claims extracted from the response
        """
        formatted_prompt = self.CLAIM_GENERATOR_USER_PROMPT.format(
            query_passage=response
        )

        claim_generator_response = self.claimify_llm.invoke(
            system_prompt=self.CLAIM_GENERATOR_SYSTEM_PROMPT,
            user_prompt=formatted_prompt,
        )

        return claim_generator_response.completion.split("\n")

    def _faithfulness_evaluation(self, context: str, claims: List[str]) -> float:
        """
        Evaluate the faithfulness of claims against the provided context.

        Args:
            context: The context to evaluate claims against
            claims: List of claims to evaluate

        Returns:
            Faithfulness score between 0 and 1
        """
        if not claims:
            raise ValueError("No claims provided for evaluation")

        if not context:
            raise ValueError("No context provided for evaluation")

        num_supported_claims = 0

        for claim in claims:
            try:
                formatted_prompt = self.JUDGE_USER_PROMPT.format(
                    context=context, claim=claim
                )

                judgement = self.judge_llm.invoke(
                    system_prompt=self.JUDGE_SYSTEM_PROMPT, user_prompt=formatted_prompt
                ).completion

                try:
                    verdict = json.loads(judgement)["verdict"]
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Invalid JSON response from judge_llm: {judgement}"
                    ) from e
                except KeyError as e:
                    raise ValueError(
                        f"Missing 'verdict' key in judge_llm response: {judgement}"
                    ) from e

                if verdict == 1:
                    num_supported_claims += 1

            except Exception as e:
                raise RuntimeError(f"Error evaluating claim '{claim}': {str(e)}") from e

        if len(claims) == 0:
            raise ValueError("No claims were evaluated")

        return num_supported_claims / len(claims)


faithfulness = Faithfulness
