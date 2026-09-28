"""Example: Running simulated mode with goal-based verification.

This shows how to:
1. Define a goal with natural language verification
2. Run autonomous simulation to achieve it
3. Get measurable outcome (not just "did we talk enough")
"""

from simulated_goals import (
    Goal,
    GoalType,
    create_pod_fix_goal,
    create_research_goal,
    create_decision_goal,
    EXECUTIVE_FIX_INVENTORY_GOAL
)
from outcome_verification import OutcomeCheck, OutcomeVerifier
from simulated_mode import SimulatedMode
from dual_driver import DualDriver
from agent_backends import create_agent_backend
from memory_backends import create_memory_backend


# Example 1: Fix a failing pod
def example_pod_fix():
    """Goal: Fix CrashLoopBackOff pod - measurable outcome is pod Running."""

    # Create goal
    goal = create_pod_fix_goal(
        pod_label="app=memoryhub-api",
        namespace="memoryhub"
    )

    # Setup driver and verifier
    agent = create_agent_backend({"provider": "openai", "model": "gpt-4o"})
    memory = create_memory_backend({"type": "dict"})
    driver = DualDriver(agent, memory, judge=None)
    verifier = OutcomeVerifier(agent)

    # Run simulation
    simulator = SimulatedMode(driver, verifier)
    result = simulator.run(goal)

    # Check outcome
    print(f"Goal: {goal.description}")
    print(f"Turns used: {result.turn}/{goal.max_turns}")
    print(f"Success: {result.final_verification.status.value}")
    print(f"Evidence: {result.final_verification.evidence}")
    print(f"Reasoning: {result.final_verification.reasoning}")

    # Measurable outcome: Is pod actually running?
    # (Not: "did we talk about how to fix it?")


# Example 2: Research task with document output
def example_research():
    """Goal: Research competitors - measurable outcome is report file exists."""

    goal = create_research_goal(
        topic="AI memory systems (MemoryHub, mem0, Zep, LangChain)",
        output_file="/tmp/competitor_analysis.md",
        min_sources=5
    )

    agent = create_agent_backend({"provider": "openai", "model": "gpt-4o"})
    memory = create_memory_backend({"type": "dict"})
    driver = DualDriver(agent, memory, judge=None)
    verifier = OutcomeVerifier(agent)

    simulator = SimulatedMode(driver, verifier)
    result = simulator.run(goal)

    print(f"Success: {result.final_verification.status.value}")
    print(f"Report created: /tmp/competitor_analysis.md")

    # Measurable outcome: Does file exist with ≥5 competitors covered?
    # Agent verifies by reading file and checking content


# Example 3: Executive decision with strict validator
def example_decision_with_strict_check():
    """Goal: Make decision - with optional strict validator for critical check."""

    import os

    def strict_check_file_exists():
        """Fallback: Precisely check if decision file exists."""
        return os.path.exists("/tmp/plant_decision.md")

    goal = Goal(
        goal_type=GoalType.DECIDE,
        description="Should we close Texas or Ohio plant?",
        required_tools=["database_query", "file_write", "file_read"],
        outcome_check=OutcomeCheck(
            instruction="Check if decision document exists at /tmp/plant_decision.md",
            required_tools=["file_read"],
            success_criteria="""Decision document exists with clear recommendation,
            trade-offs for each option, and data-backed reasoning""",

            # Optional: Strict validator if LLM verification is ambiguous
            strict_validator=strict_check_file_exists,
            strict_on_ambiguity=True
        ),
        context="""Texas plant runs 2 shifts, Ohio runs 3 shifts.
        Ohio has lower efficiency but higher capacity.
        Board member Patricia Chen is pushing for Ohio closure."""
    )

    agent = create_agent_backend({"provider": "openai", "model": "gpt-4o"})
    memory = create_memory_backend({"type": "dict"})
    driver = DualDriver(agent, memory, judge=None)
    verifier = OutcomeVerifier(agent)

    simulator = SimulatedMode(driver, verifier)
    result = simulator.run(goal)

    print(f"Decision made: {result.final_verification.status.value}")
    print(f"Strict mode used: {result.final_verification.strict_mode_used}")

    # If LLM verification was ambiguous, falls back to strict_check_file_exists()


# Example 4: Real executive scenario from demo
def example_executive_scenario():
    """Goal: Executive under pressure - complex multi-faceted goal."""

    goal = EXECUTIVE_FIX_INVENTORY_GOAL  # From simulated_goals.py

    # Load executive persona
    with open("seeds/executive.txt") as f:
        persona_context = f.read()

    agent = create_agent_backend({"provider": "openai", "model": "gpt-4o"})
    memory = create_memory_backend({"type": "dict"}, seed_file="seeds/executive.txt")
    driver = DualDriver(agent, memory, judge=None)
    verifier = OutcomeVerifier(agent)

    simulator = SimulatedMode(driver, verifier)
    result = simulator.run(goal, persona_context=persona_context)

    print(f"Goal: {goal.description}")
    print(f"Success: {result.final_verification.status.value}")
    print(f"Evidence:\n{result.final_verification.evidence}")
    print(f"\nWith memory - Tokens: {result.total_tokens_left}")
    print(f"Without memory - Tokens: {result.total_tokens_right}")
    print(f"Savings: {((result.total_tokens_right - result.total_tokens_left) / result.total_tokens_right * 100):.1f}%")

    # Measurable outcome: Does action plan exist with all required elements?
    # Shows memory's impact on complex real-world scenario


# Example 5: Custom goal from scratch
def example_custom_goal():
    """Define a completely custom goal."""

    goal = Goal(
        goal_type=GoalType.CREATE,
        description="Create Q3 board presentation with financial data",
        required_tools=["data_query", "chart_generate", "file_write", "file_read"],
        outcome_check=OutcomeCheck(
            instruction="Check if Q3 board presentation exists",
            required_tools=["file_read"],
            success_criteria="""PowerPoint file exists at /tmp/q3_board.pptx with:
            - At least 10 slides
            - Q3 revenue and expense charts
            - Executive summary on first slide
            - YoY comparison data
            - Professional formatting"""
        ),
        context="Q3 revenue was $2.3M (up 15% YoY), expenses $1.8M (up 8% YoY)"
    )

    agent = create_agent_backend({"provider": "openai", "model": "gpt-4o"})
    memory = create_memory_backend({"type": "dict"})
    driver = DualDriver(agent, memory, judge=None)
    verifier = OutcomeVerifier(agent)

    simulator = SimulatedMode(driver, verifier)
    result = simulator.run(goal)

    print(f"Presentation created: {result.final_verification.status.value}")

    # Measurable outcome: Does presentation file exist with required content?


if __name__ == "__main__":
    print("Simulated Mode Examples")
    print("=" * 50)

    print("\n1. Pod Fix Goal")
    print("-" * 50)
    example_pod_fix()

    print("\n2. Research Goal")
    print("-" * 50)
    example_research()

    print("\n3. Decision with Strict Validator")
    print("-" * 50)
    example_decision_with_strict_check()

    print("\n4. Executive Scenario")
    print("-" * 50)
    example_executive_scenario()

    print("\n5. Custom Goal")
    print("-" * 50)
    example_custom_goal()
