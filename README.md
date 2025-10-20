# Life OS - AI-Powered Personal Assistant

**Brain-dump anywhere → AI understands → Search everything semantically**

## What Is Life OS?

Life OS is your intelligent personal assistant powered by Claude AI. Send messages via Telegram in natural language, and the AI automatically:
- Creates tasks with due dates
- Saves notes and observations
- Answers questions by searching your memory

### Current Status: Phase 2A Production

**Telegram Bot + Agentic Router + RAG System**

```
You (Telegram) → AI Router → Add Task / Add Note / Answer Question
                               ↓            ↓            ↓
                          Database    Database    Vector Search
                               ↓            ↓            ↓
                          Auto-Vectorize (instant semantic searchability)
```

## Features

### Core Capabilities
- **Telegram Bot** - Message from anywhere, 24/7
- **Agentic Routing** - AI decides what to do with your message
- **RAG (Retrieval-Augmented Generation)** - Semantic search across all your data
- **Auto-Vectorization** - New items instantly searchable
- **41 Categories** - Organized across all life areas
- **Natural Language** - No rigid commands, just talk naturally

### Example Usage

**Add a task:**
```
You: "buy groceries tomorrow"
Bot: ✅ Task added to Home category. Due: 2025-10-20
```

**Save a note:**
```
You: "i really love the eagles"
Bot: 📝 Note saved to Hobbies category
```

**Ask a question:**
```
You: "what are my wedding tasks"
Bot: 🔍 Found 10 results:
     ⏳ [Wedding] Book photographer
     ⏳ [Wedding] Send invitations
     ...
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
# Windows
set TELEGRAM_BOT_TOKEN=your_bot_token
set TELEGRAM_USER_ID=your_user_id
set ANTHROPIC_API_KEY=your_api_key

# Linux/Mac
export TELEGRAM_BOT_TOKEN=your_bot_token
export TELEGRAM_USER_ID=your_user_id
export ANTHROPIC_API_KEY=your_api_key
```

### 3. Initialize Database

```bash
python scripts/init_database.py
```

### 4. Vectorize Existing Data (if migrating)

```bash
python scripts/vector_store.py vectorize
```

### 5. Run the Bot

```bash
python scripts/telegram_bot.py
```

## Development Workflows

Life OS includes **automated workflows** for development, deployment, and operations. These are like DevOps agents that help YOU manage the project.

### Available Workflows

| Workflow | Purpose | Use When |
|----------|---------|----------|
| `/workflow new-session` | Session startup with health checks | Starting your coding session |
| `/workflow test-and-push` | Test, commit, push, and deploy | You've written code and want to deploy |
| `/workflow deploy` | Complete deployment automation | Ready to deploy to production |
| `/workflow end-session` | Clean shutdown & documentation | Ending your coding session |
| `/workflow new-feature` | Feature planning wizard | Planning a new feature |
| `/workflow emergency` | Production incident response | Something is broken in production |

### Quick Example

```
$ /workflow test-and-push

✅ Running tests... 15 passed
📝 Suggested commit: "feat(calendar): Add Google Calendar agent"
✅ Committed and pushed to GitHub
🚀 Deploying to Render...
✅ Deployment successful!
✅ Documentation updated

All done! 🎉
```

**See:** `.claude/workflows/README.md` for complete documentation

---

## System Architecture

### Components

1. **Telegram Bot** (`scripts/telegram_bot.py`)
   - Entry point for all user interactions
   - Handles commands: /start, /help, /stats
   - Routes messages to agentic router

2. **Agentic Router** (`scripts/router.py`)
   - Uses Claude 3.5 Haiku for intelligent routing
   - 3 tools: `add_task`, `add_note`, `ask_question`
   - Extracts categories, due dates, filters automatically
   - Auto-vectorizes new items

3. **Vector Store** (`scripts/vector_store.py`)
   - Custom JSON-based vector database
   - sentence-transformers: `all-MiniLM-L6-v2`
   - 384-dimensional embeddings
   - Cosine similarity search
   - Functions:
     - `vectorize_all_data()` - Batch vectorization
     - `search_memory()` - Semantic search
     - `add_to_vector_store()` - Auto-vectorization

4. **RAG Query** (`scripts/rag_query.py`)
   - Semantic search + filtering
   - Top 10 results by similarity
   - Filters: category, type, status
   - Simple formatted list output

5. **Tool Manifest** (`scripts/tools_manifest.py`)
   - Defines available tools and schemas
   - Used by router for Claude AI prompting

### Database Schema (SQLite)

**Categories:**
- 41 categories with parent_category support
- Examples: Home, Wedding, Princeton AI, Hobbies, etc.

**Tasks:**
```sql
id | category_id | content | due_date | completed | created_date
```

**Notes:**
```sql
id | category_id | content | created_date
```

### Technology Stack

- **Python 3.11+**
- **python-telegram-bot** - Async Telegram framework
- **anthropic** - Claude AI SDK
- **sentence-transformers** - Vector embeddings
- **torch, numpy** - ML dependencies
- **SQLite** - Local database

## Deployment

### Cloud Deployment (Railway/Render)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

**Quick Deploy to Railway:**
1. Push to GitHub
2. Connect repo in Railway dashboard
3. Add environment variables
4. Deploy automatically

**Cost Estimate:**
- Railway: $5/month (Hobby plan)
- Claude API: ~$0.36/month (20 messages/day with Haiku)
- **Total: ~$5-6/month**

### Local Development

```bash
# Run bot locally
cd life-os
python scripts/telegram_bot.py

# Test router directly
python scripts/router.py "buy milk tomorrow"

# Search vector store
python scripts/vector_store.py search "wedding planning"
```

## Categories

Your 41 categories organized across life areas:

1. **Buddy** - Dog care, health, vet
2. **Family** - Coordination, account access
3. **Home** - Maintenance, HOA, rent
4. **Bills** - 13 tracked bills
5. **Personal Projects** - Life OS, Personal Assistant, etc.
6. **Betting** - Sports betting tracking
7. **Hobbies** - 11 hobbies (Physical, Creative, Intellectual)
8. **Wedding** - May 3, 2026 planning
9. **Princeton AI Partners** - Business ventures
10. **Events** - Upcoming events, birthdays
11. **Social** - Friends visiting
12. **Generic Tasks** - Catch-all
13. **Notes** - Freeform notes
14. **Bills Reference** - Bill information

## Examples

### Natural Language Understanding

| You Type | AI Routing | Result |
|----------|-----------|--------|
| "buy groceries tomorrow" | add_task | Task → Home, Due: 2025-10-20 |
| "i love the eagles" | add_note | Note → Hobbies |
| "what are my wedding tasks" | ask_question | RAG search → 10 results |
| "remind me to call mom next week" | add_task | Task → Family, Due: Next Friday |
| "florist 1 and 2 were great" | add_note | Note → Wedding |

## RAG System Details

### How It Works

1. **Vectorization:**
   - All tasks and notes converted to 384-dim embeddings
   - Stored in `vector_store.json` (~1.08 MB for 95 items)
   - Auto-vectorizes new items immediately

2. **Semantic Search:**
   - Query converted to embedding
   - Cosine similarity calculated
   - Top 10 most relevant results returned
   - Filter by type, category, status

3. **Response:**
   - Simple formatted list (not full Claude analysis)
   - Shows tasks with status icons (⏳ pending, ✓ completed)
   - Includes due dates and categories

### Performance

- **Search time:** <1 second
- **Scales to:** 10,000+ items
- **Storage:** ~11 KB per 1,000 items
- **Model size:** ~90 MB (sentence-transformers)

## Project Structure

```
life-os/
├── scripts/
│   ├── telegram_bot.py       # Main entry point
│   ├── router.py              # Agentic routing + tool execution
│   ├── vector_store.py        # Vector database
│   ├── rag_query.py           # RAG query execution
│   └── tools_manifest.py      # Tool definitions
├── .agent/                    # Context for AI agents
│   ├── decisions/             # Decision logs
│   └── system/                # Architecture docs
├── data.db                    # SQLite database (gitignored)
├── vector_store.json          # Vector embeddings (gitignored)
├── requirements.txt           # Python dependencies
├── railway.toml               # Railway deployment config
├── Procfile                   # Process definition
├── DEPLOYMENT.md              # Deployment guide
├── PRODUCT_OVERVIEW.md        # Product vision
└── README.md                  # This file
```

## Commands

**Telegram Bot Commands:**
- `/start` - Introduction message
- `/help` - Show help information
- `/stats` - Show database statistics

**Direct Message Examples:**
- "buy milk tomorrow"
- "i love pizza"
- "what are my home tasks"
- "remind me to call john next week"

## Development

### Testing Router

```bash
# Test routing and execution
python scripts/router.py "your message here"
```

### Testing Vector Search

```bash
# Search directly
python scripts/vector_store.py search "your query"

# Vectorize all data
python scripts/vector_store.py vectorize
```

### Adding New Categories

1. Add to database:
```sql
INSERT INTO categories (name, parent_category, sort_order)
VALUES ('New Category', 'Parent Category', 99);
```

2. No code changes needed - router auto-discovers categories

## Roadmap

### Phase 2A: RAG System (COMPLETE)
- ✅ Vector store implementation
- ✅ Auto-vectorization
- ✅ Semantic search
- ✅ Agentic routing
- ✅ Cloud deployment ready

### Phase 2B: Google Calendar Integration (NEXT)
- New tool: `schedule_event`
- Event vs Task differentiation
- "schedule" keyword detection
- Two-way sync with Google Calendar

### Future Enhancements
- **Image Support** - CLIP embeddings for screenshots
- **Dashboard** - Web interface for viewing/editing
- **Mobile App** - Native mobile experience
- **Multi-user** - Share with friends/family
- **Analytics** - Completion trends and insights

## Troubleshooting

### Bot not responding?
- Check environment variables are set
- Verify bot token is valid
- Check logs for errors

### Vector search not finding items?
- Run vectorization: `python scripts/vector_store.py vectorize`
- Check vector_store.json exists
- Verify embeddings model loaded successfully

### Database errors?
- Ensure data.db exists
- Run init_database.py if needed
- Check file permissions

### Out of memory?
- sentence-transformers model is ~90MB
- Upgrade to paid cloud tier if needed

## Data Privacy

Your data is private and local:
- **Database**: `data.db` (gitignored, never committed)
- **Vector Store**: `vector_store.json` (gitignored)
- **Cloud Deployment**: Include database in first deploy only
- **Backup**: Copy data.db and vector_store.json regularly

## Cost Analysis

**Free Tier (Local):**
- $0 - Run on your own machine

**Production (Cloud):**
- Railway: $5/month
- Claude API (Haiku): $0.36/month (20 msgs/day)
- **Total: ~$5-6/month**

**Scaling:**
- 1,000 messages/month: ~$18/month
- 10,000 messages/month: ~$180/month

## Credits

Built with:
- **Claude AI** - Anthropic (routing + intelligence)
- **sentence-transformers** - HuggingFace (vector embeddings)
- **python-telegram-bot** - Telegram framework
- **SQLite** - Database
- **Railway** - Cloud deployment

**Built:** October 2025
**Phase:** 2A Production
**Status:** Deployed and operational
