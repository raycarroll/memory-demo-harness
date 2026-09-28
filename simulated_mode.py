"""Simulated mode execution engine."""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from simulated_goals import Goal, GoalType
from outcome_verification import OutcomeVerifier, VerificationResult, VerificationStatus
from dual_driver import DualDriver


@dataclass
class SimulationState:
    """Current state of a simulated goal execution."""

    goal: Goal
    turn: int = 0
    started_at: datetime = None
    completed_at: datetime = None

    # Verification results
    verification_history: list[VerificationResult] = None
    final_verification: VerificationResult = None

    # Conversation history
    left_messages: list[dict] = None
    right_messages: list[dict] = None

    # Metrics
    total_tokens_left: int = 0
    total_tokens_right: int = 0

    def __post_init__(self):
        if self.verification_history is None:
            self.verification_history = []
        if self.left_messages is None:
            self.left_messages = []
        if self.right_messages is None:
            self.right_messages = []


class SimulatedMode:
    """Execute goals with autonomous agent + outcome verification.

    Flow:
    1. Agent works toward goal using tools
    2. After each turn, verify outcome
    3. Stop when goal achieved or max turns reached
    4. Report success/failure with evidence

    Example:
        driver = DualDriver(agent, memory, judge)
        verifier = OutcomeVerifier(agent)
        simulator = SimulatedMode(driver, verifier)

        goal = create_pod_fix_goal("app=memoryhub-api", "memoryhub")
        result = simulator.run(goal)

        print(f"Success: {result.final_verification.status}")
    """

    def __init__(self, driver: DualDriver, verifier: OutcomeVerifier):
        self.driver = driver
        self.verifier = verifier
        self.question_generator = QuestionGenerator()

    def run(self, goal: Goal, persona_context: str = None) -> SimulationState:
        """Run simulation to achieve goal.

        Args:
            goal: The goal to achieve
            persona_context: Optional persona background (from seed file)

        Returns:
            SimulationState with results and verification
        """

        state = SimulationState(
            goal=goal,
            started_at=datetime.now()
        )

        # Initial message to agent
        initial_prompt = self._build_initial_prompt(goal, persona_context)

        # Main execution loop
        while state.turn < goal.max_turns and not goal.completed:
            state.turn += 1

            # Generate next question/prompt
            if state.turn == 1:
                prompt = initial_prompt
            else:
                prompt = self.question_generator.generate_next(
                    goal=goal,
                    conversation_history=state.left_messages
                )

            # Execute through dual driver
            left_resp, right_resp, verdict = self.driver.execute(prompt)

            # Record messages
            state.left_messages.append({"role": "user", "content": prompt})
            state.left_messages.append({
                "role": "assistant",
                "content": left_resp.content,
                "tokens_in": left_resp.tokens_in,
                "tokens_out": left_resp.tokens_out
            })

            state.right_messages.append({"role": "user", "content": prompt})
            state.right_messages.append({
                "role": "assistant",
                "content": right_resp.content,
                "tokens_in": right_resp.tokens_in,
                "tokens_out": right_resp.tokens_out
            })

            # Update token counts
            state.total_tokens_left += left_resp.tokens_in + left_resp.tokens_out
            state.total_tokens_right += right_resp.tokens_in + right_resp.tokens_out

            # Check if goal achieved (if check timing says to)
            if self._should_verify_now(goal.outcome_check.check_timing, state.turn):
                verification = self.verifier.verify(
                    goal_description=goal.description,
                    outcome_check=goal.outcome_check
                )

                state.verification_history.append(verification)

                # Goal achieved?
                if verification.status == VerificationStatus.PASS:
                    goal.completed = True
                    goal.success = True
                    state.final_verification = verification
                    break

        # Final verification if not already done
        if not goal.completed:
            final_verification = self.verifier.verify(
                goal_description=goal.description,
                outcome_check=goal.outcome_check
            )
            state.final_verification = final_verification

            if final_verification.status == VerificationStatus.PASS:
                goal.success = True

        state.completed_at = datetime.now()

        return state

    def _build_initial_prompt(self, goal: Goal, persona_context: str = None) -> str:
        """Build initial prompt to start goal execution."""

        context_section = ""
        if goal.context:
            context_section = f"\n\n**Context**:\n{goal.context}"

        if persona_context:
            context_section += f"\n\n**Your Background**:\n{persona_context}"

        prompt = f"""You need to achieve the following goal:

{goal.description}

**Available Tools**: {', '.join(goal.required_tools)}

**Success Criteria**: {goal.outcome_check.success_criteria}{context_section}

**Instructions**:
1. Work toward achieving this goal
2. Use the available tools to gather information, make changes, or verify results
3. Be systematic and thorough
4. You have up to {goal.max_turns} turns to complete this

Start by assessing the current situation and determining what needs to be done.
"""

        return prompt

    def _should_verify_now(self, check_timing: str, current_turn: int) -> bool:
        """Determine if we should run verification check now."""

        if check_timing == "after_each_turn":
            return True
        elif check_timing == "end":
            return False  # Only check at end
        elif check_timing.startswith("every_"):
            # Parse "every_5_turns" -> check every 5 turns
            try:
                interval = int(check_timing.split("_")[1])
                return current_turn % interval == 0
            except:
                return False

        return False


class QuestionGenerator:
    """Generates follow-up questions to guide agent toward goal."""

    def generate_next(self, goal: Goal, conversation_history: list[dict]) -> str:
        """Generate next prompt based on goal type and conversation.

        For now, this is simple continuation. In future, could be smarter
        about steering agent toward completion.
        """

        # Look at last assistant message
        if len(conversation_history) >= 2:
            last_message = conversation_history[-1]["content"]

            # If agent is asking questions back, answer them
            if "?" in last_message:
                return self._answer_agent_questions(last_message, goal)

            # If agent reported doing something, ask for verification
            if any(word in last_message.lower() for word in ["completed", "fixed", "created", "deployed"]):
                return "Can you verify that worked? Check the current state."

            # If agent seems stuck, prompt action
            if any(word in last_message.lower() for word in ["need", "require", "missing"]):
                return "What specific action can you take right now to move forward?"

        # Default: continue working
        return "Continue working toward the goal. What's your next step?"

    def _answer_agent_questions(self, message: str, goal: Goal) -> str:
        """Agent asked questions - provide answers from goal context."""

        if goal.context:
            return f"Based on the context provided: {goal.context}\n\nUse this information to proceed."

        return "Use the information available through your tools to find the answer."


# UI State Management

@dataclass
class SimulationDisplay:
    """UI state for displaying simulation progress."""

    goal_description: str
    current_turn: int
    max_turns: int
    status: str  # "running", "verifying", "completed", "failed"

    # Current verification status
    last_verification: Optional[VerificationResult] = None

    # Progress indicators
    progress_percent: int = 0

    # Live metrics
    tokens_saved_percent: float = 0.0
    current_state: str = "Starting..."

    def update_from_state(self, state: SimulationState):
        """Update display from simulation state."""
        self.current_turn = state.turn
        self.progress_percent = int((state.turn / state.goal.max_turns) * 100)

        if state.verification_history:
            self.last_verification = state.verification_history[-1]

        if state.total_tokens_right > 0:
            savings = state.total_tokens_right - state.total_tokens_left
            self.tokens_saved_percent = (savings / state.total_tokens_right) * 100

        if state.goal.completed:
            self.status = "completed" if state.goal.success else "failed"
        else:
            self.status = "running"
