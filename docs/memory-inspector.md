# Memory Inspector

View and inspect stored memories in dict and file backends.

## What It Does

Shows exactly what memories have been stored during the conversation:
- List of all facts
- Weights/ordering (for dict backend)
- File path (for file backend)
- Export functionality

## How to Use

### 1. Enable Inspectable Backend

Select either:
- **Dict** - In-memory storage
- **Text-file** - File-backed storage

Memory inspector NOT available for:
- None (no memory)
- MemoryHub (uses MCP server)

### 2. Open Inspector

**Sidebar → Click "🔍 Inspect Memories"**

Opens a **modal dialog window** (overlay) showing:
```
┌─────────────────────────────────────────┐
│ 🔍 Memory Inspector                  ✕ │
├─────────────────────────────────────────┤
│ Type: In-memory dict | Count: 3 facts  │
│                                         │
│ Stored Facts                            │
│ 1. [1.0] I prefer Python over R         │
│ 2. [1.0] I work with pandas             │
│ 3. [1.0] I have limited GPU budget      │
│                                         │
│ ─────────────────────────────────       │
│ [📥 Export Memories]                    │
└─────────────────────────────────────────┘
```

**Benefits of modal:**
- No scrolling on main page
- Larger viewing area
- Click outside to close
- Doesn't interfere with chat

### 3. Review Memories

**Dict backend shows:**
- Number of facts
- Each fact with weight
- Sorted by weight (highest first)

**File backend shows:**
- Number of facts
- File path location
- Each fact in order
- Optional: View raw file contents

### 4. Export

Click **"📥 Export Memories"** to download as `.txt` file.

**Export format:**
```
I prefer Python over R (weight: 1.0)
I work with pandas and scikit-learn (weight: 1.0)
I have limited GPU budget (weight: 1.0)
```

## UI Location

```
┌────────────────────────────┐
│ SIDEBAR                    │
├────────────────────────────┤
│ ⚙️ Configuration           │
│                            │
│ 👤 User Persona            │
│ [Alex Chen ▼]              │
│                            │
│ 🔄 New Session             │ ← Reset button
│ 🔍 Inspect Memories        │ ← NEW button
├────────────────────────────┤
│ 📊 Stats                   │
│ ...                        │
└────────────────────────────┘
```

## Memory Inspector Display

### Dict Backend (Modal Dialog)
```
┌─────────────────────────────────────────┐
│ 🔍 Memory Inspector                  ✕ │
├─────────────────────────────────────────┤
│ Type: In-memory dict | Count: 5 facts  │
│                                         │
│ Stored Facts                            │
│ 1. [1.0] User prefers Python over R     │
│ 2. [1.0] User works in ML Ops           │
│ 3. [1.0] User has limited GPU budget    │
│ 4. [1.0] User uses MLflow               │
│ 5. [1.0] User's team has 5 scientists   │
│                                         │
│ ─────────────────────────────────       │
│ [📥 Export Memories]                    │
└─────────────────────────────────────────┘
```

### File Backend (Modal Dialog)
```
┌─────────────────────────────────────────┐
│ 🔍 Memory Inspector                  ✕ │
├─────────────────────────────────────────┤
│ Type: File-backed | Count: 5 facts      │
│ 📁 Path: `./memory/facts.txt`          │
│                                         │
│ Stored Facts                            │
│ 1. User prefers Python over R           │
│ 2. User works in ML Ops                 │
│ 3. User has limited GPU budget          │
│ 4. User uses MLflow                     │
│ 5. User's team has 5 scientists         │
│                                         │
│ ▼ 📄 View Raw File                     │
│   [Click to expand]                     │
│                                         │
│ ─────────────────────────────────       │
│ [📥 Export Memories]                    │
└─────────────────────────────────────────┘
```

### Closing the Inspector

**3 ways to close:**
1. Click **✕** button (top right)
2. Click **outside the modal** (on dimmed background)
3. Press **Esc** key

## Use Cases

### 1. Debugging Memory Extraction

**Problem:** "Did it store my preference?"

**Solution:**
1. Say: "I prefer Python"
2. Open inspector
3. Verify: "I prefer Python" appears in list

### 2. Comparing Backends

**Test dict vs file:**
1. Run same conversation with dict backend
2. Inspect memories
3. Switch to file backend
4. Run again
5. Compare what was stored

### 3. Demo Transparency

**Show the audience:**
1. Start with empty memory
2. Build conversation
3. Open inspector periodically
4. Show memory growing in real-time
5. Point out what got stored

### 4. Export for Analysis

**Research workflow:**
1. Run 10 test conversations
2. Export memories each time
3. Compare quality across runs
4. Identify what gets consistently stored

### 5. Persona Verification

**Check pre-loaded memories:**
1. Select "Alex Chen" persona
2. Click "New Session"
3. Immediately inspect memories
4. Verify all 13 seed facts loaded

## Technical Details

### Modal Dialog

Uses Streamlit's `@st.dialog` decorator:
```python
@st.dialog("🔍 Memory Inspector", width="large")
def show_memory_inspector():
    # Inspector content
    ...

# Trigger from button
if st.button("🔍 Inspect Memories"):
    st.session_state.show_memory_inspector = True

# Show modal if triggered
if st.session_state.get("show_memory_inspector"):
    show_memory_inspector()
    st.session_state.show_memory_inspector = False
```

**Benefits:**
- Overlay window (doesn't shift page content)
- Large width for better viewing
- Auto-closes on outside click
- No scrolling issues on main page

### Detection

Inspector button only shows when:
```python
if memory_config.get("type") in ["dict", "file"]:
    # Show inspector button
```

### Dict Backend Inspection
```python
if hasattr(memory_backend, 'facts') and isinstance(memory_backend.facts, dict):
    sorted_facts = sorted(
        memory_backend.facts.items(),
        key=lambda x: x[1],  # Sort by weight
        reverse=True
    )
```

### File Backend Inspection
```python
if hasattr(memory_backend, 'facts') and isinstance(memory_backend.facts, list):
    # Show list of facts
    # Optionally read raw file
    with open(memory_backend.path) as f:
        file_contents = f.read()
```

### Export Format

**Dict backend:**
```
{fact} (weight: {weight})
```

**File backend:**
```
{fact}
```

One fact per line, plain text.

## Limitations

### Current
- Only works for dict and file backends
- MemoryHub backend not inspectable (needs MCP query)
- No editing/deleting memories from inspector
- No memory timestamps
- No source attribution (which turn added it)

### Future Enhancements
- [ ] MemoryHub inspection via MCP queries
- [ ] Edit memories inline
- [ ] Delete individual memories
- [ ] Show timestamp per memory
- [ ] Show source turn/message
- [ ] Color-code by type (preference, fact, constraint)
- [ ] Search/filter memories
- [ ] Memory usage graph over time

## Edge Cases

### No Memories Yet
```
🔍 Memory Inspector

Stored Memories
Type: In-memory dict (0 facts)

ℹ️ No memories stored yet.
   Start a conversation to build memory.
```

### Backend Type "None"
Inspector button hidden in sidebar.

Message if somehow opened:
```
⚠️ No memory backend active (using 'none' mode)
```

### File Not Created Yet
```
Type: File-backed (0 facts)
Path: ./memory/facts.txt

⚠️ File not created yet
```

## Example Workflow

### Building Memory from Scratch

**Turn 1:**
```
User: I'm a data scientist who prefers Python
Inspector shows:
1. [1.0] I'm a data scientist who prefers Python
```

**Turn 2:**
```
User: I work with pandas and scikit-learn
Inspector shows:
1. [1.0] I'm a data scientist who prefers Python
2. [1.0] I work with pandas and scikit-learn
```

**Turn 3:**
```
User: I have limited GPU budget
Inspector shows:
1. [1.0] I'm a data scientist who prefers Python
2. [1.0] I work with pandas and scikit-learn
3. [1.0] I have limited GPU budget
```

### With Pre-loaded Persona

**On session start:**
```
✨ Loaded persona: Alex Chen - Data Scientist
📚 Pre-loaded 13 memories

[🔍 Inspect Memories]

Inspector shows:
1. [1.0] User is a Senior Data Scientist named Alex Chen
2. [1.0] User works in ML Ops on Kubernetes
3. [1.0] User prefers Python over R
... (all 13 facts)
```

## Tips

### For Demos
1. Open inspector before starting
2. Show it's empty
3. Build conversation
4. Reopen inspector after each turn
5. Highlight what was added

### For Debugging
1. Reproduce issue
2. Inspect memories
3. Verify expected facts present
4. Check for unexpected/missing facts
5. Export for analysis

### For Testing
1. Run same input twice
2. Compare exported memories
3. Verify consistency
4. Check for duplicates/variations

## UI Improvements (Latest)

### Before: Inline Expander
- Opened on same page
- Required scrolling past chat
- Took up vertical space
- Could interfere with layout

### After: Modal Dialog ✓
- Opens as overlay window
- Covers chat area temporarily
- Larger viewing area
- Easy to close (click outside)
- No page scrolling needed

**User Experience:**
1. Click "🔍 Inspect Memories" in sidebar
2. Modal appears instantly (no page jump)
3. Review memories in large window
4. Click outside or press Esc to close
5. Back to conversation seamlessly
