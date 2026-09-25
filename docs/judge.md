# LLM-as-Judge Evaluation

Per-turn quality evaluation that measures how well each response aligns with the user's memories and preferences.

## How It Works

After each turn, a judge LLM evaluates both responses on:

1. **Relevance** - Does it answer the question?
2. **Accuracy** - Is the information correct?
3. **Memory Alignment** - Does it use known preferences/context?
4. **Specificity** - Is it tailored vs generic?
5. **Efficiency** - Gets to answer without clarifications?

## Output

```
⚖️ Score: 8.5/10
   Correctly used Python preference and provided
   pandas-specific example matching user's known tools
```

**Scores:**
- `0-10` scale per response
- Higher = better quality and memory alignment
- Delta shows memory advantage

## UI Display

### Per-Turn Scores

Expandable cards below each response:
```
⚖️ Score: 8.5/10 (click to expand)
  → Justification appears
```

### Aggregate Stats

Sidebar shows running averages:
```
Average Scores (0-10)
  With Memory:    8.5
  Without Memory: 6.2
  Memory Δ:      +2.3
```

## Evaluation Prompt

The judge receives:

```
## User's Pre-existing Memories/Context
- User prefers Python over R
- User works in ML Ops on Kubernetes
- User has limited GPU budget
...

## User Query
How do I deploy a model?

## Response A (with memory)
[response using context]

## Response B (without memory)  
[generic response]
```

Then scores each on 0-10 scale with justification.

## Example Verdicts

### High Memory Alignment

```
Query: "How do I read a CSV?"

Response A (WITH memory): 9.0/10
"Immediately provided pandas example matching
 user's Python preference. No wasted explanation
 of alternatives."

Response B (WITHOUT memory): 6.5/10
"Correct but generic. Listed Python, R, Excel
 options without knowing user's preference."

Delta: +2.5
```

### Low Memory Impact

```
Query: "What is Kubernetes?"

Response A (WITH memory): 7.5/10
"Good definition. Memory didn't add much since
 this is a factual question."

Response B (WITHOUT memory): 7.0/10
"Similar quality. Slight edge to A for mentioning
 container orchestration in user's context."

Delta: +0.5
```

## Enable/Disable

**In UI:**
- Sidebar → "Evaluation" section
- Toggle "Enable LLM-as-Judge"

**Note:** Adds ~1-2 seconds per turn (extra LLM call)

## Cost Impact

Each evaluation is one LLM call with:
- Input: User query + both responses + memories (~500-1000 tokens)
- Output: Scores + justifications (~150-300 tokens)

**Estimate:** ~$0.01-0.02 per evaluation with GPT-4o

## Technical Details

**Judge Backend:** `judge.py`
- `ResponseJudge` class wraps any `AgentBackend`
- Currently uses same model as main agent
- Could be configured to use cheaper model (e.g., GPT-4o-mini for judge)

**Verdict Schema:**
```python
@dataclass
class JudgeVerdict:
    left_score: float           # 0-10
    right_score: float          # 0-10
    left_justification: str
    right_justification: str
    memory_alignment_delta: float  # left - right
```

**Parsing:**
- Judge outputs structured text:
  ```
  RESPONSE_A_SCORE: 8.5
  RESPONSE_A_JUSTIFICATION: ...
  RESPONSE_B_SCORE: 6.0
  RESPONSE_B_JUSTIFICATION: ...
  ```
- Parser extracts scores and justifications

## Use Cases

**Sales Demos:**
- Quantify memory value with numbers
- Show 2-3 point improvement in scores

**Research:**
- Measure memory impact across personas
- Compare memory backend quality

**Internal Testing:**
- A/B test memory system changes
- Validate memory extraction quality

## Limitations

- Judge quality depends on judge model
- Subjective evaluation (not ground truth)
- Adds latency to each turn
- Cost increases with evaluations

## Future Enhancements

- [ ] Configurable judge model (cheaper option)
- [ ] Multi-criteria breakdown (relevance, accuracy, etc.)
- [ ] Batch evaluation mode (judge after conversation)
- [ ] Export verdicts to CSV/JSON
- [ ] Judge disagreement detection
