# Quick Start - Resume After Claude Code Restart

**Last Updated:** October 20, 2025 - 2:00 PM
**Status:** Ready for Render deployment with MCP

---

## 🎯 Current Status

### ✅ Completed
- Phase 2A RAG system complete
- PostgreSQL migration code complete
- SSH authentication configured (personal GitHub)
- All code pushed to GitHub: https://github.com/parthakker/life-os
- Render service created: `srv-d3r6u5ogjchc73bsiibg`
- PostgreSQL database created: `lifeos` (connection string saved in Render)
- All environment variables configured in Render
- **3 MCPs configured:**
  - ✅ GitHub MCP (active)
  - ✅ Render MCP (active after restart)
  - ⏳ Google Calendar MCP (disabled, for Phase 2B)

### ⏳ In Progress
- Render deployment (auto-deploying from GitHub push)
- Waiting for "Bot is running!" in logs

### 🔜 Next Steps
1. **After restart:** Use Render MCP to check deployment logs
2. Run migration via Render MCP
3. Test production bot
4. Security cleanup

---

## 🔑 Key Information

**GitHub Repository:**
```
https://github.com/parthakker/life-os
```

**Render Service ID:**
```
srv-d3r6u5ogjchc73bsiibg
```

**PostgreSQL Database:**
```
Name: lifeos
Connection: postgresql://lifeos_user:nS2SUCw1PRQ4CZvzJELSuWGptCtbQMz7@dpg-d3r8oj6uk2gs73cbdlu0-a/lifeos
```

**Environment Variables (Already Set in Render):**
- TELEGRAM_BOT_TOKEN: ✅ Configured
- TELEGRAM_USER_ID: ✅ Configured
- ANTHROPIC_API_KEY: ✅ Configured (new key after old one was exposed)
- DATABASE_URL: ✅ Auto-linked from PostgreSQL database

---

## 📋 Resume Commands (After Restart)

### 1. Check Deployment Status
Ask Claude Code:
```
"Check my Render deployment logs for srv-d3r6u5ogjchc73bsiibg"
```

### 2. Run Migration (When Bot is Running)
Ask Claude Code:
```
"Run the PostgreSQL migration script on Render"
```

### 3. Test Bot
You test manually via Telegram:
- `/start` - Welcome message
- `buy milk tomorrow` - Add task
- `/stats` - Show statistics
- `what are my wedding tasks` - RAG search

### 4. Security Cleanup
Ask Claude Code:
```
"Re-hide the data files in .gitignore and push to GitHub"
```

---

## 🛠️ MCP Tools Available After Restart

**GitHub MCP:**
- Create repos, issues, PRs
- Manage repositories

**Render MCP:**
- Check deployment logs
- Run shell commands on services
- Monitor service status
- Update environment variables

**Google Calendar MCP (Disabled):**
- Will enable in Phase 2B

---

## 📚 Important Documents

**For Deployment:**
- `DEPLOYMENT.md` - Complete step-by-step guide
- `AFTER_DEPLOYMENT_CLEANUP.md` - Post-deployment security

**For Architecture:**
- `.agent/system/current-architecture.md` - System design
- `.agent/decisions/phase-2b-4-roadmap.md` - Future roadmap

**For Troubleshooting:**
- Check DEPLOYMENT.md "Troubleshooting" section

---

## ⚠️ Known Issues / Reminders

1. **GitHub Token Revoked:**
   - Old token `ghp_vhkW...` was exposed in old commit
   - Revoked and replaced with new token
   - No action needed

2. **Data Files Temporarily Exposed:**
   - data.db and vector_store.json are in GitHub (one-time for migration)
   - Will re-hide after successful deployment

3. **SSH for Git:**
   - Personal projects use: `git@github.com-personal:parthakker/life-os.git`
   - Business projects use: `git@github.com:princetonaipartners/...`

---

## 🎯 Success Criteria

Deployment is complete when:
- ✅ "Bot is running!" appears in Render logs
- ✅ PostgreSQL migration completes (41 categories, XX tasks, XX notes)
- ✅ `/stats` command shows your data
- ✅ RAG search works ("what are my wedding tasks")
- ✅ Data persists after Render service restart
- ✅ data.db and vector_store.json re-hidden in .gitignore

---

## 💰 Monthly Cost

- Render Background Worker: $7.00/month (paid tier, always awake)
- PostgreSQL Database: $0.00/month (free tier)
- Claude Haiku API: ~$0.36/month (20 messages/day)
- **Total: ~$7.36/month**

---

**Ready to restart Claude Code and continue!**
