# New Session Workflow - Session Startup Automation

You are the **New Session Orchestrator** for Life OS.

Welcome the user and prepare the development environment for a productive session.

---

## Step 1: Welcome & Context

### 1.1 Greet User

Display welcome message:

```
╔═══════════════════════════════════════════════╗
║  🚀 Welcome back to Life OS Development!      ║
╚═══════════════════════════════════════════════╝

Loading session information...
```

### 1.2 Load Session Context

Read: `QUICK_START_NEXT_SESSION.md`

Extract:
- Last session date
- Current phase
- Deployment status
- Pending tasks

**Display:**
```
Last session: [date] ([X] days ago)
Current phase: [Phase 2B / 3B / etc.]
Status: [Brief status from doc]
```

---

## Step 2: System Health Check

### 2.1 Check Render Deployment

Use **Render MCP**:
- Service status (running/stopped/failed)
- Last deploy timestamp
- Recent restarts (if any)

**Quick log check:**
- Get last 20 lines
- Look for errors or warnings
- Check for "Bot is running!"

**Report:**
```
✅ Render Service: RUNNING
   Last deploy: [time ago]
   Status: Healthy
   Logs: No errors detected
```

Or if issues:
```
⚠️ Render Service: RUNNING (with warnings)
   Last deploy: [time ago]
   Warning: [details from logs]

   → Recommendation: [action to take]
```

### 2.2 Check Database

Use **Render MCP Shell**:
```bash
python -c "import scripts.db_helper as db; conn = db.get_db_connection(); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM categories'); print(f'✓ Database connected: {cursor.fetchone()[0]} categories')"
```

**Also query:**
```bash
python -c "
import scripts.db_helper as db
conn = db.get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM tasks WHERE completed = FALSE')
active_tasks = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM notes')
notes = cursor.fetchone()[0]
print(f'Active tasks: {active_tasks}, Notes: {notes}')
"
```

**Report:**
```
✅ Database: Connected
   Categories: 41
   Active tasks: 12
   Notes: 23
```

### 2.3 Check Vector Store

Use **Render MCP Shell**:
```bash
python -c "import json; data = json.load(open('vector_store.json')); print(f'Vector store: {data[\"metadata\"][\"total_items\"]} items')"
```

**Report:**
```
✅ Vector Store: 95 items
   Last updated: [timestamp]
   Size: 1.08 MB
```

### 2.4 Overall Health Summary

Combine all checks:

```
═══════════════════════════════════════════════
System Health Check
═══════════════════════════════════════════════

✅ Render Service:     RUNNING (healthy)
✅ PostgreSQL:         CONNECTED (41 categories)
✅ Vector Store:       SYNCED (95 items)
✅ Bot Status:         OPERATIONAL

Last activity: 2 hours ago
Service uptime: 14 days

All systems healthy. Ready to code! 🎉
```

Or if issues detected:
```
⚠️ Issues detected:

1. [Issue description]
   → Suggested fix: [action]

2. [Issue description]
   → Suggested fix: [action]

Run diagnostics? (yes/no)
```

---

## Step 3: Review Pending Work

### 3.1 Show Next Steps from Docs

From `QUICK_START_NEXT_SESSION.md`:

**Display:**
```
📋 Pending Tasks (from last session)

Next Steps:
  1. [Step 1 from doc]
  2. [Step 2 from doc]
  3. [Step 3 from doc]

Current focus: [Main goal from doc]
```

### 3.2 Check for Uncommitted Changes

Run: `git status`

**If changes exist:**
```
⚠️ Uncommitted changes from last session:

  M scripts/router.py
  M scripts/vector_store.py

Options:
  1. Review changes
  2. Commit changes
  3. Discard changes (⚠️ will lose work)
  4. Continue (keep changes uncommitted)

What would you like to do?
```

**If clean:**
```
✅ Git status: Clean (no uncommitted changes)
```

### 3.3 Ask User for Session Goal

**Prompt user:**
```
What would you like to work on today?

Options:
  1. Continue with [next step from docs]
  2. Work on a different feature (describe)
  3. Fix bugs / investigate issues
  4. Run diagnostics / health checks
  5. Update documentation

Your choice: [1-5 or describe]
```

**Store user's response** for session summary later

---

## Step 4: Environment Setup

### 4.1 Check Git Branch

Run: `git branch --show-current`

**If not on main:**
```
ℹ️ Current branch: [branch-name]

This is a feature branch. Continue here or switch to main?
  1. Stay on [branch-name]
  2. Switch to main
  3. Create new feature branch

Your choice:
```

### 4.2 Sync with Remote (Optional)

Ask: **"Pull latest changes from GitHub? (yes/no)"**

If yes:
```bash
git pull origin main
```

**Report:**
- Up to date → `✅ Already up to date`
- New commits → `✅ Pulled [N] new commits`
- Conflicts → Show conflicts, guide resolution

### 4.3 Check Dependencies

Run: `pip list | grep -E "(anthropic|telegram|sentence-transformers|psycopg2)"`

**Check versions:**
- anthropic: [version]
- python-telegram-bot: [version]
- sentence-transformers: [version]
- psycopg2-binary: [version]

**If outdated packages detected:**
```
ℹ️ Dependency updates available:
  • anthropic: 0.39.0 → 0.40.0
  • python-telegram-bot: 20.6 → 20.7

Update now? (yes/no)
```

If yes: `pip install --upgrade [packages]`

### 4.4 Verify Local Environment

Quick sanity check:
```bash
python -c "import scripts.router as r; import scripts.vector_store as v; import scripts.db_helper as d; print('✓ All imports successful')"
```

**Report:** `✅ Local environment: Ready`

---

## Step 5: Session Summary & Recommendations

### 5.1 Provide Session Roadmap

Based on phase and next steps:

```
╔═══════════════════════════════════════════════╗
║       📋 SESSION ROADMAP                      ║
╚═══════════════════════════════════════════════╝

Current Phase: Phase 2B (Calendar Integration)

Today's Goal: [User's stated goal from Step 3.3]

Recommended workflow:
  1. [Specific recommendation based on goal]
  2. [Next step]
  3. [Testing step]

Suggested commands:
  • /workflow new-feature (if planning new feature)
  • /workflow test-and-push (when ready to deploy)
  • /workflow end-session (when done for the day)

Estimated time: [Rough estimate]
```

### 5.2 Quick Reference

```
═══════════════════════════════════════════════
Quick Reference
═══════════════════════════════════════════════

Service ID: srv-d3r9ocbe5dus73b4vs4g
Database: lifeos (PostgreSQL)
Repository: parthakker/life-os

Key Files:
  • scripts/telegram_bot.py   - Bot entry point
  • scripts/router.py          - Agentic routing
  • scripts/vector_store.py    - RAG system
  • .claude/workflows/         - Automation workflows

Useful Commands:
  • /workflow deploy          - Full deployment
  • /workflow test-and-push   - Test, commit, push
  • /workflow end-session     - Clean shutdown
```

---

## Step 6: Ready to Code

**Final message:**

```
═══════════════════════════════════════════════

✅ Session initialized successfully!

System: HEALTHY
Environment: READY
Phase: [Current phase]
Goal: [Today's goal]

You're all set. Happy coding! 🚀

═══════════════════════════════════════════════
```

---

## Special Scenarios

### Scenario A: First Session After Deployment

If this is first session after a deploy:
```
🎉 Welcome to your first session after deployment!

✅ Life OS is now live in production
✅ Service running on Render
✅ PostgreSQL database operational

Recommended first actions:
  1. Test bot via Telegram
  2. Send test messages
  3. Verify RAG search works
  4. Monitor logs for any issues

Test now? (yes/no)
```

### Scenario B: Long Time Since Last Session

If last session > 7 days ago:
```
👋 Welcome back! It's been [X] days since your last session.

Recommended actions:
  1. Review what changed (git log)
  2. Check for dependency updates
  3. Verify production is still healthy
  4. Re-familiarize with codebase

Run extended health check? (yes/no)
```

### Scenario C: Issues Detected

If health check found issues:
```
⚠️ Issues detected during startup:

[List of issues with severity]

Recommended workflow:
  1. Address critical issues first
  2. Then continue with planned work

Run /workflow emergency for diagnostics? (yes/no)
```

---

## Error Handling

**Render Service Down:**
```
❌ Critical: Render service is not responding

This requires immediate attention.

Actions:
  1. Check Render dashboard: https://dashboard.render.com
  2. View deployment logs
  3. Restart service if needed

Investigate now? (yes/no)
```

**Database Connection Failed:**
```
❌ Critical: Cannot connect to PostgreSQL

Possible causes:
  - DATABASE_URL environment variable missing
  - Database service down
  - Network issues

Troubleshooting:
  1. Check Render environment variables
  2. Verify database service is running
  3. Test connection manually

Run diagnostics? (yes/no)
```

---

## Notes

- **Be welcoming and informative**
- **Prioritize critical issues** before suggesting work
- **Provide context** from last session
- **Set clear expectations** for the session
- **Make it easy to jump into coding** quickly
