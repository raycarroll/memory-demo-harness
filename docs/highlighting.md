# Memory-Influenced Highlighting

Visual highlighting of response segments that were influenced by user memories.

## What It Does

When judge is enabled, specific parts of the **left panel response** (with memory) are highlighted in yellow to show exactly which phrases used the user's context.

## Visual Example

**Without highlighting:**
```
Here's how to read a CSV with pandas:
import pandas as pd
```

**With highlighting:**
```
Here's how to read a CSV with pandas:
                          ^^^^^^^^^^^
                          (highlighted yellow)
import pandas as pd
       ^^^^^^^^^^^^^^^^
       (highlighted yellow)
```

In Streamlit, highlighted segments appear with a yellow background:
- Background color: `#FFEB3B` (Material Design Yellow 500)
- Padding for readability
- Rounded corners

## How It Works

### 1. Judge Extracts Segments

The judge LLM identifies specific quotes from the response that used memory:

```
MEMORY_INFLUENCED_SEGMENTS: [
  "with pandas",
  "pd.read_csv",
  "you prefer Python"
]
```

### 2. UI Applies Highlighting

The UI uses regex to find and wrap these segments in `<mark>` tags:

```python
highlighted = highlight_memory_segments(response, segments)
# Output: "...CSV <mark>with pandas</mark>..."
```

### 3. Streamlit Renders HTML

Streamlit's `unsafe_allow_html=True` renders the `<mark>` tags with inline styles.

## Example Interaction

**User:** "How do I read a CSV?"

**Memories:**
- User prefers Python over R
- User uses pandas for data analysis

**Response (highlighted):**
```
Since you prefer Python, here's how with pandas:
      ^^^^^^^^^^^^^^^^^^            ^^^^^^^^^^^
                  (memory-influenced)

import pandas as pd
df = pd.read_csv('file.csv')
     ^^^^^^^^^^^
```

**Judge verdict:**
- Score: 8.5/10
- Segments: 3 highlighted
- Justification: "Used Python preference and pandas tool knowledge"

## UI Display

### In Chat

```
┌────────────────────────────────┐
│ 🤖 Assistant:                  │
│ Since you prefer Python,       │  ← Yellow highlight
│       ^^^^^^^^^^^^^^^^^^        │
│ here's how with pandas:        │  ← Yellow highlight
│            ^^^^^^^^^^^          │
│ ...                            │
└────────────────────────────────┘
```

### In Judge Expander

```
⚖️ Score: 8.5/10 • 3 highlighted

When expanded:
  Correctly used Python preference and
  pandas tool knowledge.

  Memory-influenced segments:
  • "you prefer Python"
  • "with pandas"
  • "pd.read_csv"
```

## Implementation

### Judge Prompt Extension

Added to evaluation criteria:

```
**For MEMORY_INFLUENCED_SEGMENTS:**
- Extract short quotes (5-15 words) from Response A that
  directly used the user's memories
- Include phrases that reference preferences, known tools,
  constraints, or context
- Use exact quotes from the response
- Return as a JSON array of strings
```

### Highlighting Function

```python
def highlight_memory_segments(text: str, segments: list[str]) -> str:
    """Highlight segments with yellow background."""
    for segment in segments:
        pattern = re.compile(f"({re.escape(segment)})", re.IGNORECASE)
        text = pattern.sub(
            r'<mark style="background-color: #FFEB3B;">\\1</mark>',
            text
        )
    return text
```

### Rendering

```python
if msg["role"] == "assistant" and has_segments:
    highlighted = highlight_memory_segments(msg["content"], segments)
    st.markdown(highlighted, unsafe_allow_html=True)
else:
    st.markdown(msg["content"])
```

## Benefits

### 1. Visual Proof
- Instantly see which parts used memory
- No need to guess or compare line-by-line

### 2. Transparency
- Shows judge's reasoning
- Makes evaluation explainable

### 3. Debugging
- Verify memory extraction worked
- Check if relevant context was used

### 4. Demo Impact
- More convincing than text explanation
- Visual differentiation is immediate

## Edge Cases

### Partial Matches
- Highlights exact quotes only
- Case-insensitive matching
- Longest segments matched first (avoids partial overlaps)

### Code Blocks
- Highlighting works inside markdown code blocks
- Preserves syntax highlighting
- `<mark>` wraps around code spans

### No Segments
- If judge returns empty list `[]`
- Response renders normally (no highlighting)
- Still shows score and justification

### Multiple Occurrences
- Same segment may appear multiple times
- All occurrences highlighted
- Example: "Python" appears 3 times → all 3 highlighted

## Limitations

### Current
- Only highlights left panel (with memory)
- Right panel shows no highlights (baseline has no context)
- Segments must be exact quotes (no paraphrasing detection)

### Future Enhancements
- [ ] Color-code by memory type (preference vs fact vs constraint)
- [ ] Hover tooltip showing which specific memory was used
- [ ] Toggle highlights on/off
- [ ] Export highlighted responses to markdown
- [ ] Fuzzy matching for paraphrased segments

## Configuration

**Enable/Disable:**
- Highlighting is automatic when judge is enabled
- No separate toggle (coupled with judge)
- If judge disabled, no highlighting

**Customize Colors:**
Edit `lib/ui_components.py`:
```python
# Change yellow to another color
background-color: #FFEB3B  # Current yellow
background-color: #4CAF50  # Green alternative
background-color: #2196F3  # Blue alternative
```

## Testing

Run tests:
```bash
# Test highlighting function
python3 test_highlighting.py

# Test judge with segments
python3 test_judge.py
```

## Examples by Persona

### Data Scientist (Alex)
**Query:** "How do I deploy a model?"

**Highlighted segments:**
- "with limited GPU budget"
- "using MLflow"
- "pandas and scikit-learn"

### SRE (Jordan)
**Query:** "How do I debug a pod?"

**Highlighted segments:**
- "kubectl commands"
- "command-line approach"
- "without using the UI"

### Developer (Sam)
**Query:** "Build an API endpoint"

**Highlighted segments:**
- "with FastAPI"
- "using TypeScript types"
- "React frontend"

## Accessibility

**Considerations:**
- Yellow background (`#FFEB3B`) has good contrast with black text
- Screen readers still read text normally
- Highlighting is visual enhancement only
- Core information available in judge justification text

**WCAG Compliance:**
- Contrast ratio: >7:1 (AAA level)
- Does not rely solely on color (also listed in expander)
- Keyboard accessible (expander is keyboard-navigable)
