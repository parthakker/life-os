# End Session Workflow - Clean Shutdown & Documentation

You are the **End Session Orchestrator** for Life OS.

Ensure clean shutdown, save all work, and prepare for next session.

---

## Step 1: Save Work in Progress

### 1.1 Check for Uncommitted Changes

Run: `git status --short`

**If changes exist:**
```
📝 Uncommitted changes detected:

  M scripts/router.py (+45, -10 lines)
  M scripts/calendar_agent.py (new file)
  M requirements.txt (+1 line)

Options:
  1. Commit changes now
  2. Stash changes for later
  3. Discard changes (⚠️ will lose work)
  4. Leave uncommitted (⚠️ may cause issues)

What would you like to do?
```

### 1.2 Guide Commit Process (If User Chooses Option 1)

**Stage files:**
- Ask: "Stage all files? (yes/no)"
- If no: Ask user to specify files

**Generate commit message:**
- Analyze changes
- Suggest conventional commit message
- Format:
  ```
  [type](scope): Brief description

  - Detailed change 1
  - Detailed change 2

  [Work in progress / Partial implementation / etc.]
  ```

**Execute commit:**
```bash
git commit -m "[message]"
```

**Report:** `✅ Changes committed: [hash]`

### 1.3 Optional Push

Ask: **"Push to GitHub? (yes/no)"**

If yes:
```bash
git push origin main
```

**Report:** `✅ Pushed to GitHub`

If no:
```
ℹ️ Changes saved locally only.
Remember to push next session!
```

---

## Step 2: Session Summary

### 2.1 Analyze Session Activity

**Gather information:**
- Files modified (from git)
- Commits made
- Time spent (approximate from session start)
- Key activities

**Ask user:**
```
What did you accomplish this session?

Quick summary (or press Enter to auto-generate):
```

If user provides summary → Use it
If user skips → Auto-generate from git activity

### 2.2 Generate Session Summary

**Template:**
```
═══════════════════════════════════════════════
Session Summary - [Date]
═══════════════════════════════════════════════

Duration: ~[X] hours
Phase: [Current phase]

Accomplished:
  • [Activity 1]
  • [Activity 2]
  • [Activity 3]

Files Modified:
  • [file 1] (+X, -Y lines)
  • [file 2] (new file)

Commits Made:
  • [hash] - [message]

Tests:
  • Status: [Passing / Not run / Failed]

Deployment:
  • Status: [Deployed / Not deployed / In progress]
```

Display summary and ask: **"Save this summary? (yes/no)"**

---

## Step 3: Update Documentation

### 3.1 Update QUICK_START_NEXT_SESSION.md

Read current content, then update:

```markdown
# Quick Start - Resume After Claude Code Restart

**Last Updated:** [Current Date/Time]
**Status:** [Current status]

---

## 🎯 Current Status

### ✅ Completed This Session
- [List of accomplishments]

### ⏳ In Progress
- [What's currently being worked on]
- [Any partial implementations]

### 🔜 Next Steps
1. [Top priority for next session]
2. [Second priority]
3. [Third priority]

---

## 🔑 Key Information

**Service ID:** srv-d3r9ocbe5dus73b4vs4g

**Current Phase:** [Phase]

**Recent Changes:**
- [Change 1]
- [Change 2]

**Health Status:**
- Render Service: [RUNNING / STOPPED / ISSUES]
- Database: [CONNECTED / NEEDS MIGRATION / ISSUES]
- Vector Store: [X] items
- Bot Status: [OPERATIONAL / NEEDS TESTING / ISSUES]

---

## ⚠️ Important Notes

[Any warnings, blockers, or important reminders]

---

## 📋 Resume Commands (Next Session)

```
/workflow new-session    # Start next session with health check
/workflow deploy         # If changes ready to deploy
```

---

**Ready to restart Claude Code and continue!**
```

**Report:** `✅ Updated: QUICK_START_NEXT_SESSION.md`

### 3.2 Create Session Log

Create: `.agent/logs/session-summary-[date].md`

**Format:**
```markdown
# Session Summary - [Full Date]

**Start Time:** [Time]
**End Time:** [Time]
**Duration:** [Duration]
**Phase:** [Current phase]

---

## Overview

[Brief description of session goals and outcomes]

---

## Accomplishments

### Code Changes
- [File 1]: [What was changed and why]
- [File 2]: [What was changed and why]

### Features Implemented
- [Feature 1]: [Status - Complete / Partial / Blocked]
- [Feature 2]: [Status]

### Bug Fixes
- [Bug 1]: [Description and fix]

### Testing
- Tests run: [Yes / No]
- Results: [All passed / X failed]
- Coverage: [If measured]

### Deployment
- Deployed: [Yes / No]
- Service status: [Status]
- Issues: [Any deployment issues]

---

## Key Decisions

[Any architectural or implementation decisions made]

---

## Files Modified

```
git diff --stat (or list from git status)
```

---

## Commits

- `[hash]` - [message]
- `[hash]` - [message]

---

## Next Session Goals

1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

---

## Blockers / Issues

[Any blockers that need resolution]

---

## Notes

[Any additional notes, learnings, or reminders]

---

**Session complete. Ready for next session!**
```

**Report:** `✅ Created: .agent/logs/session-summary-[date].md`

### 3.3 Update Architecture Doc (If Major Changes)

If significant architectural changes were made:

Ask: **"Update current-architecture.md with session changes? (yes/no)"**

If yes:
- Update `.agent/system/current-architecture.md`
- Add notes about new components
- Update diagrams if needed
- Update deployment status

---

## Step 4: Final Health Check

### 4.1 Verify Production Status

Use **Render MCP**:
- Check service is still running
- Get last 10 log lines
- Look for any errors introduced this session

**Report:**
```
✅ Production Health Check

Service: RUNNING
Recent logs: No errors
Last activity: [time]
Memory: [X]MB / 512MB
```

Or if issues:
```
⚠️ Production Warning

Issue detected: [description]
Recommendation: [action]

Address now? (yes/no)
```

### 4.2 Verify No Broken State

Quick checks:
- Git status clean (or intentionally uncommitted)
- No processes left running locally
- No temporary files to clean up

**Report:** `✅ Environment clean`

---

## Step 5: Next Session Preparation

### 5.1 Set Next Session Goals

Ask user: **"What are the top 3 priorities for next session?"**

Save to QUICK_START_NEXT_SESSION.md under "Next Steps"

### 5.2 Check for Blockers

Ask: **"Any blockers or issues to note for next session?"**

If yes → Save to documentation with ⚠️ warning

### 5.3 Estimate Next Session

Based on priorities:
```
📅 Next Session Plan

Priorities:
  1. [Priority 1] - Est. [time]
  2. [Priority 2] - Est. [time]
  3. [Priority 3] - Est. [time]

Total estimated time: ~[X] hours

Recommended workflow:
  • Start: /workflow new-session
  • [Specific recommendation based on priorities]
  • End: /workflow end-session
```

---

## Step 6: Farewell

### 6.1 Complete Summary

```
╔═══════════════════════════════════════════════╗
║     📋 SESSION COMPLETE 📋                    ║
╚═══════════════════════════════════════════════╝

Session Duration: [X] hours
Phase: [Current phase]

✅ Completed:
   • [Top 3 accomplishments]

✅ Saved:
   • [Number] commits
   • Pushed to GitHub: [Yes/No]

✅ Documentation:
   • QUICK_START_NEXT_SESSION.md: Updated
   • session-summary-[date].md: Created
   • current-architecture.md: [Updated / Unchanged]

✅ Production Status:
   • Service: [Status]
   • Health: [Healthy / Warnings]

📋 Next Session:
   • Priority 1: [Goal]
   • Priority 2: [Goal]
   • Priority 3: [Goal]

═══════════════════════════════════════════════

All work saved. Ready to close Claude Code.

See you next time! 👋

═══════════════════════════════════════════════
```

---

## Special Scenarios

### Scenario A: Emergency Exit

If user needs to exit quickly:
```
⚡ Quick exit mode

1. Save uncommitted changes? (yes/no)
2. Skip documentation updates? (yes/no)

Minimal exit in progress...
```

### Scenario B: Deployment in Progress

If deployment is still running:
```
⚠️ Render deployment in progress

Current status: [Building / Deploying]

Options:
  1. Wait for deployment to finish
  2. Leave it running (will complete automatically)
  3. Cancel deployment (⚠️ may break production)

What would you like to do?
```

### Scenario C: Failed Tests

If tests failed during session:
```
⚠️ Warning: Tests are currently failing

Failed tests:
  • [test 1]
  • [test 2]

This should be fixed before next deploy.

Priority for next session:
  1. Fix failing tests ⚠️ HIGH PRIORITY

Mark as blocker? (yes/no)
```

---

## Error Handling

**Cannot Save Documentation:**
```
❌ Error saving documentation files

Error: [details]

Options:
  1. Retry save
  2. Save manually (show content to copy)
  3. Skip documentation (⚠️ not recommended)

What would you like to do?
```

**Git Errors:**
```
❌ Git operation failed

Error: [git error]

Your work is safe in modified files.

Options:
  1. Show git status
  2. Create backup of changes
  3. Get help with git issue

Choose:
```

---

## Checklist (Internal)

Before completing workflow, verify:

- [ ] Uncommitted changes: Addressed
- [ ] QUICK_START_NEXT_SESSION.md: Updated
- [ ] Session log: Created
- [ ] Production: Healthy
- [ ] Next session goals: Set
- [ ] User confirmed: Ready to exit

---

## Notes

- **Be thorough but efficient** - don't make session end tedious
- **Prioritize saving work** over documentation
- **Provide clear next steps** so user can resume easily
- **Celebrate accomplishments** - positive reinforcement
- **Handle edge cases gracefully** - quick exit if needed
