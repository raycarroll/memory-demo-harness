# Demo Playback - Quick Start

Run pre-scripted conversations to showcase memory value in presentations.

## Launch Demo Mode

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **Select "Demo Playback" mode**
   - Radio button in sidebar

3. **Choose a demo script**
   - Quick Wins (5 min) - First-time viewers
   - ROI Showcase (7 min) - Stakeholders
   - SRE Workflow (6 min) - Technical audience  
   - Developer Onboarding (8 min) - Dev teams

4. **Load the demo**
   - Click "📜 Load Demo"
   - See script info: steps and duration

5. **Run through steps**
   - Click "▶️ Next Step" to advance
   - Watch annotation banner (tells you what to point out)
   - Wait for both sides to respond
   - Compare highlights, scores, tokens
   - Repeat until complete

## Example: Quick Wins Demo

```
Step 1/4: "I'm a data scientist who prefers Python over R"
Annotation: 🎯 Watch: Left panel stores this preference automatically
[Both respond, memory inspector shows 1 fact stored]

Step 2/4: "How do I read a CSV file?"
Annotation: 💡 Compare: Left uses Python, Right asks clarification
[Yellow highlights on "with pandas" in left response]

Step 3/4: "Show me an example"
Annotation: ⚡ Efficiency: Left gives code immediately
[Token delta: ~900 left vs ~1,400 right]

Step 4/4: "How do I handle missing values?"
Annotation: 🎯 Result: Check cumulative stats
[Final stats: 30-35% savings, +2-3 quality points]
```

## Tips for Presenters

### Pacing
- **Don't rush** - Let responses fully render
- **Point at screen** - Direct attention to highlights
- **Pause for questions** - After each step
- **Read annotations** - They're your script

### What to Emphasize
- **Yellow highlights** (Step 2) - "See where it used memory"
- **Token counts** (Step 3) - "Notice the efficiency"
- **Judge scores** (Step 4) - "Quality + savings"
- **Sidebar stats** (End) - "30-35% cost reduction"

### Handling Questions

**Q: "Does it work with our stack?"**
A: Yes - bring your own memory backend (mem0, Zep, custom).

**Q: "What if the memory is wrong?"**
A: Click "Inspect Memories" to view/export what's stored.

**Q: "How accurate is the judge?"**
A: It's using the same LLM (GPT-4 or Claude) - reliable qualitative comparison.

## Customizing Demos

See [demos/README.md](demos/README.md) for:
- Creating custom scripts
- Editing annotations
- Changing personas
- Adding steps

## Troubleshooting

**Demo won't load**
- Check sidebar config (agent, memory backend)
- Verify API key in .env
- "New Session" to reset state

**Steps advance too fast**
- Take time to explain each step
- No auto-advance (you control pacing)

**Highlights don't appear**
- Enable "LLM-as-Judge" in sidebar
- Judge extracts segments for highlighting

**Different results than expected**
- LLM responses vary - exact text may differ
- Metrics (tokens, scores) should be similar
- Retry with "New Session" if needed

## Next Steps

After running a demo:
1. Switch to "User-Driven" mode
2. Ask audience questions
3. Let them see custom queries
4. Show memory inspector
5. Export memories to text

This proves the system works beyond scripted demos.
