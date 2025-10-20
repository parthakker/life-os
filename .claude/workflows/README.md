# Life OS Workflows

**Automated orchestration for development, deployment, and operations**

---

## What Are Workflows?

Workflows are **automated multi-step processes** that handle complex operations for you. Instead of running multiple commands manually, you invoke a single workflow that orchestrates everything.

**Think of them as DevOps agents** that help YOU manage the Life OS project.

---

## Available Workflows

### 🚀 `/workflow deploy`
**Complete deployment automation** (8 steps)

**Use when:** You're ready to deploy code to production

**What it does:**
1. Run pre-deployment tests
2. Check git status
3. Push to GitHub
4. Monitor Render deployment
5. Run database migration (if needed)
6. Verify production health
7. Update documentation
8. Provide complete summary

**Time:** 5-10 minutes (mostly waiting for Render)

**Example:**
```
You: /workflow deploy
Claude: [Runs all 8 steps automatically, asks for confirmations at critical points]
```

---

### ✅ `/workflow test-and-push`
**Safe code deployment** (test → commit → push → deploy)

**Use when:** You've written code and want to deploy it safely

**What it does:**
1. Run all tests (stops if any fail)
2. Show git changes for review
3. Generate smart commit message
4. Execute commit
5. Push to GitHub
6. Auto-trigger `/workflow deploy` (from Step 3)

**Time:** 3-5 minutes + deployment time

**Example:**
```
You: /workflow test-and-push
Claude:
  ✅ 15 tests passed
  📝 Suggested commit: "feat(calendar): Add Google Calendar agent"
  Use this message? (yes/no)
```

---

### 👋 `/workflow new-session`
**Session startup automation**

**Use when:** Starting a new coding session

**What it does:**
1. Welcome message with context from last session
2. Check Render service health
3. Check database connection
4. Verify vector store
5. Review pending tasks
6. Check for uncommitted changes
7. Set up environment
8. Provide session roadmap

**Time:** 1-2 minutes

**Example:**
```
You: /workflow new-session
Claude:
  ╔═══════════════════════════════════════════════╗
  ║  🚀 Welcome back to Life OS Development!      ║
  ╚═══════════════════════════════════════════════╝

  Last session: Yesterday (1 days ago)
  Current phase: Phase 2B (Calendar Integration)

  System Health Check:
  ✅ Render Service: RUNNING
  ✅ Database: CONNECTED (41 categories)
  ✅ Vector Store: 95 items

  What would you like to work on today?
```

---

### 📋 `/workflow end-session`
**Clean shutdown & documentation**

**Use when:** Ending your coding session

**What it does:**
1. Check for uncommitted changes (help commit if needed)
2. Generate session summary
3. Update QUICK_START_NEXT_SESSION.md
4. Create session log
5. Production health check
6. Set next session goals
7. Farewell summary

**Time:** 2-3 minutes

**Example:**
```
You: /workflow end-session
Claude:
  📝 Uncommitted changes detected:
    M scripts/router.py (+45, -10 lines)

  Commit changes now? (yes/no)
```

---

### 🎯 `/workflow new-feature`
**Feature planning wizard**

**Use when:** Planning a new feature before coding

**What it does:**
1. Ask detailed questions about the feature
2. Research best practices (web search)
3. Analyze existing codebase for patterns
4. Design high-level architecture
5. Identify files to change/create
6. Estimate complexity and time
7. Create detailed implementation checklist
8. Prepare environment (install dependencies, etc.)

**Time:** 10-20 minutes (thorough planning)

**Example:**
```
You: /workflow new-feature
Claude:
  🎯 Feature Planning Wizard

  What feature are you planning to build?

You: Google Calendar integration
Claude:
  [Asks questions, researches, creates plan...]

  ✅ Created: .agent/decisions/calendar-integration-plan.md

  Implementation Steps:
    Step 1: Set up Google Calendar MCP (30 min)
    Step 2: Create calendar_agent.py (45 min)
    Step 3: Update router.py (30 min)
    [etc...]

  Total estimate: 4 hours

  Ready to start coding!
```

---

### 🚨 `/workflow emergency`
**Production incident response**

**Use when:** Something is broken in production

**What it does:**
1. Assess severity (P0-P3)
2. Quick triage (service status, logs, database)
3. Try quick wins (restart, check env vars, rollback)
4. Detailed diagnosis
5. Implement fix
6. Verify resolution
7. Document incident
8. Set up prevention

**Time:** Varies (5 min - 2 hours depending on severity)

**Example:**
```
You: /workflow emergency
Claude:
  ═══════════════════════════════════════════════
  🚨 PRODUCTION INCIDENT RESPONSE 🚨
  ═══════════════════════════════════════════════

  What's the issue?

You: Bot is not responding
Claude:
  Severity: P0 (CRITICAL)

  📋 Quick Triage:
  ⚠️ Render Service: Crashed (last restart: 5 min ago)
  ❌ Last 100 logs show: MemoryError

  Quick actions:
  1. Restart service immediately
  2. Check memory usage trends

  Restart now? (yes/no)
```

---

## How Workflows Work

### Behind the Scenes

Each workflow is a **detailed prompt** that guides Claude Code through a multi-step process:

```
.claude/workflows/
├── deploy.md           # Deployment orchestration prompt
├── test-and-push.md    # Test & deploy prompt
├── new-session.md      # Session startup prompt
├── end-session.md      # Session shutdown prompt
├── new-feature.md      # Feature planning prompt
└── emergency.md        # Incident response prompt
```

When you type `/workflow deploy`, Claude Code:
1. Reads `deploy.md`
2. Follows the step-by-step instructions
3. Uses MCPs (Render, GitHub) to interact with services
4. Asks you for decisions at critical points
5. Reports progress and results

### User Control

You're **always in control**:
- Workflows ask for confirmation at critical steps
- You can type `pause`, `skip`, or `abort` anytime
- Workflows explain what they're doing
- You make final decisions (they just automate the tedious parts)

---

## Workflow Chaining

Workflows can call other workflows:

```
/workflow test-and-push
  → Runs tests
  → Commits code
  → Pushes to GitHub
  → Auto-calls: /workflow deploy
    → Monitors deployment
    → Runs migration
    → Updates docs
```

---

## Common Workflow Patterns

### **Starting Your Day:**
```
/workflow new-session
→ Health check
→ Review pending work
→ Set today's goals
```

### **After Coding:**
```
/workflow test-and-push
→ Tests pass
→ Commits & pushes
→ Auto-deploys
→ Verifies production
```

### **Ending Your Day:**
```
/workflow end-session
→ Saves work
→ Updates docs
→ Sets next session goals
```

### **Planning New Feature:**
```
/workflow new-feature
→ Research & design
→ Create implementation plan
→ Prepare environment
```

---

## Best Practices

### ✅ DO:
- Run `/workflow new-session` at the start of each session
- Run `/workflow test-and-push` before deploying
- Run `/workflow end-session` when ending your day
- Use `/workflow new-feature` for any non-trivial feature
- Keep `/workflow emergency` handy for production issues

### ❌ DON'T:
- Skip workflows to "save time" (they save you time!)
- Ignore workflow warnings
- Override safety checks without understanding why
- Deploy without running tests
- End session without updating docs

---

## Customization

You can modify workflows to fit your needs:

**To edit a workflow:**
1. Open `.claude/workflows/[workflow-name].md`
2. Modify steps, add/remove checks, change prompts
3. Save
4. Next time you run the workflow, it uses your changes

**Example customization:**
- Add specific tests to run in `test-and-push.md`
- Add team notifications to `deploy.md`
- Add custom health checks to `new-session.md`

---

## Troubleshooting

### Workflow Not Found
```
Error: Workflow 'deploy' not found
```
**Fix:** Ensure file exists at `.claude/workflows/deploy.md`

### Workflow Hangs
```
Workflow seems stuck...
```
**Fix:** Type `status` to see current step, or `abort` to stop

### MCP Not Working
```
Error: Render MCP not available
```
**Fix:** Restart Claude Code to activate MCPs

---

## Future Workflows (Ideas)

- `/workflow backup` - Backup database and vector store
- `/workflow migrate-db` - Database migration wizard
- `/workflow performance` - Performance analysis and optimization
- `/workflow security` - Security audit
- `/workflow docs` - Auto-generate documentation

---

## Workflow vs Manual Commands

| Task | Manual | With Workflow |
|------|--------|---------------|
| Deploy | 15+ commands, 15-20 min | `/workflow deploy`, 5-10 min |
| Test & Push | 8+ commands, 10 min | `/workflow test-and-push`, 3-5 min |
| Session Start | 5+ checks, 5 min | `/workflow new-session`, 1-2 min |
| Session End | Manual doc updates, 10 min | `/workflow end-session`, 2-3 min |
| Plan Feature | Ad-hoc, varies | `/workflow new-feature`, 10-20 min |

**Time saved:** ~50% on routine tasks

---

## Philosophy

Workflows embody the Life OS approach:

**For your app:**
- Users brain-dump → AI organizes → Semantic search

**For your development:**
- You code → Workflows orchestrate → Production deployed

**Both systems:** Intelligent automation that handles the tedious stuff so you can focus on what matters.

---

## Quick Reference Card

```
═══════════════════════════════════════════════
Life OS Workflows - Quick Reference
═══════════════════════════════════════════════

Daily Use:
  /workflow new-session       Start your day
  /workflow test-and-push     Deploy your code
  /workflow end-session       End your day

Planning:
  /workflow new-feature       Plan before coding

Emergency:
  /workflow emergency         Fix production issues

Full Deployment:
  /workflow deploy            Complete deployment

Commands During Workflow:
  pause   - Pause workflow
  skip    - Skip current step
  abort   - Stop workflow
  status  - Show progress
  help    - Show commands

═══════════════════════════════════════════════
```

---

**Happy automating! 🚀**

*Last updated: October 20, 2025*
