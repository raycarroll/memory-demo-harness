"""LLM-as-judge for evaluating response quality and memory alignment."""

from dataclasses import dataclass
from typing import Optional
from agent_backends import AgentBackend

@dataclass
class JudgeVerdict:
    """Evaluation result for a response pair."""
    left_score: float  # 0-10 for response WITH memory
    right_score: float  # 0-10 for response WITHOUT memory
    left_justification: str
    right_justification: str
    memory_alignment_delta: float  # left_score - right_score
    memory_influenced_segments: list[str]  # Quotes from left response that used memory

class ResponseJudge:
    """LLM-as-judge for evaluating response quality."""

    def __init__(self, judge_backend: AgentBackend):
        self.judge = judge_backend

    def evaluate(
        self,
        user_query: str,
        left_response: str,
        right_response: str,
        memories: Optional[str] = None
    ) -> JudgeVerdict:
        """
        Evaluate both responses for quality and memory alignment.

        Args:
            user_query: The user's question
            left_response: Response WITH memory
            right_response: Response WITHOUT memory
            memories: Pre-loaded memories (if any)

        Returns:
            JudgeVerdict with scores and justifications
        """

        # Build evaluation prompt
        prompt = self._build_evaluation_prompt(
            user_query,
            left_response,
            right_response,
            memories
        )

        # Call judge LLM
        response = self.judge.send([{"role": "user", "content": prompt}])

        # Parse verdict
        return self._parse_verdict(response.content)

    def _build_evaluation_prompt(
        self,
        user_query: str,
        left_response: str,
        right_response: str,
        memories: Optional[str]
    ) -> str:
        """Build the evaluation prompt."""

        memory_context = ""
        if memories:
            memory_context = f"""
## User's Pre-existing Memories/Context
{memories}
"""

        prompt = f"""You are an expert evaluator assessing AI assistant responses.

{memory_context}

## User Query
{user_query}

## Response A (with memory context)
{left_response}

## Response B (without memory context)
{right_response}

## Evaluation Criteria

For each response, evaluate on a scale of 0-10 considering:

1. **Relevance** - Does it address the user's question?
2. **Accuracy** - Is the information factually correct?
3. **Completeness** - Does it provide sufficient detail and thoroughness?
4. **Clarity** - Is it well-structured and easy to understand?
5. **Helpfulness** - Can the user act on this response to solve their need?

Judge both responses using the SAME criteria. Do not penalize Response B for lacking memory context it doesn't have access to.

## Output Format

Provide your evaluation in this EXACT format:

RESPONSE_A_SCORE: X.X
RESPONSE_A_JUSTIFICATION: Brief explanation (1-2 sentences) on response quality - relevance, accuracy, completeness, clarity, helpfulness
MEMORY_INFLUENCED_SEGMENTS: ["quote 1 from response A that used memory", "quote 2", ...]

RESPONSE_B_SCORE: X.X
RESPONSE_B_JUSTIFICATION: Brief explanation (1-2 sentences) on response quality - relevance, accuracy, completeness, clarity, helpfulness

**For MEMORY_INFLUENCED_SEGMENTS:**
- Extract short quotes (5-15 words) from Response A that directly used the user's memories
- Include phrases that reference preferences, known tools, constraints, or context
- Use exact quotes from the response
- Return as a JSON array of strings
- If no memory was used, return: []

Be objective and fair. Judge both responses on the same quality criteria. Response A may score higher naturally due to having context, but evaluate what each response delivers, not what it had access to.
"""

        return prompt

    def _parse_verdict(self, content: str) -> JudgeVerdict:
        """Parse the judge's response into a verdict."""

        lines = content.strip().split("\n")

        left_score = 5.0
        right_score = 5.0
        left_just = "Unable to parse justification"
        right_just = "Unable to parse justification"
        segments = []

        for line in lines:
            line = line.strip()

            if line.startswith("RESPONSE_A_SCORE:"):
                try:
                    left_score = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

            elif line.startswith("RESPONSE_A_JUSTIFICATION:"):
                left_just = line.split(":", 1)[1].strip()

            elif line.startswith("MEMORY_INFLUENCED_SEGMENTS:"):
                try:
                    import json
                    segments_str = line.split(":", 1)[1].strip()
                    segments = json.loads(segments_str)
                except (ValueError, json.JSONDecodeError):
                    # Fallback: treat as comma-separated
                    segments_str = line.split(":", 1)[1].strip()
                    if segments_str and segments_str != "[]":
                        segments = [s.strip(' "[]') for s in segments_str.split(",")]

            elif line.startswith("RESPONSE_B_SCORE:"):
                try:
                    right_score = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

            elif line.startswith("RESPONSE_B_JUSTIFICATION:"):
                right_just = line.split(":", 1)[1].strip()

        return JudgeVerdict(
            left_score=left_score,
            right_score=right_score,
            left_justification=left_just,
            right_justification=right_just,
            memory_alignment_delta=left_score - right_score,
            memory_influenced_segments=segments
        )
