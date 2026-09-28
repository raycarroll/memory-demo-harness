# Simulated Mode - Goal-Based Verification

Autonomous agent execution with **measurable outcomes**, not just conversation metrics.

## The Problem with Traditional Simulated Mode

**Old approach:**
```python
# Run conversation for 20 turns
# Check: "Did we discuss the solution?"
# Result: ❓ Maybe? Subjective.
```

**New approach:**
```python
# Run until goal achieved
# Check: "Is the pod actually Running?"
# Result: ✓ or ✗ Objective, verifiable.
```

## How It Works

### 1. Define a Goal

Use natural language + tools + success criteria:

```python
from simulated_goals import Goal, GoalType
from outcome_verification import OutcomeCheck

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
```

### 2. Run Simulation

Agent works autonomously toward goal:

```python
from simulated_mode import SimulatedMode

simulator = SimulatedMode(driver, verifier)
result = simulator.run(goal)
```

### 3. Verify Outcome

LLM checks if goal achieved using tools:

```python
print(f"Success: {result.final_verification.status}")
print(f"Evidence: {result.final_verification.evidence}")
# Evidence: "Pod is in Running state with 0 restarts"
```

## Goal Types

### Information Gathering
**Example:** Research competitive AI memory systems

**Success:** Report file exists with ≥5 competitors analyzed

```python
goal = create_research_goal(
    topic="AI memory systems",
    output_file="/tmp/analysis.md",
    min_sources=5
)
```

### Problem Solving
**Example:** Fix CrashLoopBackOff pod

**Success:** Pod status = Running

```python
goal = create_pod_fix_goal(
    pod_label="app=memoryhub-api",
    namespace="memoryhub"
)
```

### Decision Making
**Example:** Should we close Texas or Ohio plant?

**Success:** Decision document with recommendation + trade-offs

```python
goal = create_decision_goal(
    decision="Which plant to close?",
    options=["Texas", "Ohio", "Neither"],
    output_file="/tmp/decision.md"
)
```

### Artifact Creation
**Example:** Create board presentation

**Success:** PowerPoint file with ≥10 slides

```python
goal = create_document_goal(
    document_type="Q3 board presentation",
    output_file="/tmp/q3_board.pptx",
    requirements=["10+ slides", "Financial charts", "Executive summary"]
)
```

### Planning
**Example:** Plan facility visits

**Success:** Schedule with dates, travel times, no conflicts

```python
goal = create_plan_goal(
    plan_description="Next week's facility visits",
    output_file="/tmp/visit_plan.md",
    days_ahead=7
)
```

## LLM-Based Verification

Instead of rigid command parsing:

```python
# Old (rigid, complex)
verification=CommandVerification(
    command="kubectl get pod -l app=memoryhub-api -o jsonpath='{.items[0].status.phase}'"
),
expected=Expected(MatchType.EQUALS, "Running")

# New (flexible, simple)
OutcomeCheck(
    instruction="Check if memoryhub-api pod is running",
    required_tools=["kubectl"],
    success_criteria="Pod status is Running"
)
```

**Agent figures out HOW to verify** - uses appropriate kubectl commands, checks output, reports verdict.

### Verification Prompt

Agent receives:

```
You are verifying if a goal has been achieved.

Goal: Fix CrashLoopBackOff in memoryhub-api pod

Verification Task: Check if memoryhub-api pod is running

Success Criteria: Pod status is Running with no crash loops

Available Tools: kubectl

Instructions:
1. Use tools to check current state
2. Gather specific evidence
3. Compare against success criteria
4. Report PASS or FAIL

Output Format:
VERDICT: PASS or FAIL
EVIDENCE: What you observed
REASONING: Why this meets/fails criteria
```

### Agent Response

```
VERDICT: PASS
CONFIDENCE: 1.0

EVIDENCE:
- Executed: kubectl get pod -l app=memoryhub-api -n memoryhub
- Output: NAME: memoryhub-api-7d9f8c-xyz, STATUS: Running, RESTARTS: 0
- Pod has been running for 2m without crashes

REASONING:
Success criteria requires "Pod is Running with no crash loops"
- Status is "Running" ✓
- Restart count is 0 (no crashes) ✓
All criteria met.
```

## Strict Validators (Optional)

For critical checks, add fallback validator:

```python
import subprocess

def strict_pod_check():
    """Precise check: is pod Running?"""
    output = subprocess.check_output(
        "kubectl get pod -l app=memoryhub-api -o jsonpath='{.items[0].status.phase}'"
    ).decode().strip()
    return output == "Running"

outcome = OutcomeCheck(
    instruction="Check if pod is running",
    required_tools=["kubectl"],
    success_criteria="Pod status is Running",
    
    strict_validator=strict_pod_check,
    strict_on_ambiguity=True  # Use strict if LLM result unclear
)
```

**When to use:**
- Critical infrastructure checks
- Security-sensitive verifications
- Need 100% precision

**When not needed:**
- Document quality checks (subjective)
- Research completeness (flexible)
- Most planning/decision goals

## Metrics That Matter

### Before (Conversation Metrics)
```python
metrics = {
    "turns_used": 8,
    "topics_discussed": 3,
    "recommendations_given": 2
}
# ❓ Did it work? Unknown.
```

### After (Outcome Metrics)
```python
metrics = {
    "initial_state": "CrashLoopBackOff",
    "final_state": "Running",  # ✓ Measurable
    "goal_achieved": True,
    "time_to_success": 45,
    "tokens_with_memory": 1200,
    "tokens_without_memory": 2100,
    "efficiency_gain": "43% savings"
}
# ✓ Did it work? YES. Verifiable.
```

## Executive Scenario Example

From our demo persona:

```python
from simulated_goals import EXECUTIVE_FIX_INVENTORY_GOAL

goal = EXECUTIVE_FIX_INVENTORY_GOAL
# Goal: Fix inventory accuracy from 73% to 95% in 90 days

# Success criteria:
# - Action plan document exists
# - Root cause analysis included
# - Timeline to 95% in 90 days
# - Weekly milestones defined
# - Risk mitigation strategies
# - Success metrics to track

result = simulator.run(goal, persona_context=executive_seed)

# Outcome: Does action plan exist meeting all criteria?
# Not: "Did we talk about fixing inventory?"
```

## Memory's Impact - Measured

With tangible outcomes, you can measure memory's real value:

**Without memory:**
- 15 turns to create action plan
- 3,200 tokens
- Missing context (had to re-explain Patricia Chen, Tom, Sarah)
- Generic plan

**With memory:**
- 9 turns to create action plan
- 1,900 tokens (41% savings)
- Includes specific people, constraints, politics
- Actionable plan tailored to situation

**Verification proves it:**
```
VERDICT: PASS (with memory) vs FAIL (without memory)

EVIDENCE:
With memory: Plan includes Patricia Chen counter-strategy,
delegates to Sarah (trusted), addresses Tom's resistance,
fits within 5-7 PM family constraint.

Without memory: Generic inventory improvement plan,
doesn't account for board politics or team dynamics.
```

## UI Integration (Future)

```
┌──────────────────────────────────────────────────┐
│ Simulated Mode: Fix Inventory Accuracy          │
├──────────────────────────────────────────────────┤
│ Status: In Progress                              │
│ Progress: ████████░░ 8/15 turns                  │
│                                                  │
│ Goal: Fix inventory from 73% to 95% in 90 days  │
│                                                  │
│ Current State:                                   │
│ • Analyzing root causes                          │
│ • Identified legacy ERP as primary issue         │
│ • Drafting corrective action plan                │
│                                                  │
│ Last Verification (Turn 5):                      │
│ Status: ❌ FAIL                                  │
│ Reason: Action plan not yet complete             │
│                                                  │
│ Metrics:                                         │
│ • Tokens (with memory):    1,234                 │
│ • Tokens (without memory): 2,100                 │
│ • Savings: 41%                                   │
│                                                  │
│ [Pause] [Stop] [Skip to End]                    │
└──────────────────────────────────────────────────┘
```

## Key Benefits

✅ **Objective outcomes** - Not "did we talk about it" but "is it done"  
✅ **Natural language** - Easy to define, no complex verification code  
✅ **Tool-enabled** - Agent can actually DO things, not just discuss  
✅ **Flexible** - LLM figures out how to verify  
✅ **Safe** - Strict validators for critical checks  
✅ **Measurable ROI** - Real efficiency gains, not proxy metrics  

## Next Steps

1. **Try examples:** `python examples/simulated_mode_example.py`
2. **Create custom goal:** Use templates in `simulated_goals.py`
3. **Test with personas:** Load executive/SRE/developer context
4. **Measure impact:** Compare with/without memory on real goals

This transforms simulated mode from **vague conversation** to **measurable achievement**.
