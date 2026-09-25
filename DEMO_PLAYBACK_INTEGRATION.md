# Demo Playback Integration Guide

The demo playback system is ready to integrate into the app.

## What's Included

**New file:** `demo_player.py` - Demo script player with 4 built-in demos
**Documentation:** `demos/README.md` - Usage guide

## Built-in Demo Scripts

1. **Quick Wins** (5 min) - Immediate memory benefits
2. **ROI Showcase** (7 min) - Cost savings focus
3. **SRE Workflow** (6 min) - Operational efficiency
4. **Developer Onboarding** (8 min) - Learning acceleration

## Integration Steps

### 1. Update app.py Imports

Add to the top of `app.py`:

```python
from demo_player import DemoPlayer, get_available_demos
import time
```

### 2. Add Demo Mode to Radio Button

Change:
```python
mode = st.radio("Mode", ["User-Driven", "Simulated"])
```

To:
```python
mode = st.radio("Mode", ["User-Driven", "Demo Playback", "Simulated"])
```

### 3. Add Demo Playback Handler

Add this BEFORE the `if mode == "User-Driven":` block:

```python
if mode == "Demo Playback":
    # Initialize demo player
    if "demo_player" not in st.session_state:
        st.session_state.demo_player = DemoPlayer()

    # Demo script selector
    available_demos = get_available_demos()
    demo_choice = st.selectbox(
        "Choose Demo Script",
        options=list(available_demos.keys()),
        format_func=lambda x: available_demos[x]
    )

    # Load and play controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📜 Load Demo", use_container_width=True):
            script = st.session_state.demo_player.load_script(demo_choice)
            st.session_state.demo_loaded = True
            st.success(f"Loaded: {script.name} ({len(script.steps)} steps)")

    with col2:
        if st.button("▶️ Next Step", use_container_width=True, 
                     disabled=not st.session_state.get("demo_loaded")):
            step = st.session_state.demo_player.get_next_step()
            if step:
                # Show annotation
                st.info(step.annotation)
                
                # Execute step (same as user-driven mode)
                prompt = step.user_message
                # ... execute through driver ...

elif mode == "User-Driven":
    # Existing user-driven code
```

### 4. Test

```bash
streamlit run app.py
```

1. Select "Demo Playback" mode
2. Choose "quick-wins" from dropdown
3. Click "Load Demo"
4. Click "Next Step" to advance through script

## Quick Integration (Copy-Paste)

Alternatively, copy the working `app.py` from the original repo:

```bash
# Backup current
cp app.py app.py.backup

# Copy from original
cp /Users/rcarroll/Documents/code/memory-hub/demos/memory-comparison/app.py .
```

Then add the demo imports and mode.

## How It Works

### Demo Script Format

```python
DemoScript(
    name="Demo Name",
    persona="data-scientist",  # Auto-loads persona
    enable_judge=True,         # Auto-enables judge
    steps=[
        DemoStep(
            user_message="Question to ask",
            annotation="🎯 **What to notice**",
            wait_seconds=6.0,
            highlight_metrics=["highlights", "tokens"]
        ),
    ]
)
```

### Playback Flow

1. User selects demo script
2. Script configures persona + judge
3. "Next Step" sends message
4. Annotation appears explaining what to watch
5. Both agents respond
6. Progress bar shows completion

### Adding Custom Demos

Edit `demo_player.py`:

```python
DEMO_SCRIPTS = {
    # ...existing demos...
    
    "your-demo": DemoScript(
        name="Your Demo Name",
        description="What it demonstrates",
        persona="data-scientist",
        memory_backend="dict",
        enable_judge=True,
        steps=[
            DemoStep(
                user_message="Your question",
                annotation="💡 **Watch for:** key point",
                wait_seconds=7.0,
                highlight_metrics=["scores"]
            ),
            # More steps...
        ]
    ),
}
```

## Features

✅ **4 built-in demos** - Ready to use  
✅ **Annotations** - Guide audience attention  
✅ **Progress tracking** - Show completion  
✅ **Highlight metrics** - Emphasize key stats  
✅ **Persona integration** - Auto-configures  

## Future Enhancements

- [ ] Auto-play mode (hands-free)
- [ ] Custom wait times per step
- [ ] Export demo as video
- [ ] Demo recording/replay
- [ ] Branching demos

## Testing

```bash
# Test demo player imports
PYTHONPATH=. python3 -c "from demo_player import get_available_demos; print(get_available_demos())"

# Expected output:
# {
#   'quick-wins': '5-minute demo showing immediate memory benefits',
#   'roi-showcase': '7-minute demo emphasizing token savings...',
#   ...
# }
```

## Documentation

See `demos/README.md` for:
- Demo descriptions
- Usage instructions
- Custom demo creation
- Best practices
