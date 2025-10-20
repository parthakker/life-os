# Life OS - Cloud Deployment Guide

## Quick Deploy to Railway

### Option 1: Deploy via Railway Dashboard (Recommended)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub (easiest)

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your `life-os` repository

3. **Configure Environment Variables**
   In Railway dashboard, go to Variables tab and add:
   ```
   TELEGRAM_BOT_TOKEN=8479331593:AAEdxa4w7pWeATybTnC_bXZT9J4QrpUx3n4
   TELEGRAM_USER_ID=6573778096
   ANTHROPIC_API_KEY=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
   ```

4. **Deploy**
   - Railway will auto-detect Python
   - It will use `railway.toml` for configuration
   - Bot will start automatically
   - Check logs to verify it's running

### Option 2: Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set TELEGRAM_BOT_TOKEN=8479331593:AAEdxa4w7pWeATybTnC_bXZT9J4QrpUx3n4
railway variables set TELEGRAM_USER_ID=6573778096
railway variables set ANTHROPIC_API_KEY=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

# Deploy
railway up
```

## Alternative: Deploy to Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Background Worker"
   - Connect your GitHub repo
   - Name: `life-os-bot`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python scripts/telegram_bot.py`

3. **Add Environment Variables**
   ```
   TELEGRAM_BOT_TOKEN=8479331593:AAEdxa4w7pWeATybTnC_bXZT9J4QrpUx3n4
   TELEGRAM_USER_ID=6573778096
   ANTHROPIC_API_KEY=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
   ```

4. **Deploy**
   - Click "Create Background Worker"
   - Monitor logs for successful startup

## Important Notes

### Database Persistence
- **Railway/Render ephemeral storage**: Your `data.db` and `vector_store.json` will reset on every redeploy
- **Solution Options**:
  1. Use Railway's Volume feature (persistent disk)
  2. Migrate to PostgreSQL (recommended for production)
  3. Use cloud storage (S3, Google Cloud Storage)

### For Initial Deployment
Since you already have data locally, you'll need to:

1. **Include your database in the first deploy**:
   - Comment out `data.db` and `vector_store.json` in `.gitignore`
   - Commit and push
   - Deploy
   - Then uncomment them again

2. **OR Set up Railway Volume**:
   - Create a volume in Railway dashboard
   - Mount it to `/app` directory
   - Upload your `data.db` and `vector_store.json` to the volume

### Cost Estimates
- **Railway**: $5/month (Hobby plan) - 500 hours + $0.000231/min after
- **Render**: Free tier available (sleeps after inactivity) or $7/month

### Monitoring
After deployment, check logs:
- Railway: Click "View Logs" in dashboard
- Render: Go to "Logs" tab

You should see:
```
[OK] Starting Life OS Telegram Bot...
[OK] Bot token: 8479331593:AAEdxa...
[Vector Store] Loading embedding model...
[Vector Store] Model loaded successfully
[OK] Bot is running!
```

### Testing
Send a message to your Telegram bot:
- "buy milk tomorrow" (should add task)
- "what are my home tasks" (should query with RAG)

## Troubleshooting

**Bot not responding?**
- Check environment variables are set correctly
- Verify bot token is valid
- Check logs for errors

**Database empty?**
- Your local `data.db` wasn't uploaded
- Follow "Include your database in the first deploy" steps above

**Out of memory?**
- sentence-transformers model is ~90MB
- Railway/Render free tiers should handle this
- If issues, upgrade to paid tier
