# Life OS - Render Deployment Guide

**Complete step-by-step guide for deploying Life OS to Render with PostgreSQL**

---

## Prerequisites

✅ Render account created (https://render.com - sign up with GitHub)
✅ GitHub repository: `parthakker/life-os`
✅ Service created: `srv-d3r6u5ogjchc73bsiibg` ($7/month paid tier)
✅ Local data ready: `data.db` and `vector_store.json`

---

## Part 1: Create PostgreSQL Database

### Step 1: Create Database in Render

1. Go to Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name:** `life-os-db`
   - **Database:** `lifeos`
   - **User:** `lifeos` (or leave default)
   - **Region:** Same as your service (Oregon recommended)
   - **Plan:** **Free** (sufficient for your data)

4. Click **"Create Database"**
5. Wait 2-3 minutes for provisioning
6. **IMPORTANT:** Copy the **Internal Database URL** (looks like `postgresql://...`)
   - Save this - you'll need it in the next step

---

## Part 2: Configure Environment Variables

### Step 2: Add Environment Variables to Service

1. Go to your service: `srv-d3r6u5ogjchc73bsiibg`
2. Click **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"**
4. Add these 4 variables ONE BY ONE:

**Variable 1:**
```
Key: TELEGRAM_BOT_TOKEN
Value: 8479331593:AAEdxa4w7pWeATybTnC_bXZT9J4QrpUx3n4
```

**Variable 2:**
```
Key: TELEGRAM_USER_ID
Value: 6573778096
```

**Variable 3:**
```
Key: ANTHROPIC_API_KEY
Value: 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
```

**Variable 4:**
```
Key: DATABASE_URL
Value: <paste the Internal Database URL from Step 1>
```

5. Click **"Save Changes"**

---

## Part 3: Deploy Code

### Step 3: Push to GitHub

From your local machine:

```bash
cd /c/Users/parth/OneDrive/Desktop/life-os

# Check what will be committed
git status

# Should see:
# - render.yaml (new)
# - db_helper.py (new)
# - migrate_to_postgres.py (new)
# - data.db (NOW VISIBLE - temporary)
# - vector_store.json (NOW VISIBLE - temporary)
# - Modified: requirements.txt, telegram_bot.py, router.py, .gitignore

# Add all changes
git add .

# Commit
git commit -m "Deploy to Render with PostgreSQL migration

- Add render.yaml configuration
- Create db_helper.py for database abstraction
- Create migrate_to_postgres.py migration script
- Update all scripts to support PostgreSQL
- Add psycopg2-binary to requirements
- Temporarily expose data.db and vector_store.json for initial deploy

Service ID: srv-d3r6u5ogjchc73bsiibg
Database: life-os-db (PostgreSQL free tier)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub
git push origin main
```

### Step 4: Monitor Render Deployment

1. Go to your Render service dashboard
2. Render will **auto-deploy** when it detects the push
3. Watch the **"Logs"** tab (real-time):

Expected output:
```
==> Installing dependencies from requirements.txt
==> Successfully installed python-telegram-bot anthropic psycopg2-binary sentence-transformers...
==> Build successful
==> Starting service with 'python scripts/telegram_bot.py'
[Vector Store] Loading embedding model...
[Vector Store] Model loaded successfully
[OK] Starting Life OS Telegram Bot...
[OK] Bot is running!
```

4. **Wait for "Bot is running!"** message (takes 2-3 minutes first time due to model download)

---

## Part 4: Migrate Data to PostgreSQL

### Step 5: Run Migration Script

1. In Render dashboard, go to your service
2. Click **"Shell"** tab (left sidebar)
3. Click **"Launch Shell"** button
4. In the shell, run:

```bash
python scripts/migrate_to_postgres.py
```

Expected output:
```
[Migration] Starting SQLite → PostgreSQL migration...
[1/4] Creating PostgreSQL tables...
[✓] Tables created successfully
[2/4] Migrating categories...
[✓] Migrated 41 categories
[3/4] Migrating tasks...
[✓] Migrated XX tasks
[4/4] Migrating notes...
[✓] Migrated XX notes

[Verification]
  Categories: 41
  Tasks: XX
  Notes: XX

[✓] Migration completed successfully!
```

5. **Type `exit`** to close shell

---

## Part 5: Test Production Bot

### Step 6: Verify Everything Works

**Test 1: Basic Response**
```
You (Telegram): /start
Bot: 🤖 Life OS Agentic Assistant is ready! ...
```

**Test 2: Add Task**
```
You: buy milk tomorrow
Bot: ✓ Task added to Home
     Content: buy milk tomorrow
     Due: 2025-10-21
     ID: XXX
```

**Test 3: Statistics**
```
You: /stats
Bot: Life OS Statistics:

     Active Tasks: XX
     Completed Tasks: XX
     Notes: XX
     Categories: 41

     Keep crushing it!
```

**Test 4: RAG Search**
```
You: what are my wedding tasks
Bot: 💭 Found X tasks:

     ⏳ [Wedding] Book photographer
     ...
```

### Step 7: Verify Data Persistence

1. In Render dashboard → Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Wait for redeployment
3. Test bot again with `/stats`
4. **Data should still be there!** (PostgreSQL persists)

---

## Part 6: Security Cleanup

### Step 8: Re-Hide Data Files

**IMPORTANT:** Now that data is in PostgreSQL, re-hide local files:

```bash
cd /c/Users/parth/OneDrive/Desktop/life-os

# Edit .gitignore - restore these lines:
# Change:
#   # data.db
#   # *.db
#   # vector_store.json
# Back to:
#   data.db
#   *.db
#   vector_store.json

# Commit the security fix
git add .gitignore
git commit -m "Security: Re-hide local data files after successful deployment"
git push origin main
```

See `AFTER_DEPLOYMENT_CLEANUP.md` for detailed instructions.

---

## Deployment Complete! 🎉

Your Life OS is now running 24/7 on Render with:
- ✅ Always-awake bot ($7/month paid tier)
- ✅ PostgreSQL database (free tier)
- ✅ All your data migrated
- ✅ RAG search working
- ✅ Secure (data files hidden from future commits)

---

## Monitoring & Maintenance

### Check Logs
```
Render Dashboard → Your Service → Logs tab
```

### Update Code
```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push origin main

# Render auto-deploys
# Data persists in PostgreSQL
```

### Re-vectorize (if needed)
```bash
# In Render shell:
python scripts/vector_store.py vectorize --force
```

---

## Cost Breakdown

**Monthly Costs:**
- Render Background Worker (Paid): **$7.00/month**
- PostgreSQL Database (Free): **$0.00/month**
- Claude Haiku API (~20 msgs/day): **~$0.36/month**
- **Total: ~$7.36/month**

**When to upgrade:**
- PostgreSQL: When data > 1GB (upgrade to $7/mo)
- Render: Already on paid tier (always awake)

---

## Troubleshooting

### Bot not responding?
1. Check Render logs for errors
2. Verify environment variables are set
3. Test DATABASE_URL connection in shell:
   ```bash
   python -c "import os; print(os.getenv('DATABASE_URL'))"
   ```

### Database empty after deploy?
1. Check if migration script ran: `python scripts/migrate_to_postgres.py`
2. Verify data.db and vector_store.json were in the commit
3. Check PostgreSQL connection: Look for `psycopg2.OperationalError` in logs

### RAG not finding items?
1. Verify vector_store.json exists: `ls -la vector_store.json`
2. Check file size: `du -h vector_store.json` (should be ~1MB)
3. Re-vectorize if needed

### Out of memory?
1. sentence-transformers model is ~90MB
2. Paid tier has 512MB RAM (sufficient)
3. If issues, check logs for `MemoryError`

---

## Next Steps: Phase 2B

Once deployment is stable, proceed to **Google Calendar Integration**:
1. Set up Google Calendar API credentials
2. Enable Google Calendar MCP in `.claude/settings.local.json`
3. Add `schedule_event` tool to router
4. See `.agent/decisions/phase-2b-4-roadmap.md` for details

---

**Deployment Guide Version:** 1.0
**Last Updated:** October 20, 2025
**Service ID:** srv-d3r6u5ogjchc73bsiibg
**Database:** life-os-db (PostgreSQL)
