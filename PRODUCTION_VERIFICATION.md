# Production Verification Quick Reference

**Last Updated:** October 22, 2025 - 2:00 AM
**Status:** Ready for tomorrow's debugging session

---

## Quick Health Check

### 1. Verify Telegram Bot → Production DB Pipeline

**Step 1: Check current production state**
```bash
export DATABASE_URL="postgresql://lifeos_user:nS2SUCw1PRQ4CZvzJELSuWGptCtbQMz7@dpg-d3r8oj6uk2gs73cbdlu0-a.ohio-postgres.render.com/lifeos"

python -c "
from scripts.db_helper import execute_query
import os
os.environ['DATABASE_URL'] = '$DATABASE_URL'

# Count total tasks
tasks = execute_query('SELECT COUNT(*) as c FROM tasks', fetch='one')
print(f'Total tasks: {tasks[\"c\"]}')

# Show latest task
latest = execute_query('SELECT id, content, created_date FROM tasks ORDER BY id DESC LIMIT 1', fetch='one')
print(f'Latest: ID {latest[\"id\"]}, \"{latest[\"content\"]}\"')
print(f'Created: {latest[\"created_date\"]}')
"
```

**Expected:** 79-85 tasks (depends on testing), latest should be from Oct 22

**Step 2: Send test message via Telegram**
```
Send to @lifeos2_bot: "test production write [current time]"
```

**Step 3: Immediately verify in production**
```bash
python -c "
from scripts.db_helper import execute_query
import os
os.environ['DATABASE_URL'] = '$DATABASE_URL'

latest = execute_query('SELECT id, content, created_date FROM tasks ORDER BY id DESC LIMIT 1', fetch='one')
print(f'Latest: ID {latest[\"id\"]}, \"{latest[\"content\"]}\"')
"
```

**Success Criteria:** New task appears with content matching your test message

---

## Connect Dashboard to Production

### Option A: Local API → Production DB (FASTEST)

**Terminal 1 - API Server with Production DB:**
```bash
cd scripts
export DATABASE_URL="postgresql://lifeos_user:nS2SUCw1PRQ4CZvzJELSuWGptCtbQMz7@dpg-d3r8oj6uk2gs73cbdlu0-a.ohio-postgres.render.com/lifeos"
python api_server.py
```

**Expected Output:**
```
Database: postgres
Server running on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Test:** Navigate to http://localhost:5180
- Should show 79+ tasks (not 71 from local SQLite)
- Health charts should load with migrated data
- All categories should display correct task counts

### Option B: Windows Environment Variable (PERSISTENT)

```cmd
# PowerShell (run as Administrator)
setx DATABASE_URL "postgresql://lifeos_user:nS2SUCw1PRQ4CZvzJELSuWGptCtbQMz7@dpg-d3r8oj6uk2gs73cbdlu0-a.ohio-postgres.render.com/lifeos"

# Restart terminals for change to take effect
# Then run normally:
cd scripts
python api_server.py
```

---

## Quick Database Queries

### All Tables Summary
```bash
export DATABASE_URL="postgresql://lifeos_user:nS2SUCw1PRQ4CZvzJELSuWGptCtbQMz7@dpg-d3r8oj6uk2gs73cbdlu0-a.ohio-postgres.render.com/lifeos"

python -c "
from scripts.db_helper import execute_query
import os
os.environ['DATABASE_URL'] = '$DATABASE_URL'

tables = ['categories', 'tasks', 'notes', 'sleep_logs', 'water_logs', 'exercise_logs', 'sauna_logs', 'inbody_measurements']

for table in tables:
    result = execute_query(f'SELECT COUNT(*) as c FROM {table}', fetch='one')
    count = result['c'] if result else 0
    print(f'{table}: {count} rows')
"
```

**Expected Production Counts (as of Oct 22, 1:30 AM):**
- categories: 50 rows
- tasks: 79-85 rows
- notes: 20 rows
- sleep_logs: 31 rows (30 migrated + 1 new from Telegram)
- water_logs: 0 rows (migration failed, manual entry)
- exercise_logs: 15 rows
- sauna_logs: 8 rows
- inbody_measurements: 5 rows

### Recent Tasks
```bash
python -c "
from scripts.db_helper import execute_query
import os
os.environ['DATABASE_URL'] = '$DATABASE_URL'

tasks = execute_query('SELECT id, content, created_date FROM tasks ORDER BY id DESC LIMIT 10', fetch='all')
for task in tasks:
    print(f'[{task[\"id\"]}] {task[\"content\"]} ({task[\"created_date\"]})')
"
```

### Health Data Verification
```bash
python -c "
from scripts.db_helper import execute_query
import os
os.environ['DATABASE_URL'] = '$DATABASE_URL'

# Latest sleep log
sleep = execute_query('SELECT * FROM sleep_logs ORDER BY date DESC LIMIT 1', fetch='one')
print(f'Latest sleep: {sleep[\"hours\"]} hours on {sleep[\"date\"]}')

# Exercise summary
exercise = execute_query('SELECT COUNT(*) as c, SUM(duration_minutes) as total FROM exercise_logs', fetch='one')
print(f'Exercise: {exercise[\"c\"]} sessions, {exercise[\"total\"]} minutes total')

# InBody latest
inbody = execute_query('SELECT * FROM inbody_measurements ORDER BY date DESC LIMIT 1', fetch='one')
print(f'Latest InBody: {inbody[\"weight\"]} lbs on {inbody[\"date\"]}')
"
```

---

## Telegram Bot Health Check

### Check Render Service Status
```bash
curl -H "Authorization: Bearer rnd_QjyBrYyANyjxjcndK026CRHVzsJH" \
  "https://api.render.com/v1/services/srv-d3r9ocbe5dus73b4vs4g"
```

### View Recent Logs
```bash
curl -H "Authorization: Bearer rnd_QjyBrYyANyjxjcndK026CRHVzsJH" \
  "https://api.render.com/v1/services/srv-d3r9ocbe5dus73b4vs4g/logs?limit=100"
```

### Restart Service (Kill Zombie Instances)
```bash
# Suspend
curl -X POST -H "Authorization: Bearer rnd_QjyBrYyANyjxjcndK026CRHVzsJH" \
  "https://api.render.com/v1/services/srv-d3r9ocbe5dus73b4vs4g/suspend"

# Wait 5 seconds
sleep 5

# Resume
curl -X POST -H "Authorization: Bearer rnd_QjyBrYyANyjxjcndK026CRHVzsJH" \
  "https://api.render.com/v1/services/srv-d3r9ocbe5dus73b4vs4g/resume"
```

---

## Dashboard Testing with Playwright MCP

**Verify Playwright MCP is installed:**
```bash
claude mcp list | grep playwright
```

**Test Workflow:**
1. Start API server with production DB (see above)
2. Start frontend dev server
3. Use Playwright to:
   - Navigate to http://localhost:5180
   - Verify health charts render
   - Click different categories
   - Verify task counts match production
   - Screenshot all panels

---

## Known Issues & Fixes

### Issue 1: Dashboard Shows Local Data (71 tasks)
**Symptom:** Dashboard shows 71 tasks instead of 79+

**Diagnosis:**
```bash
# Check which DB the API is using
curl http://localhost:5000/api/tasks | jq 'length'
# If returns 71 → connected to local SQLite
# If returns 79+ → connected to production PostgreSQL
```

**Fix:** Set DATABASE_URL before starting API server

---

### Issue 2: Telegram Bot Not Writing
**Symptom:** Bot responds but production DB not updating

**Diagnosis:**
1. Check Render logs for errors
2. Query production DB for latest task
3. Compare task IDs with bot responses

**Fix:** Suspend → Resume service to kill zombies

---

### Issue 3: Health Charts Don't Load
**Symptom:** Dashboard shows health panel but no data

**Diagnosis:**
```bash
# Check if health data exists in DB
curl http://localhost:5000/api/health/sleep | jq '.'
```

**Fix:** Verify API server connected to production DB (has migrated health data)

---

## Success Criteria for Tomorrow

✅ **Telegram Bot Verification:**
- [ ] Send 3 test messages (task, note, health log)
- [ ] All 3 appear in production DB within 5 seconds
- [ ] No errors in Render logs

✅ **Dashboard Production Connection:**
- [ ] API server shows "Database: postgres"
- [ ] Dashboard displays 79+ tasks
- [ ] Health charts load with data
- [ ] Task counts match production database

✅ **End-to-End Pipeline:**
- [ ] Send Telegram message → appears in production DB → shows in dashboard
- [ ] All within 10 seconds with zero errors

---

## Contacts & Resources

**Production Database:**
```
postgresql://lifeos_user:nS2SUCw1PRQ4CZvzJELSuWGptCtbQMz7@dpg-d3r8oj6uk2gs73cbdlu0-a.ohio-postgres.render.com/lifeos
```

**Telegram Bot:**
- Username: @lifeos2_bot
- Token: 7972961951:AAH4hUa5vv884awuR3_B2d5b1p5KTqR7IK0
- Authorized User ID: 6573778096

**Render Service:**
- Service ID: srv-d3r9ocbe5dus73b4vs4g
- Dashboard: https://dashboard.render.com/worker/srv-d3r9ocbe5dus73b4vs4g
- API Key: rnd_QjyBrYyANyjxjcndK026CRHVzsJH

**MCPs Installed:**
- GitHub MCP ✅
- Filesystem MCP ✅
- Google Calendar MCP ✅
- Render MCP ✅
- Playwright MCP ✅

---

**Ready to debug! Tomorrow we verify the full pipeline and get that dashboard showing LIVE production data. 🚀**
