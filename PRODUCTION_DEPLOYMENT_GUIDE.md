# Production Deployment Guide - Health Tracking + Schema Updates

## Overview

This guide will help you deploy:
1. ✅ Category hierarchy (parent_id, sort_order)
2. ✅ Category descriptions (AI-generated)
3. ✅ Health tracking tables (sleep, water, exercise, sauna, inbody)
4. ✅ Telegram bot health logging

**IMPORTANT**: This will preserve all your existing production data (tasks, notes, categories)

---

## Pre-Deployment: Backup Production Database

### Option A: Via Render Dashboard (Recommended)
1. Go to https://dashboard.render.com
2. Navigate to your `life-os-db` database
3. Click **"Backups"** tab
4. Click **"Create Backup"** button
5. Wait for backup to complete (~1-2 minutes)
6. **Download backup** to your computer for safety

### Option B: Via pg_dump (Advanced)
```bash
# Get DATABASE_URL from Render dashboard
# Format: postgresql://user:password@host/database

pg_dump "your-database-url-here" > life_os_backup_$(date +%Y%m%d).sql
```

---

## Step 1: Run Migrations on Production

### 1.1 Set Production Database URL

**Windows (PowerShell)**:
```powershell
$env:DATABASE_URL="postgresql://your-database-url-from-render"
```

**Windows (CMD)**:
```cmd
set DATABASE_URL=postgresql://your-database-url-from-render
```

**Mac/Linux**:
```bash
export DATABASE_URL="postgresql://your-database-url-from-render"
```

**How to get DATABASE_URL**:
1. Go to Render Dashboard → `life-os-db`
2. Find "Internal Database URL" or "External Database URL"
3. Copy the full PostgreSQL connection string

### 1.2 Install PostgreSQL Python Driver (if not already installed)

```bash
pip install psycopg2-binary
```

### 1.3 Run Migrations IN ORDER

```bash
cd scripts

# Migration 1: Add parent_id and build hierarchy
python migrate_category_hierarchy_postgres.py

# Migration 2: Add descriptions
python migrate_category_descriptions_postgres.py

# Migration 3: Create health tables
python migrate_health_tables_postgres.py
```

### 1.4 Verify Migrations

Each migration will print a summary. Look for:
- ✅ "MIGRATION COMPLETED SUCCESSFULLY!"
- ✅ No error messages
- ✅ Table/column counts match expectations

**If any migration fails**:
1. Check error message
2. DO NOT proceed to next migration
3. Fix issue or restore from backup
4. Contact support if needed

---

## Step 2: Deploy Code to Render

### 2.1 Commit All Changes

```bash
git add .
git commit -m "Add health tracking + schema migrations

- PostgreSQL-compatible migrations for production
- Category hierarchy (parent_id, sort_order)
- Category descriptions from AI
- Health tables (sleep, water, exercise, sauna, inbody)
- Telegram bot health logging support
"
```

### 2.2 Push to GitHub

```bash
git push origin main
```

### 2.3 Monitor Render Deployment

1. Go to Render Dashboard → `life-os-bot`
2. Watch the deployment logs
3. Wait for "Deploy succeeded" message (~2-3 minutes)

**Common deployment issues**:
- Missing environment variables → Check Render settings
- Build errors → Check logs for missing dependencies
- Import errors → Verify all files committed and pushed

---

## Step 3: Test Health Logging via Telegram

### 3.1 Send Test Messages

Try each health logging tool:

```
You → Telegram Bot:
"I slept 8 hours last night"

Bot should respond:
"💤 Logged 8.0 hours of sleep for 2025-10-20"
```

```
"2 cups of water"
→ "💧 Logged 2 cup(s) of water for 2025-10-21"
```

```
"played pickleball for 60 minutes"
→ "🏃 Logged 60 min of Pickleball for 2025-10-21"
```

```
"20 minutes in sauna"
→ "🧖 Logged sauna session: 20 min for 2025-10-21"
```

### 3.2 Verify Data in Database

**Option A: Via API (if deployed)**
```bash
curl https://your-render-api-url.onrender.com/api/health/summary
```

**Option B: Via Render Shell**
1. Render Dashboard → `life-os-bot`
2. Click "Shell" tab
3. Run:
```bash
python
>>> from db_helper import execute_query
>>> execute_query("SELECT * FROM sleep_logs LIMIT 5", fetch='all')
```

### 3.3 Test Task/Note Logging Still Works

```
"buy groceries tomorrow"
→ Should add task to Wedding - Vendors or appropriate category
```

---

## Step 4: Verify Production Data Intact

### 4.1 Check Task Count

Send Telegram message:
```
/stats
```

Expected response should show:
- Active Tasks: [your count]
- Completed Tasks: [your count]
- Notes: [your count]
- Categories: [your count - likely increased due to parent categories]

### 4.2 Verify Specific Data

Check that your recent task (ID 175 "Follow up with Lukki") still exists:

Via Render Shell:
```python
from db_helper import execute_query
execute_query("SELECT * FROM tasks WHERE id = 175", fetch='one')
```

---

## Troubleshooting

### Migration Failed

**Symptom**: Migration script shows error

**Solution**:
1. Note the error message
2. Check if column/table already exists (may be safe to ignore)
3. Restore from backup if data was corrupted:
   ```bash
   # Via Render dashboard: Backups → Restore
   ```

### Bot Not Responding to Health Messages

**Symptom**: Telegram bot doesn't recognize "I slept 8 hours"

**Possible causes**:
1. **ANTHROPIC_API_KEY not set** → Check Render environment variables
2. **Migration not run** → Health tables don't exist
3. **Code not deployed** → Old version still running

**Fix**:
1. Check Render logs for errors
2. Verify environment variables set
3. Re-deploy if needed

### Data Not Showing in Dashboard

**Symptom**: Dashboard shows old data or no health data

**Solution**:
1. Dashboard is currently local only (not deployed)
2. Deploy frontend to Vercel (see below) to access production data
3. Or check data via API:
   ```bash
   curl https://your-api.onrender.com/api/health/summary
   ```

---

## Optional: Deploy Frontend Dashboard

### Quick Deploy to Vercel

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow prompts:
# - Link to GitHub repo
# - Set build command: npm run build
# - Set output directory: dist
# - Add environment variable:
#   VITE_API_URL=https://your-render-api.onrender.com
```

### Access Dashboard
- Vercel will provide URL: `https://life-os-xyz123.vercel.app`
- Dashboard will show production data
- All panels resizable, live health tracking visible

---

## Success Checklist

- [ ] Production database backed up
- [ ] All 3 migrations run successfully
- [ ] Code deployed to Render
- [ ] Telegram bot responding
- [ ] Health logging works ("I slept 8 hours")
- [ ] Task/note logging still works ("buy groceries")
- [ ] /stats shows correct counts
- [ ] Old data intact (check task ID 175)

---

## Rollback Plan (If Needed)

### If something goes wrong:

1. **Restore database from backup**:
   - Render Dashboard → Backups → Select backup → Restore

2. **Revert code deployment**:
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Or deploy specific commit**:
   - Render Dashboard → Manual Deploy → Select previous commit

---

## Post-Deployment

### What's Working Now
✅ Telegram bot logs health data to production
✅ Category hierarchy and descriptions active
✅ All existing data preserved
✅ Schema matches local development environment

### Next Steps (Optional)
- Deploy frontend dashboard to Vercel for live health visualizations
- Add more health metrics (food tracking, steps, etc.)
- Calendar widget integration
- Export health data reports

---

## Support

If you encounter issues:
1. Check Render logs: Dashboard → Logs
2. Review error messages in Telegram bot responses
3. Verify DATABASE_URL is correct
4. Ensure all environment variables set

**Common environment variables needed**:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_USER_ID`
- `ANTHROPIC_API_KEY`
- `DATABASE_URL` (auto-set by Render)
