# Production Architecture - Life OS

**Last Updated:** October 22, 2025
**Status:** Live and Operational

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                                                                   │
│  ┌──────────────┐                                                │
│  │   Telegram   │  User sends messages via mobile/desktop        │
│  │  @lifeos2_bot│                                                │
│  └──────┬───────┘                                                │
│         │                                                         │
└─────────┼─────────────────────────────────────────────────────────┘
          │
          │ HTTPS POST (webhook)
          │ + Secret Token Validation
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RENDER WEB SERVICE                             │
│              (life-os-bot-ttlr.onrender.com)                     │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  FastAPI Application (telegram_webhook_bot.py)            │  │
│  │                                                            │  │
│  │  • Webhook endpoint: /telegram-webhook                    │  │
│  │  • Health check: /health                                  │  │
│  │  • Lifespan: Registers webhook with Telegram              │  │
│  │  • Security: Validates secret token on every request      │  │
│  └───────────────────┬───────────────────────────────────────┘  │
│                      │                                           │
│                      ▼                                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Message Router (router.py)                               │  │
│  │                                                            │  │
│  │  • Claude 3.5 Sonnet AI for intent classification         │  │
│  │  • Tools: add_task, add_note, ask_question, log_health    │  │
│  │  • Smart categorization & date parsing                    │  │
│  └────┬──────────────────────────────────────────┬───────────┘  │
│       │                                           │              │
│       │ Database Operations                       │ RAG Query    │
│       ▼                                           ▼              │
│  ┌─────────────────────┐              ┌──────────────────────┐  │
│  │  Database Helper    │              │  Vector Store        │  │
│  │  (db_helper.py)     │              │  (vector_store.py)   │  │
│  │                     │              │                      │  │
│  │  • Abstraction layer│              │  • 103 embeddings    │  │
│  │  • PostgreSQL conn  │              │  • OpenAI API        │  │
│  │  • Query execution  │              │  • Cosine similarity │  │
│  └─────────┬───────────┘              └──────────┬───────────┘  │
│            │                                     │              │
│            │                                     │              │
└────────────┼─────────────────────────────────────┼──────────────┘
             │                                     │
             │ psycopg[binary]                    │ OpenAI API
             ▼                                     ▼
┌─────────────────────────────┐      ┌─────────────────────────┐
│  PostgreSQL Database        │      │  OpenAI Embeddings      │
│  (Render Free Tier)         │      │  text-embedding-3-small │
│                             │      │  384 dimensions         │
│  • Tables:                  │      └─────────────────────────┘
│    - tasks (84 rows)        │
│    - notes (21 rows)        │      ┌─────────────────────────┐
│    - categories (50 rows)   │      │  Anthropic Claude API   │
│    - sleep_logs (31 rows)   │      │  claude-3-5-sonnet      │
│    - exercise_logs (16)     │      │                         │
│    - water_logs             │      │  • Intent classification│
│    - sauna_logs             │      │  • RAG synthesis        │
│    - inbody_measurements    │      │  • Natural language     │
│                             │      └─────────────────────────┘
└─────────────────────────────┘
```

---

## Request Flow Examples

### **1. Add Task: "buy bread tomorrow"**

```
User → Telegram
  ↓
Telegram → Webhook (POST /telegram-webhook)
  ↓ [Secret token validated]
Update → PTB Application
  ↓
Message Handler → router.route_message("buy bread tomorrow")
  ↓
Claude AI Analysis:
  - Tool: add_task
  - Category: General (inferred)
  - Content: "Buy bread"
  - Due Date: 2025-10-23 (parsed "tomorrow")
  ↓
router.execute_add_task(category="General", content="Buy bread", due_date="2025-10-23")
  ↓
db_helper.execute_insert(
  "INSERT INTO tasks (content, category_id, due_date, completed) VALUES (?, ?, ?, ?)",
  ("Buy bread", 25, "2025-10-23", False)
)
  ↓
PostgreSQL: Task ID 83 created
  ↓
Response: "✓ Task added to General\nContent: Buy bread\nDue: 2025-10-23\nID: 83"
  ↓
Telegram → User (message appears in chat)
```

**Total Time:** ~1.5 seconds

---

### **2. RAG Query: "what tasks do I have?"**

```
User → Telegram → Webhook
  ↓
Message Handler → router.route_message("what tasks do I have?")
  ↓
Claude AI Analysis:
  - Tool: ask_question
  - Query Type: all
  - Filters: None
  ↓
router.execute_ask_question(query="what tasks do I have?")
  ↓
rag_query.execute_rag_query("what tasks do I have?")
  ↓
vector_store.search_memory("what tasks do I have?", n_results=5)
  ↓
OpenAI API: Generate query embedding (384 dimensions)
  ↓
Cosine Similarity Calculation:
  - Compare query embedding vs. all 103 stored embeddings
  - Rank by similarity score
  ↓
Top 5 Results (example):
  1. [General] Buy bread (similarity: 0.842)
  2. [Work] Complete project proposal (similarity: 0.798)
  3. [Home] Fix kitchen sink (similarity: 0.756)
  4. [Health] Schedule doctor appointment (similarity: 0.721)
  5. [General] Call Mom (similarity: 0.689)
  ↓
Claude AI Synthesis:
  - Input: Query + Top 5 results
  - Output: Natural language summary
  ↓
Response: "You have 5 active tasks:
  1. Buy bread (due tomorrow)
  2. Complete project proposal (work-related)
  3. Fix kitchen sink (home maintenance)
  4. Schedule doctor appointment
  5. Call Mom this weekend"
  ↓
Telegram → User
```

**Total Time:** ~4 seconds

---

### **3. Health Logging: "I slept 8 hours last night"**

```
User → Telegram → Webhook
  ↓
Message Handler → router.route_message("I slept 8 hours last night")
  ↓
Claude AI Analysis:
  - Tool: log_sleep
  - Hours: 8.0
  - Date: 2025-10-22 (inferred "last night")
  - Notes: None
  ↓
router.execute_log_sleep(hours=8.0, date="2025-10-22", notes=None)
  ↓
db_helper.execute_insert(
  "INSERT INTO sleep_logs (date, hours, notes) VALUES (?, ?, ?)",
  ("2025-10-22", 8.0, None)
)
  ↓
PostgreSQL: Sleep log created
  ↓
Response: "✓ Logged 8.0 hours of sleep for 2025-10-22"
  ↓
Telegram → User
```

**Total Time:** ~1.2 seconds

---

## Database Schema

### **tasks**
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    due_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE
);
```

### **notes**
```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **categories**
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    parent_id INTEGER REFERENCES categories(id)
);
```

### **sleep_logs**
```sql
CREATE TABLE sleep_logs (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    hours REAL NOT NULL,
    notes TEXT
);
```

### **exercise_logs**
```sql
CREATE TABLE exercise_logs (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    activity_type TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    notes TEXT
);
```

---

## Environment Variables

### **Required (Render Dashboard)**
```bash
TELEGRAM_BOT_TOKEN=7972961951:AAH4hUa5vv884awuR3_B2d5b1p5KTqR7IK0
TELEGRAM_USER_ID=6573778096
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-5FwgONXEnbYSO3fUSMd1y4cIXurNKKTVqtI__...
WEBHOOK_SECRET_TOKEN=<auto-generated by Render>
DATABASE_URL=<auto-linked to life-os-db>
```

### **Auto-Provided by Render**
```bash
PORT=10000  # Render assigns this
RENDER_EXTERNAL_URL=https://life-os-bot-ttlr.onrender.com
```

---

## Deployment Commands

### **Build Command** (render.yaml)
```bash
pip install -r requirements.txt
```

### **Start Command** (render.yaml)
```bash
gunicorn scripts.telegram_webhook_bot:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT
```

### **Health Check**
```bash
curl https://life-os-bot-ttlr.onrender.com/health
# Response: {"status": "healthy", "mode": "webhook"}
```

---

## Vector Store Details

### **File Location**
```
/opt/render/project/src/vector_store.json
```

### **Structure**
```json
{
  "metadata": {
    "created_at": "2025-10-22T17:40:XX",
    "model": "text-embedding-3-small",
    "provider": "openai",
    "dimensions": 384,
    "total_items": 103
  },
  "items": [
    {
      "id": "task_83",
      "type": "task",
      "category": "General",
      "content": "Buy bread",
      "due_date": "2025-10-23",
      "created_date": "2025-10-22T17:26:55",
      "completed": false,
      "embedding": [0.123, -0.456, 0.789, ...(384 floats)]
    },
    {
      "id": "note_21",
      "type": "note",
      "category": "Tech",
      "content": "YouTube Shorts AI video link: https://...",
      "created_date": "2025-10-19T12:34:56",
      "embedding": [-0.234, 0.567, -0.890, ...(384 floats)]
    }
  ]
}
```

### **Build Command** (via Render Shell)
```bash
python -c "from scripts.vector_store import vectorize_all_data;vectorize_all_data(force=True)"
```

**Duration:** ~60 seconds for 103 items

---

## Security

### **1. Webhook Secret Token**
- Generated by Render during service creation
- Sent in `X-Telegram-Bot-Api-Secret-Token` header
- Validated on every webhook request
- Prevents unauthorized updates

### **2. User Authorization**
- Only `TELEGRAM_USER_ID=6573778096` can interact
- Checked in every message handler
- Others receive "Sorry, you're not authorized"

### **3. Environment Variables**
- Stored in Render Dashboard (encrypted at rest)
- Never committed to Git
- Injected at runtime

### **4. Database Access**
- TLS encrypted connections
- User `lifeos_user` with limited permissions
- No public access (internal to Render)

---

## Monitoring & Logs

### **Render Dashboard**
- Live logs: https://dashboard.render.com/web/srv-d3sgmsqli9vc73fqkgl0/logs
- Metrics: CPU, Memory, Request count
- Deploy history

### **Log Levels**
```python
print("[OK] ...")      # Success
print("[ERROR] ...")   # Failures
print("[WARNING] ...")  # Non-critical issues
print("[RAG] ...")     # RAG-specific logs
```

### **Health Check Endpoint**
```bash
GET /health
Response: {"status": "healthy", "mode": "webhook"}
```

---

## Scaling Considerations

### **Current Limits (Free Tier)**
- **Web Service:** 512 MB RAM, 0.5 CPU
- **Database:** 1 GB storage, 100 connections
- **Requests:** Unlimited

### **If Scaling Needed**
1. **Upgrade to Starter Plan** ($7/month)
   - 2 GB RAM, 1 CPU
   - Auto-sleep disabled
   - Background workers

2. **Optimize Vector Store**
   - Use PostgreSQL pgvector extension
   - Store embeddings in database
   - Eliminate JSON file

3. **Add Redis Cache**
   - Cache Claude AI responses
   - Cache vector search results
   - Reduce API costs

4. **Queue System**
   - Celery + Redis
   - Handle long-running RAG queries
   - Prevent timeout errors

---

**Last Updated:** October 22, 2025
**Architecture Version:** 1.0 (Production)
**Status:** Stable and Operational
