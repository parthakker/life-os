# Emergency Workflow - Production Incident Response

You are the **Emergency Response Orchestrator** for Life OS.

Handle production incidents quickly and methodically.

---

## ⚠️ EMERGENCY MODE ACTIVATED ⚠️

```
═══════════════════════════════════════════════
🚨 PRODUCTION INCIDENT RESPONSE 🚨
═══════════════════════════════════════════════

This workflow prioritizes:
  1. Service restoration
  2. User impact mitigation
  3. Root cause diagnosis
  4. Prevention of recurrence

Stay calm. Follow the steps.
═══════════════════════════════════════════════
```

---

## Step 1: Assess Severity

### 1.1 Quick Severity Classification

Ask: **"What's the issue?"**

**Classify as:**

**CRITICAL (P0):**
- Bot completely down
- Database inaccessible
- Data loss detected
- Security breach

**HIGH (P1):**
- Bot partially functional
- Some features broken
- Performance severely degraded
- Errors affecting multiple users

**MEDIUM (P2):**
- Single feature broken
- Intermittent errors
- Performance degraded but functional

**LOW (P3):**
- Minor bug
- Cosmetic issue
- No user impact

**Report:**
```
Severity: [P0/P1/P2/P3]
Impact: [Description]
Status: Investigating...
```

---

## Step 2: Immediate Triage (CRITICAL/HIGH only)

### 2.1 Check Service Status

Use **Render MCP**:
```
Service Status Check:
  • Status: [running / stopped / crashed]
  • Last restart: [timestamp]
  • Restart count: [number]
  • Memory: [usage]
  • CPU: [usage]
```

**If service crashed:**
```
🚨 SERVICE CRASHED

Quick actions:
  1. Restart service immediately
  2. Check crash logs
  3. Identify crash cause

Restart now? (yes/no)
```

### 2.2 Check Recent Logs

Use **Render MCP**: Get last 100 lines

**Look for:**
- Error stack traces
- Exception messages
- Warning patterns
- Last successful operation

**Common error patterns:**
```
❌ Database connection errors
❌ API rate limit exceeded
❌ Memory errors (OOM)
❌ Import/module errors
❌ Authentication failures
```

**Report:**
```
📋 Log Analysis

Errors detected:
  • [Error 1]: [Count] occurrences
  • [Error 2]: [Count] occurrences

Last successful operation:
  • [Operation] at [timestamp]

First error:
  • [Error message] at [timestamp]
```

### 2.3 Check Database

Use **Render MCP Shell**:
```bash
python -c "import scripts.db_helper as db; conn = db.get_db_connection(); print('✓ Database accessible')"
```

**If database fails:**
```
🚨 DATABASE CONNECTION FAILED

Possible causes:
  • DATABASE_URL missing/incorrect
  • Database service down
  • Network issues
  • Connection pool exhausted

Check:
  1. Render environment variables
  2. Database service status
  3. Connection string format
```

---

## Step 3: Quick Wins (Try First)

### 3.1 Simple Restart

**For:** Service crashes, memory issues, transient errors

```bash
# Via Render MCP: Restart service
```

**Monitor for 2 minutes:**
- Check if service comes back online
- Look for "Bot is running!" in logs
- Verify no immediate crash

**Result:**
- ✅ Service recovered → Monitor and investigate root cause
- ❌ Still broken → Continue to Step 3.2

### 3.2 Check Environment Variables

**Verify critical env vars:**
```
Required Variables:
  • TELEGRAM_BOT_TOKEN: [Set: Yes/No]
  • TELEGRAM_USER_ID: [Set: Yes/No]
  • ANTHROPIC_API_KEY: [Set: Yes/No]
  • DATABASE_URL: [Set: Yes/No]
```

**If missing:**
```
🚨 MISSING ENVIRONMENT VARIABLE

Variable: [NAME]
This is required for [purpose]

Add now via Render dashboard:
1. Go to Environment tab
2. Add: [NAME] = [value]
3. Trigger redeploy

Proceed? (yes/no)
```

### 3.3 Rollback to Last Known Good

**For:** Issues after recent deployment

Ask: **"Was there a recent deployment? (yes/no)"**

If yes:
```
📋 Recent Deployments

Latest: [commit hash] at [timestamp]
  • Message: [commit message]
  • Status: [Current issues]

Previous: [commit hash] at [timestamp]
  • Message: [commit message]
  • Status: [Was working]

Rollback to previous version? (yes/no)
```

**If rollback approved:**
```bash
# Via Render MCP or manual:
# 1. Find commit hash of last working version
# 2. Deploy that commit
git checkout [previous-hash]
git push origin main --force

# Or via Render: Manual Deploy → Select previous commit
```

**Monitor rollback:**
- Wait for deployment
- Check logs
- Verify service health

---

## Step 4: Detailed Diagnosis

### 4.1 Analyze Error Patterns

**Parse logs systematically:**

```python
# Pseudo-code for analysis
errors = parse_logs()
error_frequency = count_by_type(errors)
error_timeline = plot_timeline(errors)
affected_functions = identify_functions(errors)
```

**Report:**
```
📊 Error Analysis

Top Errors:
  1. [Error type]: [X] occurrences
     Pattern: [When it happens]
     Affected: [Which functions]

  2. [Error type]: [Y] occurrences
     Pattern: [When it happens]
     Affected: [Which functions]

Timeline:
  • First error: [timestamp]
  • Error spike: [timestamp]
  • Current rate: [errors/minute]
```

### 4.2 Check Recent Changes

**Review git history:**
```bash
git log --oneline -10
```

**For each recent commit:**
```
Recent Changes:
  • [hash]: [message] - [timestamp ago]
    Files: [list]
    Risk: [High/Medium/Low]

  • [hash]: [message] - [timestamp ago]
    Files: [list]
    Risk: [High/Medium/Low]
```

**Correlate with errors:**
- Did errors start after specific commit?
- Which files changed?
- What functionality affected?

### 4.3 External Dependencies Check

**Verify external services:**

```
External Service Health:
  • Telegram API: [Status]
  • Anthropic API: [Status]
  • PostgreSQL: [Status]
  • GitHub: [Status]

Check:
  1. status.telegram.org
  2. status.anthropic.com
  3. Render status page
```

**If external service down:**
```
🚨 EXTERNAL SERVICE OUTAGE

Service: [Name]
Status: [Down/Degraded]
ETA: [If known]

This is out of our control.

Options:
  1. Wait for service restoration
  2. Implement temporary workaround
  3. Disable affected feature

Choose:
```

---

## Step 5: Implement Fix

### 5.1 Identify Root Cause

Based on diagnosis:

```
🔍 Root Cause Analysis

Problem: [Description]

Cause: [What went wrong]

Evidence:
  • [Evidence 1]
  • [Evidence 2]

Contributing Factors:
  • [Factor 1]
  • [Factor 2]
```

### 5.2 Propose Solution

**Quick fix options:**

```
💡 Proposed Solutions

Option A: [Quick fix] (Time: [X] min)
  • Pros: [Benefits]
  • Cons: [Limitations]
  • Risk: [Low/Medium/High]

Option B: [Proper fix] (Time: [Y] hours)
  • Pros: [Benefits]
  • Cons: [Takes longer]
  • Risk: [Low/Medium/High]

Option C: [Workaround] (Time: [Z] min)
  • Pros: [Gets service back]
  • Cons: [Temporary only]
  • Risk: [Low/Medium/High]

Recommendation: [Which option and why]

Which option? (A/B/C)
```

### 5.3 Implement Fix

**Execute chosen solution:**

**For code fix:**
```
1. Make changes locally
2. Test locally
3. Run: /workflow test-and-push
4. Monitor deployment
5. Verify fix in production
```

**For configuration fix:**
```
1. Update environment variables
2. Restart service
3. Monitor logs
4. Verify fix
```

**For rollback:**
```
1. Deploy previous version
2. Monitor logs
3. Plan proper fix for later
```

---

## Step 6: Verify Resolution

### 6.1 Service Health Check

After fix deployed:

**Wait 5 minutes, then check:**
```
✅ Service Health

Status: [running]
Uptime: [X] minutes
Memory: [Y]MB / 512MB
CPU: [Z]%
Errors: [Count in last 5 min]
```

### 6.2 Functionality Test

**Test affected functionality:**

```
Testing: [Feature that was broken]

Test 1: [Description]
  • Expected: [Result]
  • Actual: [Result]
  • Status: [✓ / ✗]

Test 2: [Description]
  • Expected: [Result]
  • Actual: [Result]
  • Status: [✓ / ✗]
```

### 6.3 Monitor for Regression

**Continue monitoring for 15 minutes:**
```
Monitoring...

Time    | Status | Errors
--------|--------|-------
+5 min  | ✓ OK   | 0
+10 min | ✓ OK   | 0
+15 min | ✓ OK   | 0

✅ No regression detected
```

---

## Step 7: Post-Incident Actions

### 7.1 Document Incident

Create: `.agent/logs/incident-[date].md`

```markdown
# Incident Report - [Date]

**Severity:** [P0/P1/P2/P3]
**Duration:** [Start time] - [End time] ([X] minutes)
**Status:** RESOLVED

---

## Summary

[Brief description of what happened]

---

## Timeline

- [Time]: Issue first detected
- [Time]: Investigation started
- [Time]: Root cause identified
- [Time]: Fix implemented
- [Time]: Service restored
- [Time]: Incident closed

---

## Impact

- Users affected: [Number or description]
- Functionality impacted: [What was broken]
- Data loss: [Yes/No - details]
- Downtime: [X] minutes

---

## Root Cause

[Detailed explanation]

---

## Resolution

[How it was fixed]

---

## Prevention

Actions to prevent recurrence:
1. [Action 1]
2. [Action 2]
3. [Action 3]

---

## Lessons Learned

- [Lesson 1]
- [Lesson 2]
```

### 7.2 Update Monitoring

**Add alerts for this issue:**
```
Recommended Monitoring:
  • Alert: [What to monitor]
  • Threshold: [When to alert]
  • Action: [What to do]
```

### 7.3 Schedule Follow-Up

**If quick fix was used:**
```
⚠️ Follow-Up Required

Current state: Working (quick fix applied)
Proper fix needed: [Description]
Priority: [High/Medium/Low]
Estimated time: [X] hours

Add to next session goals? (yes/no)
```

---

## Step 8: All-Clear

### 8.1 Final Status

```
╔═══════════════════════════════════════════════╗
║        ✅ INCIDENT RESOLVED ✅                ║
╚═══════════════════════════════════════════════╝

Incident: [Description]
Severity: [P0/P1/P2/P3]
Duration: [X] minutes
Resolution: [How fixed]

Current Status:
  ✅ Service: RUNNING
  ✅ Health: HEALTHY
  ✅ Functionality: RESTORED
  ✅ Monitoring: ACTIVE

Documentation:
  ✅ Incident report: Created
  ✅ Follow-up tasks: [Added/Not needed]

═══════════════════════════════════════════════

Service restored. Continue monitoring.

═══════════════════════════════════════════════
```

### 8.2 Communication

**If this affects users (future):**
```
📢 User Communication

Draft message:
─────────────────────────────────
We experienced a temporary issue with [feature].

The issue has been resolved.

Impact: [Description]
Duration: [X] minutes
Current status: Fully operational

We apologize for any inconvenience.
─────────────────────────────────

Send notification? (yes/no)
```

---

## Common Issues & Quick Fixes

### Issue: Service Won't Start

**Symptoms:** Render shows "Live" but bot not responding

**Quick checks:**
1. Check "Bot is running!" in logs
2. Verify sentence-transformers model loaded
3. Check memory usage (may be OOM)
4. Verify all imports successful

**Fix:** Usually restart + wait 2-3 min for model load

---

### Issue: Database Connection Failed

**Symptoms:** Errors mentioning psycopg2, DATABASE_URL

**Quick checks:**
1. Verify DATABASE_URL env var set
2. Check database service status in Render
3. Test connection string format
4. Check for connection pool exhaustion

**Fix:** Restart service, verify env var, check DB service

---

### Issue: Memory Issues

**Symptoms:** Service crashes, OOM errors

**Quick checks:**
1. Check memory usage trends
2. Verify model loading once (not per request)
3. Check for memory leaks
4. Review vector store size

**Fix:** Restart, optimize code, upgrade plan if needed

---

### Issue: API Rate Limits

**Symptoms:** 429 errors, rate limit messages

**Quick checks:**
1. Check Anthropic API usage
2. Verify not in infinite loop
3. Check request patterns

**Fix:** Throttle requests, add delays, upgrade API plan

---

## Notes

- **Stay calm** - panic helps nobody
- **Prioritize restoration** over investigation
- **Document everything** - future you needs this
- **Learn from incidents** - prevent recurrence
- **Quick fix is OK** - perfect fix can wait if service is down
