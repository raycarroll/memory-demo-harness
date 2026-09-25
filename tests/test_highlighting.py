#!/usr/bin/env python3
"""Test highlighting functionality."""

from lib.ui_components import highlight_memory_segments

def test_highlighting():
    """Test segment highlighting."""
    print("Testing highlight_memory_segments...")

    # Test text
    text = """Here's how to read a CSV with pandas:

```python
import pandas as pd
df = pd.read_csv('file.csv')
```

Since you prefer Python, this is the recommended approach."""

    # Segments to highlight
    segments = [
        "with pandas",
        "pd.read_csv",
        "you prefer Python"
    ]

    # Apply highlighting
    highlighted = highlight_memory_segments(text, segments)

    # Verify highlights were applied
    assert '<mark' in highlighted, "No highlighting applied"
    assert 'with pandas' in highlighted
    assert 'pd.read_csv' in highlighted
    assert 'you prefer Python' in highlighted

    print("✓ Highlighting working")
    print("\nOriginal:")
    print(text[:100] + "...")
    print("\nHighlighted segments:")
    for seg in segments:
        print(f"  • \"{seg}\"")
    print("\nHighlighted text preview:")
    print(highlighted[:200] + "...")

def test_no_segments():
    """Test with no segments."""
    text = "Just a normal response"
    result = highlight_memory_segments(text, [])
    assert result == text, "Text should be unchanged"
    print("✓ No-segments case working")

def test_overlapping_segments():
    """Test with overlapping segments."""
    text = "Use pandas to read CSV files with pd.read_csv"
    segments = ["pandas", "pd.read_csv"]

    highlighted = highlight_memory_segments(text, segments)
    assert '<mark' in highlighted
    print("✓ Overlapping segments working")

if __name__ == "__main__":
    test_highlighting()
    test_no_segments()
    test_overlapping_segments()
    print("\n🎉 All highlighting tests passed!")
