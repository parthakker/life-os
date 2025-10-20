# Current Production Architecture

**Last Updated:** October 20, 2025 - 2:00 PM
**Phase:** 2A (RAG + Auto-Vectorization) - **DEPLOYING TO RENDER**

## System Flow

```
User Message (Telegram)
        ↓
telegram_bot.py - Entry point
        ↓
router.py - Agentic routing (Claude 3.5 Haiku)
        ↓
   ┌────┴────┬──────────────┐
   ↓         ↓              ↓
add_task  add_note    ask_question
   ↓         ↓              ↓
PostgreSQL PostgreSQL  vector_store.py
   ↓         ↓              ↓
auto-vectorize auto-vectorize  RAG query
   ↓         ↓              ↓
vector_store.json (immediate searchability)
```

## Core Components

### 1. Telegram Bot (`scripts/telegram_bot.py`)
- Receives user messages
- Handles /start, /help, /stats commands
- Routes all text messages to router
- **Updated:** Uses db_helper for PostgreSQL/SQLite abstraction

### 2. Agentic Router (`scripts/router.py`)
- Uses Claude 3.5 Haiku for intelligent routing
- 3 tools: `add_task`, `add_note`, `ask_question`
- Extracts category, content, due dates, filters
- Auto-vectorizes new items
- **Updated:** Uses db_helper for database operations

### 3. Database Helper (`scripts/db_helper.py`) **NEW**
- Auto-detects PostgreSQL vs SQLite
- Checks for DATABASE_URL environment variable
- PostgreSQL in production (Render)
- SQLite for local development
- Seamless switching between databases

### 4. Vector Store (`scripts/vector_store.py`)
- Custom JSON-based vector database
- sentence-transformers: `all-MiniLM-L6-v2`
- 384-dimensional embeddings
- Cosine similarity search
- Functions:
  - `vectorize_all_data()` - Batch vectorization
  - `search_memory()` - Semantic search
  - `add_to_vector_store()` - Auto-vectorization

### 5. RAG Query (`scripts/rag_query.py`)
- Semantic search + filtering
- Simple formatted list output
- Top 10 results by similarity
- Filters: category, type, status

### 6. Tool Manifest (`scripts/tools_manifest.py`)
- Defines available tools and schemas
- Used by router for Claude AI prompting

### 7. PostgreSQL Migration (`scripts/migrate_to_postgres.py`) **NEW**
- One-time migration from SQLite → PostgreSQL
- Migrates categories, tasks, notes
- Preserves all relationships and data
- Run once after initial Render deployment

## Database Schema

**PostgreSQL (Production):**
- `categories` - 41 categories with parent_category support
- `tasks` - id (SERIAL), category_id, content, due_date, completed (BOOLEAN), created_date
- `notes` - id (SERIAL), category_id, content, created_date

**SQLite (Local Development):**
- Same schema, different data types (INTEGER PRIMARY KEY vs SERIAL)

## Deployment

**Platform:** Render (render.com)
**Service Type:** Background Worker (always running)
**Service ID:** srv-d3r6u5ogjchc73bsiibg
**Plan:** $7/month (paid tier)
**Runtime:** Python 3.11+
**Database:** PostgreSQL (free tier)

**Dependencies:** See `requirements.txt`
- python-telegram-bot
- anthropic
- sentence-transformers
- torch, numpy
- **psycopg2-binary** (PostgreSQL adapter)

**Environment Variables (Set in Render):**
- `TELEGRAM_BOT_TOKEN` - Bot authentication
- `TELEGRAM_USER_ID` - Security (only you can use bot)
- `ANTHROPIC_API_KEY` - Claude AI access
- `DATABASE_URL` - PostgreSQL connection (auto-set by Render)

## Cost Breakdown

- **Render Background Worker:** $7.00/month (paid tier, always awake)
- **PostgreSQL Database:** $0.00/month (free tier, 1GB storage)
- **Claude Haiku API:** ~$0.36/month (20 messages/day)
- **Total:** ~$7.36/month for production

## MCP Integration **ACTIVE**

**MCPs Configured:**
1. ✅ **GitHub MCP** - Repository management, create repos, PRs, issues
2. ✅ **Render MCP** - Deployment logs, shell access, service monitoring **NEW**
3. ⏳ **Google Calendar MCP** - Calendar integration (disabled, for Phase 2B)

**MCP Config Location:**
`.claude/settings.local.json`

**See:** `.agent/decisions/mcp-integration.md` for setup details

## Git Configuration

**Personal Projects (parthakker):**
- SSH: `git@github.com-personal:parthakker/life-os.git`
- Uses: `~/.ssh/id_ed25519_personal`

**Business Projects (princetonaipartners):**
- SSH: `git@github.com:princetonaipartners/...`
- Uses: `~/.ssh/id_ed25519`

**Configuration:** `~/.ssh/config`

## Deployment Architecture

```
GitHub (parthakker/life-os)
        ↓ (auto-deploy on push)
Render Service (srv-d3r6u5ogjchc73bsiibg)
        ├─ Build: pip install -r requirements.txt
        ├─ Start: python scripts/telegram_bot.py
        ├─ Database: PostgreSQL (lifeos)
        └─ Files: vector_store.json (deployed with code)
```

## Data Persistence

**PostgreSQL:**
- Categories, tasks, notes
- Persists across restarts
- Free tier: 1GB storage, 1M rows

**Vector Store (JSON file):**
- vector_store.json deployed with code
- Persists on Render filesystem
- Re-vectorize if needed via shell

## Next Phases

**Phase 2B: Calendar Integration (Week 2)**
- Google Calendar MCP integration
- New tool: `schedule_event`
- Natural language date parsing
- Event vs Task differentiation
- See: `.agent/decisions/phase-2b-4-roadmap.md`

**Phase 2C: Calendar + RAG (Week 2)**
- Vectorize calendar events
- Unified search across tasks/notes/events
- Date range filtering

**Phase 3B: Intelligent Import - Images/PDFs (Week 3-4)**
- Forward vendor contracts → extract events
- Screenshot event flyers → auto-schedule
- Claude vision API for OCR

**Phase 3C: Web Link Import (Week 4)**
- Eventbrite links → extract events
- Facebook events → import automatically

**Phase 4: Advanced Features (Future)**
- Multi-calendar support
- Smart conflict detection
- Recurring event modification

**See:** `.agent/decisions/phase-2b-4-roadmap.md` for full roadmap

## Security Notes

1. **Data Files:**
   - data.db and vector_store.json temporarily exposed in GitHub for initial migration
   - Will be re-hidden in .gitignore after successful deployment
   - Local data files remain in .gitignore for future commits

2. **API Keys:**
   - All stored in Render environment variables
   - Never committed to GitHub
   - MCP tokens stored in local `.claude/settings.local.json` (gitignored)

3. **PostgreSQL:**
   - Connection string includes credentials
   - Only accessible via DATABASE_URL environment variable
   - Render manages security

## Current Status

- ✅ Code complete and pushed to GitHub
- ✅ Render service configured
- ✅ PostgreSQL database created
- ✅ Environment variables set
- ⏳ Deployment in progress (auto-deploying)
- ⏳ Migration pending (run after deployment)
- ⏳ Testing pending

**Next:** Restart Claude Code → Use Render MCP → Complete deployment
