"""Demo script player for automated demonstrations."""

from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class DemoStep:
    """A single step in a demo script."""
    user_message: str
    annotation: str  # What to point out to the audience
    wait_seconds: float = 5.0  # How long to pause after this step
    highlight_metrics: list[str] = None  # Which metrics to emphasize

@dataclass
class DemoScript:
    """A complete demo script with metadata."""
    name: str
    description: str
    persona: str  # Which persona to load
    memory_backend: str  # Which backend to use
    enable_judge: bool
    steps: list[DemoStep]

    def total_duration(self) -> float:
        """Estimate total demo duration in seconds."""
        return sum(step.wait_seconds for step in self.steps)

# Built-in demo scripts
DEMO_SCRIPTS = {
    "quick-wins": DemoScript(
        name="Quick Wins - Memory in Action",
        description="5-minute demo showing immediate memory benefits",
        persona="data-scientist",
        memory_backend="dict",
        enable_judge=True,
        steps=[
            DemoStep(
                user_message="I'm a data scientist who prefers Python over R",
                annotation="🎯 **Watch:** Left panel stores this preference automatically",
                wait_seconds=6.0,
                highlight_metrics=["memory_stored"]
            ),
            DemoStep(
                user_message="How do I read a CSV file?",
                annotation="💡 **Compare:** Left uses Python (remembered!), Right asks 'which language?'",
                wait_seconds=8.0,
                highlight_metrics=["highlights", "tokens"]
            ),
            DemoStep(
                user_message="Show me an example",
                annotation="⚡ **Efficiency:** Left gives pandas code immediately, Right still clarifying",
                wait_seconds=8.0,
                highlight_metrics=["tokens", "scores"]
            ),
            DemoStep(
                user_message="How do I handle missing values?",
                annotation="🎯 **Result:** Left continues with pandas context, Right generic answer",
                wait_seconds=8.0,
                highlight_metrics=["scores", "token_savings"]
            ),
        ]
    ),

    "roi-showcase": DemoScript(
        name="ROI Showcase - Cost Savings",
        description="7-minute demo emphasizing token savings and efficiency",
        persona="data-scientist",
        memory_backend="dict",
        enable_judge=True,
        steps=[
            DemoStep(
                user_message="I work with large datasets in Python using pandas and scikit-learn",
                annotation="📊 **Setup:** Building memory context (stores 2 facts)",
                wait_seconds=6.0
            ),
            DemoStep(
                user_message="I have limited GPU budget for training models",
                annotation="💰 **Constraint:** Stores important context for recommendations",
                wait_seconds=6.0
            ),
            DemoStep(
                user_message="How should I deploy a machine learning model to production?",
                annotation="🎯 **Watch tokens:** Left uses context immediately (saves clarifications)",
                wait_seconds=9.0,
                highlight_metrics=["tokens"]
            ),
            DemoStep(
                user_message="What's the best way to handle model versioning?",
                annotation="💡 **Cumulative savings:** Notice token delta growing",
                wait_seconds=8.0,
                highlight_metrics=["token_savings"]
            ),
            DemoStep(
                user_message="Show me a deployment example",
                annotation="✨ **Quality + Efficiency:** Better answer AND fewer tokens",
                wait_seconds=8.0,
                highlight_metrics=["scores", "token_savings"]
            ),
        ]
    ),

    "sre-workflow": DemoScript(
        name="SRE Workflow - Incident Response",
        description="6-minute demo showing memory in operational context",
        persona="sre-oncall",
        memory_backend="dict",
        enable_judge=True,
        steps=[
            DemoStep(
                user_message="How do I check pod status in Kubernetes?",
                annotation="🔧 **Watch:** Left gives kubectl commands (knows CLI preference from persona)",
                wait_seconds=7.0,
                highlight_metrics=["highlights"]
            ),
            DemoStep(
                user_message="Pod is in CrashLoopBackOff, what should I check?",
                annotation="⚡ **Context:** Left continues with kubectl, Right might suggest UI",
                wait_seconds=8.0,
                highlight_metrics=["highlights", "scores"]
            ),
            DemoStep(
                user_message="Show me how to debug this",
                annotation="🎯 **Efficiency:** Left provides immediate kubectl commands",
                wait_seconds=8.0,
                highlight_metrics=["tokens", "scores"]
            ),
            DemoStep(
                user_message="How do I prevent this in the future?",
                annotation="📊 **Final comparison:** Check cumulative token savings",
                wait_seconds=8.0,
                highlight_metrics=["token_savings", "scores"]
            ),
        ]
    ),

    "developer-onboarding": DemoScript(
        name="Developer Onboarding",
        description="8-minute demo showing learning acceleration",
        persona="developer",
        memory_backend="dict",
        enable_judge=True,
        steps=[
            DemoStep(
                user_message="I'm new to this codebase and prefer TypeScript with React",
                annotation="👋 **Onboarding:** Memory helps personalize guidance",
                wait_seconds=6.0
            ),
            DemoStep(
                user_message="How do I create a new API endpoint?",
                annotation="🎯 **Watch:** Left uses FastAPI (knows backend preference from persona)",
                wait_seconds=8.0,
                highlight_metrics=["highlights"]
            ),
            DemoStep(
                user_message="Show me how to add input validation",
                annotation="💡 **Context-aware:** Left continues with FastAPI patterns",
                wait_seconds=8.0,
                highlight_metrics=["highlights", "scores"]
            ),
            DemoStep(
                user_message="How should I handle errors?",
                annotation="✨ **Consistency:** All answers aligned with their stack",
                wait_seconds=8.0,
                highlight_metrics=["scores"]
            ),
            DemoStep(
                user_message="What about frontend integration?",
                annotation="🔄 **Full stack:** Switches to React context seamlessly",
                wait_seconds=8.0,
                highlight_metrics=["highlights", "token_savings"]
            ),
        ]
    ),

    "family-helper": DemoScript(
        name="Family Helper - Everyday Life",
        description="6-minute demo showing memory benefits for everyday tasks (non-technical)",
        persona="busy-parent",
        memory_backend="dict",
        enable_judge=True,
        steps=[
            DemoStep(
                user_message="I need dinner ideas for tonight that my kids will actually eat",
                annotation="🏠 **Setup:** Agent learns about family (kids' ages, allergies, food preferences)",
                wait_seconds=7.0,
                highlight_metrics=["highlights"]
            ),
            DemoStep(
                user_message="What ingredients do I need for that?",
                annotation="💡 **Watch:** Left remembers the recipe context, Right asks 'for what?'",
                wait_seconds=7.0,
                highlight_metrics=["highlights", "tokens"]
            ),
            DemoStep(
                user_message="Can you suggest activities for this Saturday?",
                annotation="⚡ **Context-aware:** Left knows about soccer schedule and dog, Right gives generic ideas",
                wait_seconds=8.0,
                highlight_metrics=["highlights", "scores"]
            ),
            DemoStep(
                user_message="Where should I shop for those supplies?",
                annotation="🎯 **Personalized:** Left suggests Target (knows preference), Right asks location/budget",
                wait_seconds=7.0,
                highlight_metrics=["scores", "token_savings"]
            ),
            DemoStep(
                user_message="Any tips for keeping it affordable?",
                annotation="📊 **Final:** Check cumulative savings - fewer clarifying questions, better answers",
                wait_seconds=7.0,
                highlight_metrics=["token_savings", "scores"]
            ),
        ]
    ),
}

class DemoPlayer:
    """Manages demo script playback."""

    def __init__(self):
        self.current_script: Optional[DemoScript] = None
        self.current_step: int = 0
        self.is_playing: bool = False
        self.paused: bool = False

    def load_script(self, script_name: str) -> DemoScript:
        """Load a demo script by name."""
        if script_name not in DEMO_SCRIPTS:
            raise ValueError(f"Unknown demo script: {script_name}")

        self.current_script = DEMO_SCRIPTS[script_name]
        self.current_step = 0
        self.is_playing = False
        self.paused = False
        return self.current_script

    def get_next_step(self) -> Optional[DemoStep]:
        """Get the next demo step."""
        if not self.current_script:
            return None

        if self.current_step >= len(self.current_script.steps):
            return None

        step = self.current_script.steps[self.current_step]
        self.current_step += 1
        return step

    def reset(self):
        """Reset to beginning of script."""
        self.current_step = 0
        self.paused = False

    def get_progress(self) -> dict:
        """Get current playback progress."""
        if not self.current_script:
            return {"step": 0, "total": 0, "percent": 0}

        total = len(self.current_script.steps)
        return {
            "step": self.current_step,
            "total": total,
            "percent": int((self.current_step / total) * 100) if total > 0 else 0
        }

def get_available_demos() -> dict[str, str]:
    """Get list of available demo scripts."""
    return {
        name: script.description
        for name, script in DEMO_SCRIPTS.items()
    }
