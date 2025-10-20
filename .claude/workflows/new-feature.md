# New Feature Workflow - Feature Planning Wizard

You are the **Feature Planning Orchestrator** for Life OS.

Guide the user through comprehensive feature planning before implementation.

---

## Step 1: Feature Discovery

### 1.1 Understand the Feature

Ask user detailed questions:

```
🎯 Feature Planning Wizard

Let's plan your new feature together.

Question 1: What feature are you planning to build?
(Describe in 1-2 sentences)
```

Wait for response, then:

```
Question 2: What phase does this belong to?
  1. Phase 2B - Calendar Integration
  2. Phase 2C - Calendar + RAG
  3. Phase 3B - Intelligent Import (Images/PDFs)
  4. Phase 3C - Web Link Import
  5. Phase 4 - Advanced Features
  6. Other / New phase

Your choice:
```

```
Question 3: Why is this feature important?
(User value, business goal, or technical benefit)
```

```
Question 4: What's the expected user experience?
(Walk through how a user would interact with this feature)
```

### 1.2 Research Best Practices

Based on feature description:

**Use web search** to find:
- Industry best practices
- Similar implementations
- Common pit falls
- Recommended libraries/tools

**Report:**
```
📚 Research Findings

Best Practices:
  • [Practice 1]
  • [Practice 2]

Recommended Tools:
  • [Tool/Library 1]: [Why]
  • [Tool/Library 2]: [Why]

Reference Implementations:
  • [Link or example]

Warnings:
  • [Common pitfall 1]
  • [Common pitfall 2]
```

### 1.3 Review Existing Code

**Search codebase** for related patterns:

```bash
grep -r "[relevant keywords]" scripts/
```

**Check:**
- Similar features already implemented
- Code patterns to follow
- Integration points

**Report:**
```
🔍 Codebase Analysis

Related Code:
  • scripts/router.py - Agentic routing pattern
  • scripts/vector_store.py - RAG implementation

Integration Points:
  • [File/function] - Where this feature plugs in

Code Patterns to Follow:
  • [Pattern 1]: [Example location]
  • [Pattern 2]: [Example location]
```

---

## Step 2: Architecture Design

### 2.1 Propose High-Level Architecture

Based on feature requirements:

**Create architecture diagram:**
```
═══════════════════════════════════════════════
Proposed Architecture
═══════════════════════════════════════════════

Current System:
  [Relevant existing components]

New Components:
  [Component 1]
     ↓
  [Component 2]
     ↓
  [Integration point]

Data Flow:
  User Input → [Step 1] → [Step 2] → [Output]

═══════════════════════════════════════════════
```

Ask: **"Does this architecture make sense? (yes/no/modify)"**

### 2.2 Identify Files to Change/Create

**Files to Modify:**
```
M scripts/router.py
   - Add new tool: [tool_name]
   - Update routing logic

M scripts/telegram_bot.py
   - Add handler for [new input type]

M requirements.txt
   - Add: [dependency 1]
   - Add: [dependency 2]
```

**New Files:**
```
N scripts/[new_file].py
   - Purpose: [description]
   - Main functions: [list]

N tests/test_[new_file].py
   - Test coverage for new feature
```

**Documentation:**
```
M .agent/decisions/phase-[X]-roadmap.md
   - Mark feature as "In Progress"

N .agent/decisions/[feature-name]-implementation.md
   - Detailed implementation plan
```

### 2.3 Database Changes

**Check if database changes needed:**

If yes:
```
Database Schema Changes:

ALTER TABLE [table]:
  - Add column: [column_name] [type]

CREATE TABLE [new_table]:
  - [schema]

Migration Script:
  - Create: scripts/migrate_[feature].py
  - Rollback plan: [describe]
```

If no:
```
✅ No database changes required
```

### 2.4 External Dependencies

**Identify external dependencies:**

**APIs:**
- [API name]: [Purpose]
  - Authentication: [Method]
  - Rate limits: [Details]
  - Cost: [If applicable]

**MCPs:**
- [MCP name]: [Why needed]
  - Already configured: [Yes/No]
  - Setup required: [If no]

**Python Packages:**
- [Package]: [Version] - [Purpose]
- [Package]: [Version] - [Purpose]

**Other:**
- [Any other dependencies]

---

## Step 3: Create Implementation Plan

### 3.1 Break Into Steps

**Divide feature into manageable steps (30-60 min each):**

```
Implementation Steps:

Step 1: [Step name] (Est: 30 min)
  - Task 1.1: [Description]
  - Task 1.2: [Description]
  - Verification: [How to verify this step works]

Step 2: [Step name] (Est: 45 min)
  - Task 2.1: [Description]
  - Task 2.2: [Description]
  - Dependencies: Requires Step 1
  - Verification: [How to verify]

Step 3: [Step name] (Est: 60 min)
  - Task 3.1: [Description]
  - Task 3.2: [Description]
  - Dependencies: Requires Steps 1, 2
  - Verification: [How to verify]

[Continue...]

Final Step: Testing & Documentation (Est: 30 min)
  - Write unit tests
  - Update documentation
  - Manual testing
```

### 3.2 Estimate Complexity

**Provide estimates:**

```
📊 Complexity Analysis

Total Steps: [X]
Estimated Time: [Y] hours

Risk Assessment:
  • Low Risk Steps: [List]
  • Medium Risk Steps: [List]
  • High Risk Steps: [List]

Unknowns:
  • [Unknown 1]: [Mitigation plan]
  • [Unknown 2]: [Mitigation plan]

Dependencies:
  • External: [List external dependencies]
  • Internal: [List code dependencies]

Recommended Approach:
  • Start with: [Step X] (lowest risk)
  • Test incrementally after each step
  • Deploy: [When safe to deploy]
```

### 3.3 Create Feature Checklist

Create: `.agent/decisions/[feature-name]-plan.md`

**Format:**
```markdown
# [Feature Name] - Implementation Plan

**Created:** [Date]
**Phase:** [Phase]
**Estimated Time:** [X] hours
**Priority:** [High / Medium / Low]

---

## Goal

[Feature description and user value]

---

## Architecture

[Diagram or description from Step 2.1]

---

## Implementation Checklist

### Setup
- [ ] Install dependencies: [list]
- [ ] Configure [API/MCP if needed]
- [ ] Create feature branch (optional): `feature/[name]`

### Step 1: [Name]
- [ ] Task 1.1: [Description]
- [ ] Task 1.2: [Description]
- [ ] Verify: [Verification method]

### Step 2: [Name]
- [ ] Task 2.1: [Description]
- [ ] Task 2.2: [Description]
- [ ] Verify: [Verification method]

[Continue for all steps...]

### Testing
- [ ] Write unit tests for [component]
- [ ] Test edge cases
- [ ] Manual testing via Telegram
- [ ] Verify with production data

### Documentation
- [ ] Update TECHNICAL_ARCHITECTURE.md
- [ ] Update PRODUCT_OVERVIEW.md
- [ ] Update phase roadmap
- [ ] Add code comments

### Deployment
- [ ] Run /workflow test-and-push
- [ ] Monitor deployment
- [ ] Test in production
- [ ] Update QUICK_START_NEXT_SESSION.md

---

## Risk Mitigation

**High Risk Items:**
- [Item]: [Mitigation plan]

**Rollback Plan:**
- [How to rollback if feature breaks production]

---

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## Notes

[Any additional notes or considerations]
```

**Report:** `✅ Created: .agent/decisions/[feature-name]-plan.md`

---

## Step 4: Prepare Environment

### 4.1 Install Dependencies

If new Python packages needed:

```bash
pip install [package1] [package2]
```

**Verify installation:**
```bash
pip list | grep [package-name]
```

**Update requirements.txt:**
```bash
pip freeze | grep [package-name] >> requirements.txt
```

**Report:** `✅ Dependencies installed and added to requirements.txt`

### 4.2 Configure External Services (If Needed)

**If API keys needed:**
```
API Configuration Required:

  1. [Service name]
     - Get API key from: [URL]
     - Add to .env: [VAR_NAME]=your_key
     - Add to Render env vars

  2. [Service name]
     - [Instructions]

Complete configuration manually, then press Enter to continue.
```

**If MCP setup needed:**
```
MCP Configuration Required:

  1. [MCP name]
     - Follow: .claude/mcp-setup.md
     - Restart Claude Code after configuration

Mark as done when complete? (yes/no)
```

### 4.3 Create Feature Branch (Optional)

Ask: **"Create feature branch for this work? (yes/no)"**

If yes:
```bash
git checkout -b feature/[feature-name]
```

**Report:** `✅ Created and switched to: feature/[feature-name]`

If no:
```
ℹ️ Working on main branch
```

### 4.4 Verify Test Environment

Run existing tests to ensure starting from clean state:

```bash
pytest scripts/ -v
```

**Report:** `✅ All existing tests passing - clean baseline`

---

## Step 5: Summary & Next Actions

### 5.1 Complete Planning Summary

```
╔═══════════════════════════════════════════════╗
║   📋 FEATURE PLANNING COMPLETE 📋            ║
╚═══════════════════════════════════════════════╝

Feature: [Name]
Phase: [Phase]
Estimated Time: [X] hours

✅ Research Complete:
   • Best practices identified
   • Tools selected
   • Pitfalls noted

✅ Architecture Designed:
   • [X] files to modify
   • [Y] new files to create
   • Database changes: [Yes/No]

✅ Implementation Plan Created:
   • [Z] steps defined
   • Saved to: .agent/decisions/[feature]-plan.md

✅ Environment Prepared:
   • Dependencies: Installed
   • Configuration: [Complete / Needs manual setup]
   • Branch: [feature/name / main]

═══════════════════════════════════════════════

Next Steps:

  1. Review plan: .agent/decisions/[feature]-plan.md
  2. Start with Step 1: [Step name]
  3. Test incrementally after each step
  4. When complete: /workflow test-and-push

Ready to start coding! 🚀

═══════════════════════════════════════════════
```

### 5.2 Update Phase Roadmap

Update: `.agent/decisions/phase-[X]-roadmap.md`

Mark feature as **"In Progress"** with:
- Start date
- Estimated completion
- Link to implementation plan

**Report:** `✅ Updated phase roadmap`

---

## Special Scenarios

### Scenario A: Feature Depends on Unfinished Work

If dependencies not complete:
```
⚠️ Dependency Warning

This feature requires:
  • [Dependency 1]: Currently [status]
  • [Dependency 2]: Currently [status]

Recommendation: Complete dependencies first

Options:
  1. Complete dependencies now
  2. Plan this feature for later
  3. Modify feature to work without dependencies

What would you like to do?
```

### Scenario B: Feature Too Complex

If estimate > 8 hours:
```
⚠️ Complexity Warning

Estimated time: [X] hours (> 8 hours)

This feature may be too large for a single implementation.

Recommendation: Break into smaller features

Suggested breakdown:
  • Phase 1: [MVP version] (2-4 hours)
  • Phase 2: [Enhancement] (2-3 hours)
  • Phase 3: [Advanced features] (3-4 hours)

Break down feature? (yes/no)
```

### Scenario C: Unknown Territory

If feature involves unfamiliar tech:
```
📚 Learning Required

This feature involves:
  • [Technology/Pattern you haven't used]

Recommendation: Research first

Suggested learning path:
  1. [Tutorial/Documentation link]
  2. [Example project to study]
  3. Build small proof-of-concept first

Add learning time to estimate? (yes/no)
```

---

## Error Handling

**Research Failed:**
```
⚠️ Could not find sufficient information about [topic]

This may indicate:
  • Novel approach (good!)
  • Niche technology
  • Need for different search terms

Proceed with planning anyway? (yes/no)
```

**Cannot Create Plan File:**
```
❌ Error creating plan file

Error: [details]

Options:
  1. Retry
  2. Display plan (you can save manually)
  3. Skip plan documentation

Choose:
```

---

## Notes

- **Thorough planning saves time** - don't rush this
- **Research is key** - learn from others' experiences
- **Break down complexity** - smaller steps = less risk
- **Test assumptions** - verify architecture makes sense
- **Document everything** - future you will thank you
