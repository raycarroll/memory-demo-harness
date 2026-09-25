"""Memory Demo Harness - Side-by-side comparison UI."""

import streamlit as st
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

from dual_driver import DualDriver
from agent_backends import create_agent_backend
from memory_backends import create_memory_backend
from judge import ResponseJudge
from lib.ui_components import highlight_memory_segments
from demo_player import DemoPlayer, get_available_demos

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(
    layout="wide",
    page_title="Agent Memory Comparison",
    page_icon="🧠"
)

# Load config
@st.cache_resource
def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

config = load_config()

# Title
st.title("🧠 Agent Memory Comparison")
st.markdown("**Side-by-side:** Watch the same conversation with and without memory")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Mode selector
    mode = st.radio("Mode", ["User-Driven", "Demo Playback", "Simulated"])

    st.divider()

    # Agent selection
    st.subheader("Agent Backend")
    agent_name = st.selectbox(
        "Select Agent",
        options=list(config["agents"].keys()),
        index=0,  # Default to first (openai-chat)
        format_func=lambda x: x.replace("-", " ").title()
    )

    agent_config = config["agents"][agent_name]
    st.caption(f"Provider: {agent_config['provider']}")
    st.caption(f"Model: {agent_config['model']}")

    st.divider()

    # Memory selection
    st.subheader("Memory Backend")
    memory_name = st.selectbox(
        "Select Memory",
        options=list(config["memory"].keys()),
        format_func=lambda x: x.replace("-", " ").title()
    )

    memory_config = config["memory"][memory_name]
    if memory_config.get("type") == "none":
        st.caption("⚠️ Baseline mode - no memory on either side")
    else:
        st.caption(f"Type: {memory_config.get('type', 'N/A')}")

    st.divider()

    # Judge toggle
    st.subheader("Evaluation")
    enable_judge = st.checkbox(
        "Enable LLM-as-Judge",
        value=False,
        help="Evaluate each response for quality and memory alignment"
    )

    if enable_judge:
        st.caption("⚖️ Each turn will be evaluated for memory alignment")

    st.divider()

    # Persona selection
    st.subheader("User Persona")
    persona_name = st.selectbox(
        "Pre-populate with",
        options=list(config["personas"].keys()),
        index=0,
        format_func=lambda x: config["personas"][x]["name"]
    )

    persona_config = config["personas"][persona_name]
    st.caption(persona_config["description"])

    if persona_config.get("seed_file"):
        st.caption(f"📄 {persona_config['seed_file']}")

    st.divider()

    # New Session button (changed from Reset)
    if st.button("🔄 New Session", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()

    # Memory Inspector button (for dict/file backends)
    if memory_config.get("type") in ["dict", "file"]:
        if st.button("🔍 Inspect Memories", use_container_width=True):
            st.session_state.show_memory_inspector = True

    st.divider()

    # Stats
    if "driver" in st.session_state and st.session_state.driver is not None:
        stats = st.session_state.driver.get_stats()
        st.subheader("📊 Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Left Turns", stats.get("left_turns", 0))
        with col2:
            st.metric("Right Turns", stats.get("right_turns", 0))

        # Token stats if available
        if stats.get("left_tokens_total"):
            st.divider()
            st.caption("Token Usage")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("With Memory", f"{stats.get('left_tokens_total', 0):,}")
            with col2:
                right_total = stats.get('right_tokens_total', 0)
                delta = stats.get('token_delta', 0)
                st.metric(
                    "Without Memory",
                    f"{right_total:,}",
                    delta=f"{delta:,}" if delta != 0 else None,
                    delta_color="inverse"  # Lower is better for tokens
                )

            efficiency = stats.get('token_efficiency', 0)
            if efficiency != 0:
                if efficiency > 0:
                    st.success(f"💰 {efficiency}% token savings with memory")
                else:
                    st.info(f"ℹ️ {abs(efficiency)}% more tokens with memory context")

        # Judge stats if enabled
        if enable_judge and stats.get("total_evaluations", 0) > 0:
            st.divider()
            st.caption("Average Scores (0-10)")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("With Memory", stats.get("avg_left_score", "N/A"))
            with col2:
                st.metric("Without Memory", stats.get("avg_right_score", "N/A"))
            with col3:
                delta = stats.get("avg_memory_delta", 0)
                st.metric("Memory Δ", f"+{delta}" if delta > 0 else str(delta))

# Initialize driver
def init_driver():
    """Initialize the dual driver with selected backends."""
    try:
        # Create agent backend
        agent = create_agent_backend(agent_config)

        # Get seed file from selected persona
        seed_file = persona_config.get("seed_file")

        # Create memory backend (if not 'none')
        memory = None
        if memory_config.get("type") != "none":
            # For text-file backend, use the agent as extractor
            memory = create_memory_backend(
                memory_config,
                extractor_backend=agent,
                seed_file=seed_file
            )

        # Create judge if enabled
        judge = None
        if enable_judge:
            # Use the same agent backend for judging (could be configurable)
            judge = ResponseJudge(agent)

        return DualDriver(agent, memory, judge)
    except ValueError as e:
        error_msg = str(e)
        st.error(f"❌ {error_msg}")

        if "API_KEY" in error_msg:
            st.info("💡 **To fix:** Add your API key to the `.env` file:")
            if "OPENAI" in error_msg:
                st.code("OPENAI_API_KEY=sk-...", language="bash")
            elif "ANTHROPIC" in error_msg:
                st.code("ANTHROPIC_API_KEY=sk-ant-...", language="bash")
            st.caption("Then refresh this page (Ctrl+R / Cmd+R)")

        return None
    except Exception as e:
        st.error(f"❌ Failed to initialize driver: {e}")
        return None

if "driver" not in st.session_state or st.session_state.driver is None:
    st.session_state.driver = init_driver()
    st.session_state.left_messages = []
    st.session_state.right_messages = []
    st.session_state.current_persona = persona_name

# Main UI: Side-by-side chat columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧠 With Memory")
    if persona_config.get("seed_file"):
        st.caption(f"Persona: {persona_config['name']} | Memory: {memory_name}")
    else:
        st.caption(f"Memory: {memory_name}")

    # Render chat history
    chat_container = st.container(height=500)
    with chat_container:
        if not st.session_state.left_messages:
            st.info("👋 Start a conversation to see memory in action!")
        else:
            # Track segments for highlighting
            current_segments = []

            for i, msg in enumerate(st.session_state.left_messages):
                if msg["role"] == "judge":
                    # Render judge verdict
                    segments_info = ""
                    if msg.get("segments"):
                        segments_info = f" • {len(msg['segments'])} highlighted"
                        current_segments = msg["segments"]

                    with st.expander(f"⚖️ Score: {msg['score']}/10{segments_info}", expanded=False):
                        st.caption(msg["justification"])

                        if msg.get("segments"):
                            st.caption("**Memory-influenced segments:**")
                            for seg in msg["segments"]:
                                st.caption(f"• \"{seg}\"")
                else:
                    with st.chat_message(msg["role"]):
                        # Check if next message is a judge with segments
                        next_segments = []
                        if i + 1 < len(st.session_state.left_messages):
                            next_msg = st.session_state.left_messages[i + 1]
                            if next_msg.get("role") == "judge" and next_msg.get("segments"):
                                next_segments = next_msg["segments"]

                        # Render with highlighting if this is an assistant message followed by judge
                        if msg["role"] == "assistant" and next_segments:
                            highlighted = highlight_memory_segments(msg["content"], next_segments)
                            st.markdown(highlighted, unsafe_allow_html=True)
                        else:
                            st.markdown(msg["content"])

                        # Show token usage for assistant messages
                        if msg["role"] == "assistant" and msg.get("tokens_in") is not None:
                            tokens_total = msg["tokens_in"] + msg["tokens_out"]
                            st.caption(f"🔢 {tokens_total:,} tokens ({msg['tokens_in']:,} in + {msg['tokens_out']:,} out)")

with col2:
    st.markdown("### 🤷 Without Memory")
    st.caption("Baseline (no context)")

    # Render chat history
    chat_container = st.container(height=500)
    with chat_container:
        if not st.session_state.right_messages:
            st.info("👋 Same input, different context!")
        else:
            for msg in st.session_state.right_messages:
                if msg["role"] == "judge":
                    # Render judge verdict
                    with st.expander(f"⚖️ Score: {msg['score']}/10", expanded=False):
                        st.caption(msg["justification"])
                else:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

                        # Show token usage for assistant messages
                        if msg["role"] == "assistant" and msg.get("tokens_in") is not None:
                            tokens_total = msg["tokens_in"] + msg["tokens_out"]
                            st.caption(f"🔢 {tokens_total:,} tokens ({msg['tokens_in']:,} in + {msg['tokens_out']:,} out)")

# Helper function to execute a prompt (used by both demo and manual input)
def execute_prompt(prompt: str, from_demo: bool = False):
    """Execute a prompt through the dual driver."""
    # Add user message to display
    st.session_state.left_messages.append({"role": "user", "content": prompt})
    st.session_state.right_messages.append({"role": "user", "content": prompt})

    # Execute through dual driver
    with st.spinner("Thinking..."):
        try:
            left_resp, right_resp, verdict = st.session_state.driver.execute(prompt)

            # Add assistant responses with token counts
            st.session_state.left_messages.append({
                "role": "assistant",
                "content": left_resp.content,
                "tokens_in": left_resp.tokens_in,
                "tokens_out": left_resp.tokens_out
            })
            st.session_state.right_messages.append({
                "role": "assistant",
                "content": right_resp.content,
                "tokens_in": right_resp.tokens_in,
                "tokens_out": right_resp.tokens_out
            })

            # Add judge verdict if available
            if verdict:
                st.session_state.left_messages.append({
                    "role": "judge",
                    "score": verdict.left_score,
                    "justification": verdict.left_justification,
                    "segments": verdict.memory_influenced_segments
                })
                st.session_state.right_messages.append({
                    "role": "judge",
                    "score": verdict.right_score,
                    "justification": verdict.right_justification
                })

            # Clear pending demo step if this was from demo
            if from_demo and "demo_step_to_execute" in st.session_state:
                st.session_state.demo_step_to_execute = None

            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")
            # Remove the user messages we added
            st.session_state.left_messages.pop()
            st.session_state.right_messages.pop()
            if from_demo and "demo_step_to_execute" in st.session_state:
                st.session_state.demo_step_to_execute = None
            st.rerun()

# Input area (below columns)
st.divider()

# Demo controls (shown only in Demo Playback mode)
if mode == "Demo Playback":
    # Initialize demo player
    if "demo_player" not in st.session_state:
        st.session_state.demo_player = DemoPlayer()
        st.session_state.demo_loaded = False
        st.session_state.demo_active = False

    # Demo controls
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        # Demo script selector
        available_demos = get_available_demos()
        demo_choice = st.selectbox(
            "Choose Demo Script",
            options=list(available_demos.keys()),
            format_func=lambda x: available_demos[x].split(" - ")[0]  # Just the name
        )

        # Show full description
        st.caption(available_demos[demo_choice])

    with col2:
        # Load button
        if st.button("📜 Load Demo", use_container_width=True, type="primary"):
            script = st.session_state.demo_player.load_script(demo_choice)
            st.session_state.demo_loaded = True
            st.session_state.demo_active = True

            # Configure UI based on demo script
            # Note: These would ideally update the sidebar selectors, but that requires a rerun
            st.success(f"✅ Loaded: {script.name}")
            st.info(f"📊 {len(script.steps)} steps | ~{int(script.total_duration() / 60)} min")

    with col3:
        # Next step button
        if st.button(
            "▶️ Next Step",
            use_container_width=True,
            disabled=not st.session_state.get("demo_loaded", False)
        ):
            step = st.session_state.demo_player.get_next_step()
            if step:
                # Store the step to execute
                st.session_state.demo_step_to_execute = step
            else:
                st.info("✅ Demo complete!")
                st.session_state.demo_active = False

    # Show progress
    if st.session_state.get("demo_loaded", False):
        progress = st.session_state.demo_player.get_progress()
        st.progress(
            progress["percent"] / 100,
            text=f"Step {progress['step']}/{progress['total']}"
        )

        # Execute pending demo step
        if st.session_state.get("demo_step_to_execute"):
            step = st.session_state.demo_step_to_execute

            # Show annotation
            st.info(f"**{step.annotation}**")

            # Show suggested metrics to highlight
            if step.highlight_metrics:
                st.caption(f"👁️ Watch: {', '.join(step.highlight_metrics)}")

            # Execute the demo step
            execute_prompt(step.user_message, from_demo=True)

    st.divider()

# Chat input (always visible in all modes)
if mode == "Simulated":
    st.info("🤖 Simulated mode coming soon - use 'User-Driven' or 'Demo Playback' for now")
    prompt = None  # Disable input in simulated mode for now
else:
    # Show chat input for both User-Driven and Demo Playback modes
    input_placeholder = "Type your message here..." if mode == "User-Driven" else "Type to send manual message (or use Next Step above)..."
    prompt = st.chat_input(input_placeholder)

# Handle manual input (works in both User-Driven and Demo Playback modes)
if prompt:
    execute_prompt(prompt, from_demo=False)

# Memory Inspector Dialog
@st.dialog("🔍 Memory Inspector", width="large")
def show_memory_inspector():
    """Display memory inspector in a modal dialog."""

    if st.session_state.driver and st.session_state.driver.memory:
        memory_backend = st.session_state.driver.memory

        # Dict backend
        if hasattr(memory_backend, 'facts') and isinstance(memory_backend.facts, dict):
            if memory_backend.facts:
                st.info(f"**Type:** In-memory dict | **Count:** {len(memory_backend.facts)} facts")

                # Sort by weight
                sorted_facts = sorted(
                    memory_backend.facts.items(),
                    key=lambda x: x[1],
                    reverse=True
                )

                st.subheader("Stored Facts")
                for i, (fact, weight) in enumerate(sorted_facts, 1):
                    st.text(f"{i}. [{weight:.1f}] {fact}")
            else:
                st.info("No memories stored yet. Start a conversation to build memory.")

        # File backend
        elif hasattr(memory_backend, 'facts') and isinstance(memory_backend.facts, list):
            if memory_backend.facts:
                st.info(f"**Type:** File-backed | **Count:** {len(memory_backend.facts)} facts")
                st.caption(f"📁 Path: `{memory_backend.path}`")

                st.subheader("Stored Facts")
                for i, fact in enumerate(memory_backend.facts, 1):
                    st.text(f"{i}. {fact}")

                # Show file contents
                with st.expander("📄 View Raw File"):
                    try:
                        with open(memory_backend.path) as f:
                            file_contents = f.read()
                        st.code(file_contents, language="text")
                    except FileNotFoundError:
                        st.warning("File not created yet")
            else:
                st.info("No memories stored yet. Start a conversation to build memory.")
        else:
            st.warning("Memory backend type not inspectable")
    else:
        st.warning("No memory backend active (using 'none' mode)")

    # Export button
    if st.session_state.driver and st.session_state.driver.memory:
        memory_backend = st.session_state.driver.memory

        if hasattr(memory_backend, 'facts'):
            st.divider()

            # Prepare export content
            if isinstance(memory_backend.facts, dict):
                export_lines = [f"{fact} (weight: {weight})" for fact, weight in memory_backend.facts.items()]
            else:
                export_lines = memory_backend.facts

            export_content = "\n".join(export_lines)

            if export_content:
                st.download_button(
                    "📥 Export Memories",
                    data=export_content,
                    file_name="memories_export.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# Show inspector if triggered
if st.session_state.get("show_memory_inspector", False):
    show_memory_inspector()
    st.session_state.show_memory_inspector = False  # Reset after showing

# Footer
st.divider()
st.caption("Memory Demo Harness | MemoryHub Project")
