# Scroll Fix

## Problem

Scrolling in chat containers would jump back to bottom, making it impossible to review earlier messages.

## Root Cause

The code called `st.rerun()` after every message, which:
1. Refreshes the entire Streamlit app
2. Resets scroll position to default (usually bottom)
3. Prevents user from staying scrolled up

## Solution

**Removed unnecessary `st.rerun()`** after successful message submission.

### Why This Works

Streamlit automatically reruns when widgets interact:
- `st.chat_input()` triggers a rerun when user submits
- Session state changes persist across reruns
- No manual rerun needed

### Code Change

**Before:**
```python
if prompt:
    # Add messages to session state
    st.session_state.left_messages.append(...)
    st.session_state.right_messages.append(...)
    
    # Execute driver
    left_resp, right_resp, verdict = driver.execute(prompt)
    
    # Add responses
    st.session_state.left_messages.append(...)
    
    st.rerun()  # ❌ This caused scroll jump
```

**After:**
```python
if prompt:
    # Add messages to session state
    st.session_state.left_messages.append(...)
    st.session_state.right_messages.append(...)
    
    # Execute driver
    left_resp, right_resp, verdict = driver.execute(prompt)
    
    # Add responses
    st.session_state.left_messages.append(...)
    
    # ✓ No rerun - Streamlit handles it automatically
```

### When We DO Rerun

Only on error cleanup:
```python
except Exception as e:
    st.error(f"Error: {e}")
    # Remove failed messages
    st.session_state.left_messages.pop()
    st.session_state.right_messages.pop()
    st.rerun()  # ✓ Clear error state
```

## Behavior Now

### Sending Messages
1. User types and submits
2. Spinner shows "Thinking..."
3. Responses appear
4. **Scroll stays where user left it**
5. New messages appear at bottom
6. User can scroll up to review anytime

### Scrolling
- Chat containers maintain scroll position
- Can scroll up to review conversation
- New messages don't force scroll down
- Scroll to bottom to see latest

## Alternative Approaches Considered

### 1. Scroll Anchoring
```python
# Could add JavaScript to maintain position
st.markdown("""
<script>
    // Save scroll position before rerun
    window.addEventListener('beforeunload', () => {
        sessionStorage.setItem('scrollPos', window.scrollY);
    });
</script>
""", unsafe_allow_html=True)
```
**Rejected:** Too complex, fragile across browsers

### 2. Streamlit Components
```python
# Custom component with scroll control
from streamlit_chat import scrollable_chat
```
**Rejected:** Adds dependency, not needed

### 3. Session State Tracking
```python
# Track scroll position in session state
st.session_state.scroll_position = ...
```
**Rejected:** Streamlit doesn't expose scroll position

## Testing

**Test scrolling:**
1. Start conversation
2. Send 5+ messages (enough to scroll)
3. Scroll up to first message
4. Send a new message
5. **Verify:** Scroll stays at first message (doesn't jump)
6. **Verify:** New message appears at bottom
7. Scroll down to see new message

**Expected:**
- Scroll position preserved ✓
- New messages visible at bottom ✓
- No jumping or stuttering ✓

## Related Issues

### st.rerun() Use Cases

**When TO use st.rerun():**
- ✓ After config changes (persona selection)
- ✓ On "New Session" button click
- ✓ After errors to reset state
- ✓ When manually updating session state outside widget callbacks

**When NOT to use st.rerun():**
- ❌ After widget interactions (auto-handled)
- ❌ After chat message submission
- ❌ After form submission
- ❌ In normal message flow

### Streamlit Auto-Rerun Triggers

Streamlit automatically reruns when:
- User clicks a button
- User submits a form
- User types in chat_input and presses Enter
- User changes a selectbox/radio/checkbox
- Session state is modified in a callback

No manual `st.rerun()` needed for these!

## Documentation

See Streamlit docs:
- [Session State](https://docs.streamlit.io/library/api-reference/session-state)
- [Chat Elements](https://docs.streamlit.io/library/api-reference/chat)
- [Execution Model](https://docs.streamlit.io/library/advanced-features/execution-model)
