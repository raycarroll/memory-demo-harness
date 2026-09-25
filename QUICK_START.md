# Quick Start Guide

Get the demo running in 5 minutes.

## 1. Clone and Install

```bash
git clone https://github.com/your-org/memory-demo-harness
cd memory-demo-harness
pip install -r requirements.txt
```

## 2. Set API Key

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env
```

## 3. Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

## 4. Try It Out

### First Demo: Building Memory

1. **Configure (sidebar):**
   - Agent: "Openai Chat"
   - Memory: "Dict"
   - Persona: "None (Empty)"

2. **Type:** "I'm a data scientist who prefers Python"

3. **Observe:**
   - Left panel stores this fact
   - Right panel doesn't

4. **Type:** "How do I read a CSV?"

5. **Compare:**
   - **Left:** Uses Python (remembered preference)
   - **Right:** Asks "which language?"

### Second Demo: Pre-loaded Persona

1. **Select:**
   - Persona: "Alex Chen - Data Scientist"
   - Memory: "Dict"

2. **Click:** "🔄 New Session"
   - See: "Pre-loaded 13 memories"

3. **Enable:** "☑ Enable LLM-as-Judge"

4. **Type:** "How do I deploy a model to Kubernetes?"

5. **See:**
   - Yellow highlights on memory-influenced text
   - Scores: 8.5 vs 6.0
   - Tokens: ~35% savings

### Third Demo: Memory Inspector

1. **While conversation is running**

2. **Click:** "🔍 Inspect Memories" (sidebar)

3. **Modal shows:**
   - List of stored facts
   - Weights/ordering
   - Export option

4. **Click outside to close**

## What's Happening

```
                WITHOUT Memory          WITH Memory
                ──────────────          ───────────
User query  →   Generic response        Personalized response
                Asks clarifications     Direct answer
                More tokens            Fewer tokens
                Lower quality score    Higher quality score
```

## Next Steps

- **Try different personas** - SRE, Developer
- **Enable judge** - See quantified scores
- **Inspect memories** - View what's stored
- **Export conversation** - Save for analysis

## Troubleshooting

**"OPENAI_API_KEY not set"**
- Edit `.env` file
- Add your key
- Restart Streamlit

**No highlights appearing**
- Enable "LLM-as-Judge" checkbox
- Click "New Session"
- Send a message

**Slow responses**
- Judge mode adds ~2 seconds (3 LLM calls)
- Disable judge for faster testing

## Learn More

- [Full README](README.md) - Complete documentation
- [Examples](examples/) - More configurations
- [Docs](docs/) - Technical deep-dives
- [Contributing](CONTRIBUTING.md) - Add backends/features
