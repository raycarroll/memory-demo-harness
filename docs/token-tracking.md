# Token Tracking

Real-time token usage monitoring to quantify the efficiency gains of memory-enabled agents.

## What It Tracks

### Per-Turn Metrics
Each response shows:
```
🔢 1,234 tokens (567 in + 667 out)
```

- **Input tokens:** Context + user message
- **Output tokens:** Generated response  
- **Total:** Sum of both

### Cumulative Stats (Sidebar)

```
Token Usage
With Memory:    3,245
Without Memory: 5,892  (-2,647)

💰 45% token savings with memory
```

**Metrics:**
- Total tokens per agent
- Delta (difference)
- Efficiency percentage

## Why It Matters

### Cost Savings
```
Example (GPT-4o pricing):
- Input:  $2.50 / 1M tokens
- Output: $10.00 / 1M tokens

Without memory: 5,892 tokens → $0.05
With memory:    3,245 tokens → $0.03
Savings:        45% → $0.02 per conversation
```

At scale (1000 conversations/day):
- Without memory: $50/day
- With memory: $30/day  
- **Savings: $20/day = $600/month**

### Efficiency Gains

Memory reduces tokens by:
1. **Eliminating clarifications:** "Do you prefer Python or R?" → already knows
2. **Skip context rebuilding:** No need to re-explain preferences each turn
3. **Direct answers:** Gets to solution faster

## How It Works

### Token Collection

```python
# After each LLM call
left_resp = agent.send(messages)
# left_resp contains:
# - tokens_in: 567
# - tokens_out: 667

# Store per turn
self.left_tokens.append({
    "in": 567,
    "out": 667,
    "total": 1234
})
```

### Efficiency Calculation

```python
left_total = sum(tokens for turn in left_tokens)
right_total = sum(tokens for turn in right_tokens)

efficiency = (1 - left_total / right_total) * 100
# Example: (1 - 3245 / 5892) * 100 = 45%
```

## UI Display

### In Chat (Below Each Response)

```
┌────────────────────────────────┐
│ 🤖 Assistant:                  │
│ Here's how with pandas...      │
│                                │
│ 🔢 1,234 tokens                │  ← Per-turn count
│    (567 in + 667 out)          │
└────────────────────────────────┘
```

### In Sidebar Stats

```
📊 Stats
Left Turns:  2
Right Turns: 2
───────────────
Token Usage
With Memory:    3,245
Without Memory: 5,892  (-2,647)

💰 45% token savings with memory
───────────────
Avg Scores (0-10)
With Memory:   8.5
Without Memory: 6.0
Memory Δ:     +2.5
```

## Typical Patterns

### Memory Saves Tokens

**Common scenario:**
```
Turn 1:
  Left:  1,200 tokens (context included)
  Right: 1,000 tokens (no context yet)
  
Turn 2:
  Left:  900 tokens (uses stored context)
  Right: 1,500 tokens (asks clarifying questions)
  
Turn 3:
  Left:  1,100 tokens (builds on memory)
  Right: 1,800 tokens (rebuilds context)
  
Total:
  Left:  3,200 tokens
  Right: 4,300 tokens
  Savings: 25%
```

### Memory Adds Tokens (Rare)

**When memory doesn't help:**
```
Query: "What is 2+2?"

Left:  1,100 tokens (memory overhead unused)
Right: 900 tokens (no context needed)
Overhead: +22%
```

This happens when:
- Question is purely factual
- No personalization needed
- Memory context is noise

**Solution:** Selective memory injection (future enhancement)

## Real-World Examples

### Data Scientist Persona

**Query 1:** "I'm a data scientist who prefers Python"
```
Left:  800 tokens (stores preference)
Right: 750 tokens (acknowledges)
```

**Query 2:** "How do I read a CSV?"
```
Left:  950 tokens (uses Python pref directly)
Right: 1,400 tokens (asks "Python, R, or Excel?")
Savings: 32%
```

**Query 3:** "Show me an example"
```
Left:  1,100 tokens (pandas code based on pref)
Right: 1,600 tokens (generic examples + follow-up)
Savings: 31%
```

**Total:**
- Left: 2,850 tokens
- Right: 3,750 tokens
- **Overall savings: 24%**

### SRE On-call Persona

**Pre-loaded:** 14 facts about kubectl preference, CLI-only, etc.

**Query:** "How do I debug a pod?"
```
Left:  1,200 tokens (kubectl command immediately)
Right: 1,800 tokens (asks "UI or CLI?", "which tool?")
Savings: 33%
```

## Cost Projection Calculator

Use these formulas:

```python
# Monthly cost estimate
conversations_per_day = 1000
avg_tokens_per_conversation = 5000
days_per_month = 30

# Pricing (example: GPT-4o)
input_cost_per_1M = 2.50
output_cost_per_1M = 10.00
avg_cost_per_1M = (input_cost_per_1M + output_cost_per_1M) / 2

# Without memory
monthly_tokens = conversations_per_day * avg_tokens_per_conversation * days_per_month
monthly_cost_baseline = (monthly_tokens / 1_000_000) * avg_cost_per_1M

# With memory (assume 30% savings)
efficiency_pct = 30
monthly_cost_with_memory = monthly_cost_baseline * (1 - efficiency_pct / 100)

savings = monthly_cost_baseline - monthly_cost_with_memory
```

**Example:**
- 1000 conversations/day
- 5000 tokens/conversation
- 30% efficiency from memory
- Result: **$1,125/month savings**

## Limitations

### Current
- Token counts from LLM API (not validated)
- No judge token tracking (future)
- No cost estimation in UI (future)
- No per-persona comparison (future)

### Future Enhancements
- [ ] Cost calculator in UI (input pricing)
- [ ] Token usage graph over time
- [ ] Per-persona efficiency comparison
- [ ] Export token data to CSV
- [ ] Judge token costs tracked separately
- [ ] Breakdown by input vs output tokens

## Interpreting Results

**Good efficiency (30%+ savings):**
- Memory is valuable for this use case
- User has clear preferences/constraints
- Questions build on prior context

**Moderate efficiency (10-30% savings):**
- Some benefit from memory
- Mix of contextual and factual questions
- Typical real-world pattern

**Low/negative efficiency (<10% or negative):**
- Questions don't use memory
- Factual queries predominate
- Memory overhead > benefit

**Action:** Review persona fit or memory relevance

## Best Practices

### For Demos
1. Pre-load persona (maximizes first-turn impact)
2. Ask contextual questions (shows memory value)
3. Point out token deltas after each turn
4. Calculate monthly savings for impact

### For Testing
1. Compare same conversation with/without memory
2. Test multiple personas
3. Track efficiency over 5+ turns
4. Look for consistent savings patterns

### For Production
1. Monitor efficiency per user
2. Alert if efficiency drops (memory not helping)
3. Use as input for memory pruning decisions
4. Factor into ROI calculations
