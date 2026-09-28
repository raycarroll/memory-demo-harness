"""Goal definitions for simulated mode."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from outcome_verification import OutcomeCheck


class GoalType(Enum):
    """Type of goal - determines what success looks like."""
    INFORMATION = "information_gathering"  # Research, learn, gather data
    SOLVE = "problem_solving"             # Fix bugs, resolve issues
    DECIDE = "decision_making"            # Choose between options
    CREATE = "artifact_creation"          # Build documents, presentations
    PLAN = "planning"                     # Schedule, organize, coordinate


@dataclass
class Goal:
    """A user goal for simulated mode with verifiable outcome.

    Example:
        goal = Goal(
            goal_type=GoalType.SOLVE,
            description="Fix CrashLoopBackOff in memoryhub-api pod",
            required_tools=["kubectl", "file_read"],
            outcome_check=OutcomeCheck(
                instruction="Verify the memoryhub-api pod is running",
                required_tools=["kubectl"],
                success_criteria="Pod status is Running with no crash loops"
            )
        )
    """

    # What kind of goal
    goal_type: GoalType

    # What specifically (natural language)
    description: str

    # Tools agent needs to achieve it
    required_tools: list[str]

    # How to verify success
    outcome_check: OutcomeCheck

    # Optional: Safety constraints
    max_turns: int = 30
    timeout_minutes: int = 15

    # Optional: Additional context
    context: str = None  # Background information for the agent

    # Track progress
    current_turn: int = 0
    completed: bool = False
    success: bool = False


# Pre-built goal templates

def create_pod_fix_goal(pod_label: str, namespace: str = "default") -> Goal:
    """Goal: Fix a failing pod.

    Example:
        goal = create_pod_fix_goal("app=memoryhub-api", "memoryhub")
    """
    return Goal(
        goal_type=GoalType.SOLVE,
        description=f"Fix the pod with label {pod_label} in namespace {namespace}",
        required_tools=["kubectl", "file_read"],
        outcome_check=OutcomeCheck(
            instruction=f"Verify the pod with label {pod_label} is running in {namespace}",
            required_tools=["kubectl"],
            success_criteria="Pod status is Running with no crash loops"
        ),
        context=f"The pod is currently failing. Investigate logs, check configuration, and fix the issue."
    )


def create_research_goal(
    topic: str,
    output_file: str = "/tmp/research_report.md",
    min_sources: int = 5
) -> Goal:
    """Goal: Research a topic and create a report.

    Example:
        goal = create_research_goal(
            topic="Competitive AI memory systems",
            output_file="/tmp/competitor_analysis.md",
            min_sources=5
        )
    """
    return Goal(
        goal_type=GoalType.INFORMATION,
        description=f"Research {topic} and create a comprehensive report",
        required_tools=["web_search", "file_write", "file_read"],
        outcome_check=OutcomeCheck(
            instruction=f"Check if research report exists at {output_file}",
            required_tools=["file_read"],
            success_criteria=f"""Report exists at {output_file} with:
            - At least {min_sources} distinct sources/competitors covered
            - Key sections: features, pricing, architecture
            - Minimum 2000 words
            - Clear comparison and analysis"""
        ),
        context=f"Research {topic}. Create a thorough report comparing different options."
    )


def create_decision_goal(
    decision: str,
    options: list[str],
    output_file: str = "/tmp/decision.md"
) -> Goal:
    """Goal: Make a decision between options.

    Example:
        goal = create_decision_goal(
            decision="Should we close Texas or Ohio plant?",
            options=["Close Texas plant", "Close Ohio plant", "Keep both open"],
            output_file="/tmp/plant_decision.md"
        )
    """
    options_str = ", ".join(options)

    return Goal(
        goal_type=GoalType.DECIDE,
        description=decision,
        required_tools=["database_query", "file_write", "file_read"],
        outcome_check=OutcomeCheck(
            instruction=f"Check if decision document exists at {output_file}",
            required_tools=["file_read"],
            success_criteria=f"""Decision document exists with:
            - Clear recommendation stated
            - All options evaluated: {options_str}
            - At least 3 trade-offs identified per option
            - Data/evidence cited to support recommendation
            - Confidence level stated"""
        ),
        context=f"Analyze the options: {options_str}. Make a recommendation with clear reasoning."
    )


def create_deployment_goal(
    service_name: str,
    target_version: str,
    namespace: str = "default"
) -> Goal:
    """Goal: Deploy a specific version.

    Example:
        goal = create_deployment_goal(
            service_name="memory-hub-mcp",
            target_version="v1.2.3",
            namespace="memory-hub-mcp"
        )
    """
    return Goal(
        goal_type=GoalType.SOLVE,
        description=f"Deploy {service_name} version {target_version} to {namespace}",
        required_tools=["kubectl", "oc"],
        outcome_check=OutcomeCheck(
            instruction=f"Verify {service_name} is running {target_version} in {namespace}",
            required_tools=["kubectl", "oc"],
            success_criteria=f"""Deployment successful:
            - Image tag contains '{target_version}'
            - All pods are ready
            - Rollout is complete
            - No errors in recent logs"""
        ),
        context=f"Deploy version {target_version}. Verify deployment completes successfully."
    )


def create_document_goal(
    document_type: str,
    output_file: str,
    requirements: list[str]
) -> Goal:
    """Goal: Create a document.

    Example:
        goal = create_document_goal(
            document_type="Board presentation for Q3",
            output_file="/tmp/q3_board.pptx",
            requirements=[
                "At least 10 slides",
                "Q3 financial data included",
                "Charts and visualizations",
                "Executive summary first slide"
            ]
        )
    """
    requirements_str = "\n- ".join(requirements)

    return Goal(
        goal_type=GoalType.CREATE,
        description=f"Create {document_type}",
        required_tools=["data_query", "file_write", "file_read"],
        outcome_check=OutcomeCheck(
            instruction=f"Check if {document_type} exists at {output_file}",
            required_tools=["file_read"],
            success_criteria=f"""Document complete:
- {requirements_str}"""
        ),
        context=f"Create {document_type} meeting all requirements."
    )


def create_plan_goal(
    plan_description: str,
    output_file: str = "/tmp/plan.md",
    days_ahead: int = 7
) -> Goal:
    """Goal: Create a plan.

    Example:
        goal = create_plan_goal(
            plan_description="Next week's facility visits (Texas and Ohio)",
            output_file="/tmp/facility_visit_plan.md",
            days_ahead=7
        )
    """
    return Goal(
        goal_type=GoalType.PLAN,
        description=f"Plan {plan_description}",
        required_tools=["calendar_read", "file_write", "file_read"],
        outcome_check=OutcomeCheck(
            instruction=f"Check if plan exists at {output_file}",
            required_tools=["file_read"],
            success_criteria=f"""Plan is complete and executable:
            - All activities scheduled with specific dates/times
            - Travel time calculated
            - Resources allocated
            - No conflicts with existing commitments
            - Covers next {days_ahead} days
            - Can start executing tomorrow"""
        ),
        context=f"Create actionable plan for: {plan_description}"
    )


# Example: Executive scenario from our demo
EXECUTIVE_FIX_INVENTORY_GOAL = Goal(
    goal_type=GoalType.SOLVE,
    description="Fix inventory accuracy from 73% to 95% within 90 days to save Midwest Healthcare contract",
    required_tools=["database_query", "file_write", "file_read"],
    outcome_check=OutcomeCheck(
        instruction="Check if action plan exists to fix inventory accuracy",
        required_tools=["file_read"],
        success_criteria="""Action plan document exists with:
        - Root cause analysis of why accuracy is at 73%
        - Specific corrective actions with owners
        - Timeline showing path to 95% in 90 days
        - Weekly milestones defined
        - Risk mitigation strategies
        - Success metrics to track progress"""
    ),
    context="""Context from persona:
    - Current inventory accuracy: 73% (should be 95%)
    - Deadline: 90 days or lose Midwest Healthcare contract
    - Medical device manufacturing (quality failures = patient deaths)
    - Inherited from predecessor who retired suddenly
    - Legacy ERP system reports are mostly garbage
    - Have three department heads: Sarah (trusted), Tom (hostile), and one more
    """
)

EXECUTIVE_PATRICIA_COUNTER_GOAL = Goal(
    goal_type=GoalType.DECIDE,
    description="Build counter-argument to Patricia Chen's Ohio plant closure proposal",
    required_tools=["database_query", "file_write", "file_read"],
    outcome_check=OutcomeCheck(
        instruction="Check if counter-argument document exists",
        required_tools=["file_read"],
        success_criteria="""Counter-argument document exists with:
        - Data showing Ohio plant value (efficiency, capacity, strategic importance)
        - Financial impact analysis of closure
        - Alternative cost-saving proposals
        - Risk assessment of closure
        - Clear talking points for board meeting
        - Confidence level in recommendation"""
    ),
    context="""Context:
    - Patricia Chen is difficult board member pushing for Ohio closure
    - Texas plant: 2 shifts, Ohio plant: 3 shifts (but lower efficiency)
    - Board meeting next week (first Tuesday)
    - Recently promoted (6 weeks in role), need to establish credibility
    - Ohio closure decision could define your tenure
    """
)
