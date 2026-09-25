# UI Layout - Judge Output Location

## Visual Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Memory Demo Harness                               │
├────────────────────┬────────────────────────────────────────────────┤
│  SIDEBAR           │              MAIN CONTENT                       │
│                    │                                                 │
│ ⚙️ Configuration   │  ┌──────────────────┬──────────────────┐      │
│                    │  │ 🧠 With Memory   │ 🤷 Without Memory│      │
│ Agent Backend      │  ├──────────────────┼──────────────────┤      │
│ [Openai Chat ▼]    │  │                  │                  │      │
│                    │  │ 👤 User:         │ 👤 User:         │      │
│ Memory Backend     │  │ How do I deploy  │ How do I deploy  │      │
│ [Dict ▼]           │  │ a model?         │ a model?         │      │
│                    │  │                  │                  │      │
│ ─────────────────  │  │ 🤖 Assistant:    │ 🤖 Assistant:    │      │
│                    │  │ Given your       │ To deploy a      │      │
│ 📊 Evaluation      │  │ Python pref...   │ model to K8s...  │      │
│                    │  │                  │                  │      │
│ ☑ Enable Judge     │  │ ⚖️ Score: 8.5/10│ ⚖️ Score: 6.0/10│  ◄── HERE
│                    │  │ [▶ Click to     │ [▶ Click to     │      │
│ ─────────────────  │  │    expand]       │    expand]       │      │
│                    │  │                  │                  │      │
│ 👤 User Persona    │  └──────────────────┴──────────────────┘      │
│ [Alex Chen ▼]      │                                                │
│                    │  ┌───────────────────────────────────┐         │
│ 🔄 New Session     │  │ Type your message here...         │         │
│                    │  └───────────────────────────────────┘         │
│ ─────────────────  │                                                │
│                    │                                                │
│ 📊 Stats           │                                                │
│ Left Turns:  2     │                                                │
│ Right Turns: 2     │                                                │
│                    │                                                │
│ Avg Scores (0-10)  │                                                │
│ With Memory:   8.5 │                                                │
│ Without:       6.0 │                                                │
│ Memory Δ:     +2.5 │                                                │
└────────────────────┴────────────────────────────────────────────────┘
```

## Judge Output - Expanded View

When you click `⚖️ Score: 8.5/10`:

```
┌────────────────────────────────────┐
│ 🤖 Assistant:                      │
│ Given your Python preference and   │
│ limited GPU budget, here's how to  │
│ deploy using MLflow...             │
│                                    │
│ ⚖️ Score: 8.5/10 [▼ Expanded]     │
│ ┌──────────────────────────────┐   │
│ │ Correctly used Python        │   │
│ │ preference and provided      │   │
│ │ pandas-specific example      │   │
│ │ matching user's known tools. │   │
│ └──────────────────────────────┘   │
└────────────────────────────────────┘
```

## When Judge is Enabled

**Flow:**
1. User types question
2. Click Send (or press Enter)
3. Spinner shows "Thinking..."
4. ~4-5 seconds later:
   - Left response appears
   - Right response appears
   - Judge scores appear below BOTH responses
   - Sidebar stats update

**Visual indicator:**
- Collapsed: `⚖️ Score: 8.5/10` (clickable)
- Expanded: Shows full justification text

## When Judge is Disabled

**Flow:**
1. User types question
2. ~2-3 seconds later:
   - Left response appears
   - Right response appears
   - No judge scores
   - No avg scores in sidebar

## Sidebar Stats

**Without judge enabled:**
```
📊 Stats
Left Turns:  2
Right Turns: 2
```

**With judge enabled:**
```
📊 Stats
Left Turns:  2
Right Turns: 2
───────────────
Avg Scores (0-10)
With Memory:   8.5
Without:       6.0
Memory Δ:     +2.5
```

## Color Coding (Future)

Planned color indicators:
- Green scores (8-10): High quality
- Yellow scores (5-7): Medium quality
- Red scores (0-4): Low quality
- Delta color: Green if positive, red if negative

## Mobile/Narrow Screens

On narrow screens, columns stack vertically:
```
┌────────────────────┐
│ 🧠 With Memory     │
│ [full conversation]│
│ ⚖️ Scores...       │
└────────────────────┘
┌────────────────────┐
│ 🤷 Without Memory  │
│ [full conversation]│
│ ⚖️ Scores...       │
└────────────────────┘
```
