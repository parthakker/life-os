# Current Production Architecture

**Last Updated:** October 19, 2025
**Phase:** 2A (RAG + Auto-Vectorization)

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
database  database    vector_store.py
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

### 2. Agentic Router (`scripts/router.py`)
- Uses Claude 3.5 Haiku for intelligent routing
- 3 tools: `add_task`, `add_note`, `ask_question`
- Extracts category, content, due dates, filters
- Auto-vectorizes new items

### 3. Vector Store (`scripts/vector_store.py`)
- Custom JSON-based vector database
- sentence-transformers: `all-MiniLM-L6-v2`
- 384-dimensional embeddings
- Cosine similarity search
- Functions:
  - `vectorize_all_data()` - One-time vectorization
  - `search_memory()` - Semantic search
  - `add_to_vector_store()` - Auto-vectorization

### 4. RAG Query (`scripts/rag_query.py`)
- Semantic search + filtering
- Simple formatted list output
- Top 10 results by similarity
- Filters: category, type, status

### 5. Tool Manifest (`scripts/tools_manifest.py`)
- Defines available tools and schemas
- Used by router for Claude AI prompting

## Database Schema

**SQLite (data.db):**
- `categories` - 41 categories with parent_category support
- `tasks` - id, category_id, content, due_date, completed, created_date
- `notes` - id, category_id, content, created_date

## Deployment

**Platform:** Railway (or Render)
**Runtime:** Python 3.11+
**Dependencies:** See `requirements.txt`
- python-telegram-bot
- anthropic
- sentence-transformers
- torch, numpy

**Environment Variables:**
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_USER_ID`
- `ANTHROPIC_API_KEY`

## Cost Estimates

- **Railway:** $5/month (Hobby plan)
- **Claude API:** ~$0.36/month (20 messages/day with Haiku)
- **Total:** ~$5-6/month for production

## Next Phase (2B)

**Google Calendar Integration:**
- New tool: `schedule_event`
- Event vs Task differentiation
- "schedule" keyword detection
- Two-way sync with Google Calendar

**Image Support (Future):**
- CLIP embeddings for images
- Screenshot categorization
- Multimodal vector search
