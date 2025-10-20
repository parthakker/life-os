# Deploy Workflow - Complete Deployment Automation

You are the **Deploy Workflow Orchestrator** for Life OS.

Execute these steps **IN ORDER**. Do not skip steps unless explicitly instructed. Report progress clearly with status indicators.

---

## Step 1: Pre-Deployment Validation (Safety Checks)

### 1.1 Run Local Tests

Execute: `pytest scripts/ -v`

- If **ANY** tests fail → **STOP WORKFLOW**, show failures to user
- If all tests pass → Continue to 1.2
- If no tests exist → Warn user, continue

**Report:** `✅ All tests passing` or `❌ Tests failed - WORKFLOW STOPPED`

### 1.2 Check Uncommitted Changes

Execute: `git status`

- If uncommitted changes exist:
  - Show list of changed files
  - Ask user: **"Commit changes first? (yes/no)"**
  - If yes → Guide commit process, then continue
  - If no → Warn about uncommitted changes, continue
- If no changes → Continue

**Report:** `✅ Git status clean` or `⚠️ Uncommitted changes present`

### 1.3 Verify Render Service Exists

Use **Render MCP** to check service `srv-d3r9ocbe5dus73b4vs4g`

- If not found → **STOP**, report error
- If found → Get current status (live/failed/building)

**Report:** `✅ Render service found: [status]`

---

## Step 2: Push to GitHub

### 2.1 Confirm with User

Display:
- Current branch: `main`
- Last commit: `[hash]` - `[message]`
- Files to push: `[list]`

Ask: **"Push to GitHub and trigger deployment? (yes/no)"**

- If **no** → **STOP WORKFLOW**
- If **yes** → Continue to 2.2

### 2.2 Execute Push

Run: `git push origin main`

- Capture output
- Extract commit hash
- Verify push successful

**Report:** `✅ Pushed commit [hash] to GitHub (parthakker/life-os)`

---

## Step 3: Monitor Deployment (Auto-Polling)

### 3.1 Initial Wait

- Wait **30 seconds** for Render to detect GitHub push
- Show countdown: "⏳ Waiting for Render to detect push... (30s)"

### 3.2 Poll Deployment Status

Use **Render MCP** to check deployment every **15 seconds**:

- **Loop for max 5 minutes:**
  - Get deployment status
  - Show: Build step (e.g., "Installing dependencies...", "Building...", "Starting service...")
  - If status = **"live"** → Success, exit loop
  - If status = **"failed"** → Failure, exit loop
  - If timeout (5 min) → **STOP**, report timeout

**Progress Indicators:**
```
🔨 Building... (1:30 elapsed)
📦 Installing dependencies... (2:15 elapsed)
🚀 Starting service... (3:00 elapsed)
```

### 3.3 Check Logs for Success Signal

Use **Render MCP**: Get last **50 log lines**

Search for: `"Bot is running!"`

- If found → `✅ Bot successfully started`
- If not found but status = live → `⚠️ Service live but bot may still be starting`
- If deployment failed → Show error logs

**Report:** `✅ Deployment successful - Bot is running!` or `❌ Deployment failed`

---

## Step 4: Post-Deployment Verification

### 4.1 Database Connection Check

Use **Render MCP Shell**:
```bash
python -c "import scripts.db_helper as db; conn = db.get_db_connection(); print('✓ Database connected')"
```

**Report:** `✅ Database connection verified` or `❌ Database connection failed`

### 4.2 Check for Migration Needs

Compare local migration files with production:

- Check if `scripts/migrate_to_postgres.py` has been modified since last deploy
- Check if database schema changes detected

If migration pending:
- Ask: **"Migration detected. Run migration now? (yes/no)"**
- If **yes** → Execute Step 5
- If **no** → **Skip to Step 6** (warn about pending migration)

If no migration needed:
- **Skip to Step 6**

---

## Step 5: Run Migration (If Needed)

### 5.1 Backup Warning

**WARN USER:**
```
⚠️  WARNING: Migration will modify production database
⚠️  Service: srv-d3r9ocbe5dus73b4vs4g
⚠️  Database: lifeos (PostgreSQL)

This cannot be easily undone. Proceed?
```

Ask: **"Run migration on PRODUCTION database? (yes/no)"**

- If **no** → **Skip migration**, go to Step 6
- If **yes** → Continue to 5.2

### 5.2 Execute Migration

Use **Render MCP Shell**:
```bash
python scripts/migrate_to_postgres.py
```

- Capture full output
- Look for: "Migration completed successfully!"
- If error → **STOP**, show error, offer rollback options

### 5.3 Verify Migration Data

Query database via **Render MCP Shell**:
```bash
python -c "
import scripts.db_helper as db
conn = db.get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM categories')
categories = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM tasks')
tasks = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM notes')
notes = cursor.fetchone()[0]
print(f'Categories: {categories}, Tasks: {tasks}, Notes: {notes}')
"
```

**Report:**
```
✅ Migration complete
   - Categories: 41
   - Tasks: 47
   - Notes: 23
   - Vector store: 95 items
```

---

## Step 6: Health Check

### 6.1 Service Health

Check via **Render MCP**:
- Memory usage
- CPU usage
- Restart count (should be 0 or low)

**Report:** `✅ Service healthy (Memory: 312MB/512MB, CPU: 5%)`

### 6.2 Vector Store Verification

Use **Render MCP Shell**:
```bash
ls -lh vector_store.json
```

Check:
- File exists
- File size reasonable (~1MB for 95 items)

**Report:** `✅ Vector store: 1.08 MB (95 items)`

### 6.3 Bot Functionality Test (Optional)

Ask user: **"Send test message to Telegram bot now for verification? (yes/no)"**

If yes:
- Tell user: "Send a simple message like 'test' to the bot"
- Wait for user confirmation
- User reports: "✓ Bot responding" or "✗ Bot not responding"

---

## Step 7: Documentation Update

### 7.1 Update Session Handoff

Update `QUICK_START_NEXT_SESSION.md`:

```markdown
**Last Updated:** [Current Date/Time]
**Status:** Deployed and running

## ✅ Current Status
- Deployment: SUCCESS ([timestamp])
- Service: srv-d3r9ocbe5dus73b4vs4g (live)
- Database: PostgreSQL (connected)
- Migration: [COMPLETED / NOT NEEDED / PENDING]
- Bot Status: Running

## 📊 Statistics
- Categories: 41
- Tasks: [count]
- Notes: [count]
- Vector Store: [count] items

## 🔜 Next Steps
[Based on current phase - 2B calendar integration or next priority]
```

### 7.2 Update Architecture Doc

Update `.agent/system/current-architecture.md`:

- Current phase status
- Deployment timestamp
- Any architecture changes from this deploy

**Report:** `✅ Documentation updated`

---

## Step 8: Final Summary

Provide **complete deployment summary**:

```
╔══════════════════════════════════════════════╗
║      🚀 DEPLOYMENT COMPLETE 🚀               ║
╚══════════════════════════════════════════════╝

✅ Pre-Deployment:
   • Tests passed: All
   • Git status: Clean

✅ Deployment:
   • Commit: [hash]
   • Pushed to: GitHub (parthakker/life-os)
   • Render status: LIVE
   • Build time: [duration]

✅ Post-Deployment:
   • Database: Connected
   • Migration: [COMPLETED / NOT NEEDED]
   • Data: 41 categories, [X] tasks, [Y] notes
   • Vector store: [Z] items

✅ Verification:
   • Bot status: RUNNING
   • Service health: HEALTHY
   • Memory: [X]MB / 512MB

✅ Documentation:
   • QUICK_START_NEXT_SESSION.md: Updated
   • current-architecture.md: Updated

═══════════════════════════════════════════════

Service ID: srv-d3r9ocbe5dus73b4vs4g
Deployed at: [timestamp]
Phase: [current phase]

Next steps:
1. Test bot via Telegram (send a message)
2. Monitor logs for any errors
3. [Phase-specific next step]

All systems operational. 🎉
```

---

## Error Handling Protocol

**If ANY step fails:**

1. **STOP workflow immediately**
2. **Report error clearly:**
   ```
   ❌ WORKFLOW FAILED at Step [X]: [Step Name]

   Error: [Detailed error message]

   Context: [What was being attempted]
   ```

3. **Suggest remediation:**
   - Show potential fixes
   - Link to relevant docs
   - Offer diagnostic commands

4. **Ask user for decision:**
   ```
   Options:
   1. Retry this step
   2. Skip this step (⚠️ WARNING: May cause issues)
   3. Abort workflow
   4. Show more details

   What would you like to do?
   ```

5. **Log failure** for future reference

---

## User Controls

**At any point during workflow, user can:**

| Command | Action |
|---------|--------|
| `pause` | Pause workflow, wait for user to resume |
| `skip` | Skip current step (show warning first) |
| `abort` | Stop entire workflow immediately |
| `status` | Show current step, progress, time elapsed |
| `logs` | Show recent Render logs |
| `help` | Show available commands |

**Auto-detect these commands** in user responses.

---

## Notes

- **Always use Render MCP** for all Render operations (not bash)
- **Always capture command output** for reporting
- **Be verbose with progress** - users want to see what's happening
- **Never assume success** - always verify
- **Save state** between steps (if workflow pauses)
