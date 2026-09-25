# Family Helper Demo Script

**Duration:** 6 minutes  
**Persona:** Busy Parent (Jamie)  
**Best for:** Non-technical audiences, general public, families

## Script

### Step 1: Setup (7 sec)
**User:** "I need dinner ideas for tonight that my kids will actually eat"

**Annotation:** 🏠 **Setup:** Agent learns about family (kids' ages, allergies, food preferences)

**What happens:**
- Left: Stores family details (2 kids, peanut allergy, no spicy food)
- Right: Gives generic suggestions without context
- Memory inspector shows 3-4 new facts

### Step 2: Context Recall (7 sec)
**User:** "What ingredients do I need for that?"

**Annotation:** 💡 **Watch:** Left remembers the recipe, Right asks "for what?"

**What to point out:**
- Yellow highlights on recipe name or ingredients
- Left provides ingredient list immediately
- Right needs clarification: "Which recipe?"
- Token count difference starting to show

### Step 3: Different Topic (8 sec)
**User:** "Can you suggest activities for this Saturday?"

**Annotation:** ⚡ **Context-aware:** Left knows about soccer schedule and dog, Right gives generic ideas

**What to point out:**
- Left suggests activities considering:
  - Soccer game on Saturday
  - Golden retriever Max
  - Kids' ages (7 and 10)
- Right gives generic "take kids to park" suggestions
- Judge scores show relevance difference

### Step 4: Shopping Help (7 sec)
**User:** "Where should I shop for those supplies?"

**Annotation:** 🎯 **Personalized:** Left suggests Target, Right asks location/budget

**What to point out:**
- Left: "Target has those..." (remembers preference)
- Right: "What's your budget? Where do you live?"
- Fewer back-and-forth questions on left
- Cumulative tokens: ~2,000 left vs ~3,200 right

### Step 5: Final Comparison (7 sec)
**User:** "Any tips for keeping it affordable?"

**Annotation:** 📊 **Final:** Check cumulative savings - fewer clarifying questions

**What to point out:**
- Sidebar stats:
  - Token savings: 30-40%
  - Quality delta: +2 points
  - Efficiency across different topics
- Total: ~2,600 vs ~4,100 tokens

## Key Talking Points

### After Step 1
"Notice how the left agent is learning about the family - kids' ages, allergies, preferences. This information will help with future questions."

### After Step 2
"The left side remembered which recipe we were discussing. The right side has to ask 'for what?' - wasting time and tokens."

### After Step 3
"Even switching topics, the left agent knows it's Saturday with soccer practice. The right agent gives generic weekend suggestions that might not even work with the schedule."

### After Step 4
"See how personalized this is? It knows the family shops at Target, stays on budget, has specific needs. No repetitive questions."

### After Step 5
"Over 5 questions spanning different topics - meals, activities, shopping - the memory-enabled agent saved 35% of the back-and-forth. That's real efficiency in everyday life."

## Metrics Summary

**Expected results:**
- Token savings: 30-40%
- Quality improvement: +2 points
- Topics covered: 3 different areas seamlessly
- Highlights: 4-6 segments per response

## Real-World Value

### For Busy Parents
- No repeating yourself
- Answers fit your actual situation
- Saves time (fewer clarifications)
- Feels like talking to someone who knows you

### For Non-Technical Users
- Shows AI isn't just for programmers
- Relatable everyday scenarios
- Clear before/after comparison
- Easy to understand value

## Audience Q&A Prep

**Q: "Will it remember everything I tell it?"**
A: It remembers useful context like preferences and constraints. You can view and delete memories anytime.

**Q: "What if my situation changes?"**
A: Just tell it! "My son's allergy has resolved" updates the memory.

**Q: "Is this just ChatGPT?"**
A: Any AI assistant can use memory - this shows the difference it makes. The technology works with ChatGPT, Claude, or other systems.

**Q: "Does it share my data?"**
A: No - memories stay in your private storage. It's like notes only you can see.

**Q: "How much does memory cost?"**
A: Actually saves money - fewer wasted tokens on repeated questions. Net savings around 30-40%.

## Tips for Presenting

### Language
- Avoid technical jargon
- Say "agent" or "assistant" not "LLM"
- Say "remembers" not "stores embeddings"
- Use everyday examples

### Pacing
- Let responses fully render
- Read annotations clearly
- Point at specific highlighted text
- Pause between topics

### Emphasis
- **Step 1:** "Watch it learn"
- **Step 2:** "See it remember"
- **Step 3:** "Different topic, still knows context"
- **Step 4:** "Personalized to their life"
- **Step 5:** "Look at the efficiency"

### Making it Relatable
"Imagine asking a neighbor for advice. The first time, they don't know you - lots of questions. But after living next door for a year, they know your kids, your schedule, your preferences. That's what memory does for AI."

## Variations

### For Different Audiences

**Parents/Families:**
Keep as-is - highly relatable

**Retirees:**
Change persona to focus on health management, hobbies, travel planning

**Students:**
Change to study schedules, course preferences, assignment deadlines

**Small Business Owners:**
Change to vendor preferences, customer patterns, inventory needs

## Common Misconceptions to Address

**"AI is only for tech people"**
→ This demo shows everyday use cases anyone can benefit from

**"It's too complicated to set up"**
→ It's just having a conversation - the system handles memory automatically

**"I don't want AI tracking me"**
→ You control what it remembers, can view/delete anytime, data stays private

**"It's expensive"**
→ Actually saves time and money by reducing repetitive conversations

## Demo Success Indicators

✅ Audience relates to scenarios  
✅ Clear "aha" moment at step 2  
✅ Questions about using it themselves  
✅ Understand value without technical details  
✅ Can explain benefit to others  

## Follow-Up

After the demo, show:
1. Memory inspector - let them see what's stored
2. Manual mode - take their questions live
3. Different personas - show versatility
4. Simple setup - "just talk to it"

This builds confidence that it's accessible and practical for everyday use.
