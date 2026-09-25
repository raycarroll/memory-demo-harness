"""Reusable UI components for memory demo."""

import re

def highlight_memory_segments(text: str, segments: list[str]) -> str:
    """
    Highlight segments in text that were influenced by memory.

    Args:
        text: The full response text
        segments: List of text segments to highlight

    Returns:
        Text with HTML highlighting applied
    """
    if not segments:
        return text

    highlighted_text = text

    # Sort segments by length (longest first) to avoid partial matches
    segments_sorted = sorted(segments, key=len, reverse=True)

    for segment in segments_sorted:
        # Escape the segment for regex
        segment_escaped = re.escape(segment.strip())

        # Case-insensitive replacement with highlighting
        pattern = re.compile(f"({segment_escaped})", re.IGNORECASE)
        highlighted_text = pattern.sub(
            r'<mark style="background-color: #FFEB3B; padding: 2px 4px; border-radius: 3px;">\1</mark>',
            highlighted_text
        )

    return highlighted_text

def render_response_with_highlights(content: str, segments: list[str] = None):
    """
    Render response content with optional memory highlights.

    Args:
        content: Response text to display
        segments: Optional list of segments to highlight

    Returns:
        Rendered markdown (via st.markdown)
    """
    import streamlit as st

    if segments:
        highlighted = highlight_memory_segments(content, segments)
        st.markdown(highlighted, unsafe_allow_html=True)
    else:
        st.markdown(content)
