# Memory Demo Harness

Side-by-side comparison tool for agent conversations **with** and **without** memory support.

## What It Does

Visual proof that memory improves agent quality and efficiency:

- 🎯 **Memory-influenced highlighting** - Yellow highlights show which text used stored context
- ⚖️ **LLM-as-judge scoring** - Quantified quality comparison (0-10 scores)
- 📊 **Token tracking** - See 30-45% cost savings from memory
- 🔍 **Memory inspector** - View what's stored in real-time
- 👤 **Pre-loaded personas** - Demo with 13+ facts already loaded
- 🎬 **Demo playback** - Pre-scripted conversations for hands-free presentations

## Quick Start

```bash
# Clone
git clone https://github.com/your-org/memory-demo-harness
cd memory-demo-harness

# Install
pip install -r requirements.txt

# Set API key (OpenAI or Anthropic)
export OPENAI_API_KEY="sk-..."

# Run
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

**Three modes:**
- **User-Driven** - Interactive conversation (you type questions)
- **Demo Playback** - Pre-scripted demos (automated presentations)
- **Simulated** - AI-guided conversation (coming soon)

## Live Demo

### Without Memory (Baseline)
```
User: How do I read a CSV?
Agent: You can use Python, R, or Excel. Which do you prefer?
🔢 1,400 tokens | ⚖️ 6.0/10
```

### With Memory
```
User: How do I read a CSV?
Agent: Since you prefer Python, here's how with pandas:
       ^^^^^^^^^^^^^^^^^^            ^^^^^^^^^^^
              (highlighted yellow - used memory)
       
🔢 900 tokens | ⚖️ 8.5/10 | 💰 35% savings
```

## Supported Memory Systems

Works with any memory backend that implements the `MemoryBackend` protocol:

- **Built-in:**
  - `dict` - In-memory (testing)
  - `file` - Text file with LLM extraction
  
- **Integrations:**
  - [MemoryHub](https://github.com/redhat-et/memory-hub) - Kubernetes-native MCP server
  - mem0 - Coming soon
  - Zep - Coming soon
  - LangChain memory - Coming soon

- **Custom:** Implement the `MemoryBackend` protocol (see [examples/custom_backend.py](examples/custom_backend.py))

## Features

### 1. Visual Highlighting
See **exactly** which parts of responses used memory:
- Yellow background on memory-influenced text
- Judge extracts specific quotes
- Segment count displayed

### 2. Quality Scoring
LLM-as-judge evaluates each response:
- 0-10 scores for both sides
- Detailed justifications
- Average delta tracking
- Memory alignment assessment

### 3. Token Tracking
Quantify efficiency gains:
- Per-turn token counts
- Cumulative usage comparison
- Efficiency percentage
- Cost savings calculation

### 4. Memory Inspector
View stored memories in real-time:
- Modal dialog (no scrolling)
- Export to text file
- Raw file viewer (file backend)
- Transparency for debugging

### 5. Persona Pre-population
Start with context already loaded:
- 3 built-in personas (Data Scientist, SRE, Developer)
- 13-14 facts per persona
- Custom personas via seed files
- Perfect for demos

### 6. Demo Playback
Pre-scripted conversations for presentations:
- 5 built-in demos (Quick Wins, ROI, SRE, Onboarding, Family Helper)
- Technical AND non-technical scenarios
- Step-by-step with annotations
- Highlights what to watch
- Progress tracking
- 5-8 minute durations
- Reproducible results

## Configuration

### Agent Backends

Edit `config.yaml`:

```yaml
agents:
  openai-chat:
    type: direct
    provider: openai
    model: gpt-4o
    system_prompt: "You are a helpful assistant."

  claude-sonnet:
    type: direct
    provider: anthropic
    model: claude-sonnet-4-20250514
```

### Memory Backends

```yaml
memory:
  # In-memory (resets on restart)
  dict:
    type: dict

  # File-backed (persistent)
  text-file:
    type: file
    path: ./memory/facts.txt

  # MemoryHub (MCP server)
  memoryhub:
    type: memoryhub
    url: http://localhost:8080/mcp/
    api_key: ${MEMORYHUB_API_KEY}
```

See [examples/](examples/) for more configurations.

### Personas

```yaml
personas:
  data-scientist:
    name: "Alex Chen - Data Scientist"
    description: "Senior DS, Python/ML Ops"
    seed_file: ./seeds/data-scientist.txt
```

Create custom personas: one fact per line in a text file.

## Use Cases

### 1. Sales Demos
Show memory value with visual proof:

**Interactive mode:**
- Pre-load persona
- Enable judge scoring
- Ask contextual questions
- Point out: highlights, scores, token savings

**Demo playback mode (hands-free):**
- Select "Demo Playback" mode
- Choose "quick-wins" or "roi-showcase"
- Click "Load Demo" then "Next Step"
- Annotations guide your talking points
- Reproducible, polished presentation

### 2. Testing Memory Systems
Compare backends side-by-side:
- Run same conversation
- Switch memory backend
- Compare quality and efficiency
- Validate extraction

### 3. Research
Measure memory impact quantitatively:
- Token efficiency metrics
- Quality improvement scores
- Export data for analysis
- A/B test memory strategies

### 4. Documentation
Generate comparison screenshots:
- Visual proof for docs
- Before/after examples
- ROI calculations
- Feature demonstrations

## Architecture

```
User Input
    ↓
DualDriver.execute(prompt)
    ↓
    ├─→ Left: Memory.recall() → Agent.send() → Memory.store()
    │   → Response WITH context
    │
    └─→ Right: Agent.send() (no memory)
        → Response WITHOUT context
    ↓
Judge.evaluate(left, right, memories)
    ├─→ Scores (0-10)
    ├─→ Justifications
    └─→ Memory-influenced segments (for highlighting)
    ↓
Display side-by-side with highlighting, scores, tokens
```

## Adding Custom Memory Backends

Implement the `MemoryBackend` protocol:

```python
from memory_backends import MemoryBackend

class MyMemorySystem(MemoryBackend):
    def recall(self, query: str, history: list[dict]) -> str:
        """Return memories as context string."""
        # Query your memory system
        memories = self.client.search(query)
        return "<memory>" + "\n".join(memories) + "</memory>"
    
    def store(self, user_msg: str, assistant_msg: str, history: list[dict]):
        """Store facts from this turn."""
        # Extract and store
        self.client.save(user_msg)
    
    def clear_session(self):
        """Reset session state."""
        self.session_id = None
```

Register in `memory_backends.py`:

```python
def create_memory_backend(config, ...):
    if config["type"] == "my_system":
        return MyMemorySystem(config)
```

See [examples/custom_backend.py](examples/custom_backend.py) for full example.

## Development

### Run Tests

```bash
python tests/test_basic.py
python tests/test_judge.py
python tests/test_highlighting.py
```

All tests should pass ✓

### Project Structure

```
memory-demo-harness/
├── app.py                   # Streamlit UI
├── dual_driver.py           # Parallel execution engine
├── agent_backends.py        # LLM provider adapters
├── memory_backends.py       # Memory system adapters
├── judge.py                 # LLM-as-judge evaluator
├── demo_player.py           # Demo script playback engine
├── config.yaml              # Default configuration
├── lib/
│   └── ui_components.py     # Highlighting helpers
├── seeds/                   # Pre-loaded personas
├── demos/                   # Demo scripts and guides
│   ├── README.md            # Demo usage guide
│   └── quick-wins.md        # Detailed script with talking points
├── examples/                # Example configs
├── docs/                    # Detailed documentation
└── tests/                   # Test suite
```

## Documentation

- [Judge System](docs/judge.md) - LLM-as-judge evaluation
- [Highlighting](docs/highlighting.md) - Visual memory proof
- [Token Tracking](docs/token-tracking.md) - Efficiency metrics
- [Memory Inspector](docs/memory-inspector.md) - Viewing stored memories
- [Demo Playback](demos/README.md) - Using pre-scripted demos
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues

## Contributing

Contributions welcome! Areas of interest:

- New memory backend integrations (mem0, Zep, etc.)
- Agent backend support (LangChain, LlamaIndex)
- UI improvements
- Documentation
- Test coverage

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE)

## Credits

Inspired by [MemoryHub](https://github.com/redhat-et/memory-hub) - a Kubernetes-native agent memory component.

Built with:
- [Streamlit](https://streamlit.io/) - UI framework
- OpenAI/Anthropic - LLM providers
- Your memory system - Bring your own!

## Related Projects

- [MemoryHub](https://github.com/redhat-et/memory-hub) - Kubernetes-native memory
- [mem0](https://mem0.ai/) - Memory layer for AI agents
- [Zep](https://www.getzep.com/) - Long-term memory for LLM apps
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/) - LangChain memory modules
