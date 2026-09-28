"""LLM-based outcome verification for simulated goals."""

from dataclasses import dataclass
from typing import Callable, Optional
from enum import Enum
from datetime import datetime


class VerificationStatus(Enum):
    """Verification result status."""
    PASS = "pass"
    FAIL = "fail"
    AMBIGUOUS = "ambiguous"
    ERROR = "error"


@dataclass
class VerificationResult:
    """Result of an outcome verification check."""
    status: VerificationStatus
    evidence: str  # What was observed
    reasoning: str  # Why it passed/failed
    timestamp: datetime
    confidence: float = 1.0  # 0-1, how confident in the verdict
    strict_mode_used: bool = False
    error: str = None


@dataclass
class OutcomeCheck:
    """LLM-based goal verification with optional strict fallback.

    Example:
        outcome = OutcomeCheck(
            instruction="Check if the memoryhub-api pod is running",
            required_tools=["kubectl"],
            success_criteria="Pod status is Running with no crash loops"
        )
    """

    # Natural language verification instruction
    instruction: str

    # Tools the agent needs to perform verification
    required_tools: list[str]

    # What success looks like (natural language)
    success_criteria: str

    # Optional: When to run this check
    check_timing: str = "after_each_turn"  # "after_each_turn", "end", "every_5_turns"

    # Optional: Strict validator for critical checks
    strict_validator: Optional[Callable[[], bool]] = None

    # Optional: Force strict mode (skip LLM verification)
    use_strict: bool = False

    # Optional: Fall back to strict if LLM result is ambiguous
    strict_on_ambiguity: bool = True


class OutcomeVerifier:
    """Executes outcome verification using LLM or strict validators."""

    def __init__(self, agent_backend):
        """Initialize with agent backend for LLM verification.

        Args:
            agent_backend: AgentBackend instance with tool access
        """
        self.agent = agent_backend

    def verify(self, goal_description: str, outcome_check: OutcomeCheck) -> VerificationResult:
        """Verify if outcome has been achieved.

        Args:
            goal_description: The original goal being verified
            outcome_check: How to verify it

        Returns:
            VerificationResult with status and evidence
        """

        # Force strict mode if requested
        if outcome_check.use_strict and outcome_check.strict_validator:
            return self._run_strict_check(outcome_check.strict_validator)

        # Try LLM verification
        try:
            llm_result = self._run_llm_verification(goal_description, outcome_check)

            # Fall back to strict if ambiguous and available
            if (llm_result.status == VerificationStatus.AMBIGUOUS and
                outcome_check.strict_validator and
                outcome_check.strict_on_ambiguity):
                return self._run_strict_check(outcome_check.strict_validator)

            return llm_result

        except Exception as e:
            # LLM verification failed, try strict if available
            if outcome_check.strict_validator:
                return self._run_strict_check(outcome_check.strict_validator)

            return VerificationResult(
                status=VerificationStatus.ERROR,
                evidence="",
                reasoning="",
                timestamp=datetime.now(),
                error=str(e)
            )

    def _run_llm_verification(self, goal_description: str, outcome_check: OutcomeCheck) -> VerificationResult:
        """Ask LLM to verify outcome using natural language criteria."""

        prompt = f"""You are verifying if a goal has been achieved.

**Goal**: {goal_description}

**Verification Task**: {outcome_check.instruction}

**Success Criteria**: {outcome_check.success_criteria}

**Available Tools**: {', '.join(outcome_check.required_tools)}

**Instructions**:
1. Use the provided tools to check the current state
2. Gather specific evidence (command outputs, file contents, API responses)
3. Compare what you observe against the success criteria
4. Make a clear PASS or FAIL determination

Be precise and cite actual values you observe (e.g., pod status, file size, version numbers).

**Output Format** (use this exact format):

VERDICT: PASS or FAIL or AMBIGUOUS
CONFIDENCE: 0.0 to 1.0 (how certain you are)
EVIDENCE:
<What you observed - be specific>

REASONING:
<Why this meets or fails the success criteria>

**Notes**:
- PASS means all success criteria are met
- FAIL means at least one criterion is not met
- AMBIGUOUS means you cannot determine (missing tools, unclear state, etc.)
- Include specific values and command outputs in EVIDENCE
"""

        # Execute verification with tools
        response = self.agent.send([{"role": "user", "content": prompt}])

        # Parse response
        return self._parse_verification_response(response.content)

    def _parse_verification_response(self, content: str) -> VerificationResult:
        """Parse LLM verification response into structured result."""

        lines = content.strip().split('\n')

        verdict = VerificationStatus.AMBIGUOUS
        confidence = 0.5
        evidence = ""
        reasoning = ""

        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith("VERDICT:"):
                verdict_str = line.split(":", 1)[1].strip().upper()
                if "PASS" in verdict_str:
                    verdict = VerificationStatus.PASS
                elif "FAIL" in verdict_str:
                    verdict = VerificationStatus.FAIL
                else:
                    verdict = VerificationStatus.AMBIGUOUS

            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.split(":", 1)[1].strip())
                except ValueError:
                    confidence = 0.5

            elif line.startswith("EVIDENCE:"):
                current_section = "evidence"
                evidence_text = line.split(":", 1)[1].strip()
                if evidence_text:
                    evidence = evidence_text

            elif line.startswith("REASONING:"):
                current_section = "reasoning"
                reasoning_text = line.split(":", 1)[1].strip()
                if reasoning_text:
                    reasoning = reasoning_text

            elif current_section == "evidence" and line:
                evidence += "\n" + line

            elif current_section == "reasoning" and line:
                reasoning += "\n" + line

        return VerificationResult(
            status=verdict,
            evidence=evidence.strip(),
            reasoning=reasoning.strip(),
            timestamp=datetime.now(),
            confidence=confidence,
            strict_mode_used=False
        )

    def _run_strict_check(self, validator: Callable[[], bool]) -> VerificationResult:
        """Run strict validator function for precise verification."""

        try:
            passed = validator()

            return VerificationResult(
                status=VerificationStatus.PASS if passed else VerificationStatus.FAIL,
                evidence="Strict validator executed",
                reasoning=f"Validator returned {passed}",
                timestamp=datetime.now(),
                confidence=1.0,
                strict_mode_used=True
            )

        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.ERROR,
                evidence="",
                reasoning="",
                timestamp=datetime.now(),
                confidence=0.0,
                strict_mode_used=True,
                error=str(e)
            )


# Example outcome checks for common goal types

def create_pod_running_check(pod_label: str, namespace: str = "default") -> OutcomeCheck:
    """Create check for pod running state."""
    return OutcomeCheck(
        instruction=f"Verify the pod with label {pod_label} is running in namespace {namespace}",
        required_tools=["kubectl"],
        success_criteria="Pod status is Running with no recent crash loops (restart count stable)"
    )


def create_file_exists_check(file_path: str, min_size_kb: int = None) -> OutcomeCheck:
    """Create check for file existence and size."""
    size_criteria = f" and is at least {min_size_kb}KB" if min_size_kb else ""

    return OutcomeCheck(
        instruction=f"Check if file exists at {file_path}",
        required_tools=["file_read", "bash"],
        success_criteria=f"File exists at {file_path}{size_criteria}"
    )


def create_api_health_check(url: str, expected_status: str = "healthy") -> OutcomeCheck:
    """Create check for API health endpoint."""
    return OutcomeCheck(
        instruction=f"Check if API at {url} is healthy",
        required_tools=["http_request"],
        success_criteria=f"API returns status '{expected_status}' and responds within 5 seconds"
    )


def create_deployment_version_check(
    deployment_name: str,
    namespace: str,
    expected_version: str
) -> OutcomeCheck:
    """Create check for deployment image version."""
    return OutcomeCheck(
        instruction=f"Verify deployment {deployment_name} in namespace {namespace} is running version {expected_version}",
        required_tools=["kubectl", "oc"],
        success_criteria=f"Deployment image tag contains '{expected_version}' and all pods are ready"
    )


def create_document_completeness_check(
    file_path: str,
    required_sections: list[str],
    min_words: int = None
) -> OutcomeCheck:
    """Create check for document completeness."""
    sections_str = ", ".join(required_sections)
    word_criteria = f" with at least {min_words} words" if min_words else ""

    return OutcomeCheck(
        instruction=f"Check if document at {file_path} is complete",
        required_tools=["file_read"],
        success_criteria=f"Document contains all required sections: {sections_str}{word_criteria}"
    )
