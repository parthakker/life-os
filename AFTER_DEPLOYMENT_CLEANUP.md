# Post-Deployment Cleanup Instructions

**IMPORTANT: Complete these steps AFTER your first successful deployment to Render**

## Step 1: Verify Deployment Success

Before cleanup, ensure:
- ✅ Render deployment completed successfully
- ✅ PostgreSQL migration ran (check logs for "Migration completed successfully!")
- ✅ Bot responds to Telegram messages
- ✅ `/stats` command shows your data count
- ✅ RAG search works ("what are my tasks")

## Step 2: Re-Hide Data Files in Git

1. **Edit `.gitignore`** - Restore the original settings:

Replace these lines:
```
# TEMPORARY: Uncommenting for initial deployment ONLY
# data.db
# *.db
```

With:
```
data.db
*.db
```

And replace:
```
# TEMPORARY: Uncommenting for initial deployment ONLY
# vector_store.json
```

With:
```
vector_store.json
```

2. **Commit the change:**
```bash
git add .gitignore
git commit -m "Security: Re-hide local data files after successful deployment"
git push origin main
```

## Step 3: Verify Files Are Hidden

Check that future git status doesn't show data files:
```bash
# Make a test change to data.db (it won't actually change in production)
touch data.db

# Check git status
git status

# You should NOT see data.db or vector_store.json listed
```

## Step 4: Document Render Environment

Save these details for future reference:

**Service ID:** `srv-d3r6u5ogjchc73bsiibg`

**Environment Variables Set:**
- TELEGRAM_BOT_TOKEN
- TELEGRAM_USER_ID
- ANTHROPIC_API_KEY
- DATABASE_URL (from PostgreSQL database)

**Database Name:** life-os-db

## Step 5: Test Everything Again

Final verification:
1. Send test message via Telegram: "test cleanup - buy milk"
2. Query: "what are my milk tasks"
3. Check `/stats` - should still show all your data

## Step 6: Delete This File

Once cleanup is complete and verified:
```bash
git rm AFTER_DEPLOYMENT_CLEANUP.md
git commit -m "Cleanup: Remove post-deployment instructions"
git push origin main
```

---

**Status:** Pending completion after first deployment
**Date:** 2025-10-20
