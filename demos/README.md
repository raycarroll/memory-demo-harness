# Demo Scripts

Pre-defined conversation flows that showcase memory value through automated playback.

## Available Demos

### 1. Quick Wins (5 minutes)
**Persona:** Data Scientist  
**Best for:** First-time viewers, quick showcases

Shows immediate memory benefits:
- Remembers Python preference
- Provides targeted examples
- Highlights token savings

**Key metrics:** Highlights, token efficiency

### 2. ROI Showcase (7 minutes)
**Persona:** Data Scientist  
**Best for:** Stakeholders, cost-focused audience

Emphasizes business value:
- Cumulative token savings
- Cost reduction calculation
- Quality improvement scores

**Key metrics:** Token savings (30-45%), quality scores

### 3. SRE Workflow (6 minutes)
**Persona:** SRE On-call  
**Best for:** Technical audience, operational teams

Shows operational efficiency:
- CLI-first responses
- Incident response flow
- Troubleshooting acceleration

**Key metrics:** Response quality, efficiency

### 4. Developer Onboarding (8 minutes)
**Persona:** Full-stack Developer  
**Best for:** Developer teams, onboarding scenarios

Demonstrates learning acceleration:
- Personalized guidance
- Stack-specific answers
- Consistent context

**Key metrics:** Highlights, quality scores

### 5. Family Helper (6 minutes)
**Persona:** Busy Parent  
**Best for:** Non-technical audiences, general public, families

Shows everyday practical use:
- Meal planning with dietary needs
- Family activity suggestions
- Shopping recommendations
- Budget-conscious tips

**Key metrics:** Highlights, relevance, efficiency across topics

## How to Use

### In the UI

1. **Select mode:** "Demo Playback"
2. **Choose script:** Select from dropdown
3. **Load:** Click "📜 Load Demo Script"
4. **Play:** Click "▶️ Next Step" to advance
5. **Watch:** Annotations explain what to notice

### Auto-Advance (Coming Soon)

Future: "▶️ Auto-Play" button for hands-free demos

## Demo Script Format

Each step includes:
- **User message:** What to ask
- **Annotation:** What to point out to audience
- **Wait time:** Pause duration (for auto-play)
- **Highlight metrics:** Which stats to emphasize

## Creating Custom Demos

Edit `demo_player.py` and add to `DEMO_SCRIPTS`:

```python
"my-demo": DemoScript(
    name="My Demo",
    description="Demo description",
    persona="data-scientist",  # or sre-oncall, developer
    memory_backend="dict",
    enable_judge=True,
    steps=[
        DemoStep(
            user_message="Your question here",
            annotation="🎯 **Point:** What to notice",
            wait_seconds=6.0,
            highlight_metrics=["scores", "tokens"]
        ),
        # More steps...
    ]
)
```

## Tips for Effective Demos

### Pacing
- 6-8 seconds per step minimum
- Longer for complex responses
- Leave time for audience questions

### Annotations
- Start with emoji for visual cue
- Use **bold** for key points
- Keep under 2 lines

### Metrics to Highlight
- `highlights` - Memory-influenced text
- `tokens` - Token count comparison
- `scores` - Judge quality scores
- `token_savings` - Cumulative efficiency

### Storytelling
- Start simple (build memory)
- Show immediate benefit (first query)
- Build complexity (multiple turns)
- End with cumulative stats

## Demo Flow Example

**Quick Wins Demo:**
1. **Setup** (Step 1): User states preference → Memory stores it
2. **Payoff** (Step 2): Next query uses preference → Highlight yellow markers
3. **Efficiency** (Step 3): Fewer clarifications → Show token savings
4. **Quality** (Step 4): Better answers → Compare judge scores

## Metrics to Watch

### During Demo
- Yellow highlights appearing (memory usage)
- Token count growing slower on left
- Higher scores on left panel
- Fewer clarifying questions

### After Demo
- Total token savings (30-45% typical)
- Quality delta (+2-3 points average)
- Turns saved (1-2 fewer clarifications)

## Troubleshooting

**Steps not advancing:**
- Check if driver is initialized
- Verify persona is loaded
- Enable judge if script requires it

**Annotations not showing:**
- Look above the chat columns
- Check for info banner

**Demo resets unexpectedly:**
- Click "Exit Demo" first
- Then reload script
