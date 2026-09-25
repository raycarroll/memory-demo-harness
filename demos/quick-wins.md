# Quick Wins Demo Script

**Duration:** 5 minutes  
**Persona:** Data Scientist (Alex Chen)  
**Best for:** First-time viewers, quick showcases

## Script

### Step 1: Setup (6 sec)
**User:** "I'm a data scientist who prefers Python over R"

**Annotation:** 🎯 **Watch:** Left panel stores this preference automatically

**What happens:**
- Left: Stores "prefers Python over R"
- Right: Acknowledges but doesn't store
- Memory inspector shows 1 new fact

### Step 2: First Payoff (8 sec)
**User:** "How do I read a CSV file?"

**Annotation:** 💡 **Compare:** Left uses Python (remembered!), Right asks 'which language?'

**What to point out:**
- Yellow highlights on "with pandas" or "Python"
- Left gives direct pandas example
- Right asks clarifying questions
- Token count: ~900 vs ~1,400

### Step 3: Efficiency (8 sec)
**User:** "Show me an example"

**Annotation:** ⚡ **Efficiency:** Left gives pandas code immediately, Right still clarifying

**What to point out:**
- Left provides code snippet
- Right asks "which library?"
- Cumulative tokens: ~1,800 vs ~2,900
- Judge scores: ~8.5 vs ~6.0

### Step 4: Final Comparison (8 sec)
**User:** "How do I handle missing values?"

**Annotation:** 🎯 **Result:** Left continues with pandas context, Right generic answer

**What to point out:**
- Sidebar stats:
  - Token savings: 30-35%
  - Quality delta: +2-3 points
  - Memory delta highlighted
- Total: ~2,700 vs ~4,300 tokens

## Key Talking Points

### After Step 1
"Notice the left panel automatically stored the Python preference. The right panel just acknowledged it."

### After Step 2
"See the yellow highlights? That's where the left agent used the stored memory. The right agent is asking which language to use - wasting a round trip."

### After Step 3
"We're seeing cumulative efficiency. Every question on the left gets straight to the answer because it remembers context."

### After Step 4
"Final stats: 35% token savings, 2.5 point quality improvement. That's the ROI of memory."

## Metrics Summary

**Expected results:**
- Token savings: 30-35%
- Quality improvement: +2-3 points
- Turns saved: 1-2 clarifications
- Highlights: 3-5 segments per response

## Audience Q&A Prep

**Q: "Does it work with our memory system?"**
A: Yes, it's backend-agnostic. We support MemoryHub, mem0, Zep, or custom backends.

**Q: "What if the memory is wrong?"**
A: The inspector shows what's stored. You can correct or delete entries.

**Q: "How much does memory cost?"**
A: Net savings. Memory adds small context overhead but eliminates expensive clarification rounds.

## Tips

- Pause after each step for questions
- Open memory inspector after step 1
- Point at yellow highlights in step 2
- Show sidebar stats in step 4
- Keep under 5 minutes total
