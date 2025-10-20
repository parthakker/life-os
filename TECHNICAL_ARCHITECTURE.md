# Life OS - Technical Architecture

**Deep-dive into the RAG-based personal memory system**

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Core Architecture](#core-architecture)
3. [RAG Implementation](#rag-implementation)
4. [Database Design](#database-design)
5. [Agentic Router](#agentic-router)
6. [Vector Store](#vector-store)
7. [Deployment Architecture](#deployment-architecture)
8. [Code Structure](#code-structure)
9. [Phase Evolution](#phase-evolution)
10. [Performance & Scalability](#performance--scalability)

---

## System Overview

Life OS is a **RAG-powered personal memory system** built on:
- **Retrieval-Augmented Generation (RAG)** for semantic search
- **Agentic routing** with Claude 3.5 Haiku for intelligent tool selection
- **Auto-vectorization** for instant searchability
- **PostgreSQL + JSON vector store** for production data persistence

### Technology Stack

**Backend:**
- Python 3.11+
- python-telegram-bot (async framework)
- anthropic SDK (Claude 3.5 Haiku)
- sentence-transformers (all-MiniLM-L6-v2)
- torch, numpy (ML dependencies)
- psycopg2-binary (PostgreSQL adapter)

**Database:**
- PostgreSQL (production)
- SQLite (local development)
- JSON vector store (vector_store.json)

**Deployment:**
- Render.com (Background Worker, $7/month)
- PostgreSQL free tier (1GB storage)
- GitHub auto-deploy on push

**APIs:**
- Telegram Bot API
- Anthropic Claude API
- Google Calendar API (Phase 2B)

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User (Telegram)                           │
│                 "buy milk tomorrow"                          │
│           "what was my bench press last week"                │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Telegram Bot (telegram_bot.py)                  │
│              - Receives messages                             │
│              - Handles /start, /help, /stats                 │
│              - Routes to agentic router                      │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│           Agentic Router (router.py)                         │
│           Claude 3.5 Haiku analyzes message                  │
│           Selects tool: add_task | add_note | ask_question   │
└────────────┬───────────────┬──────────────┬─────────────────┘
             ↓               ↓              ↓
    ┌────────────┐  ┌────────────┐  ┌──────────────────┐
    │  add_task  │  │  add_note  │  │  ask_question    │
    └─────┬──────┘  └─────┬──────┘  └────────┬─────────┘
          ↓               ↓                   ↓
    ┌─────────────────────────────────────────────────┐
    │         Database Helper (db_helper.py)          │
    │    Auto-detects PostgreSQL vs SQLite            │
    └─────┬───────────────────────────────────┬───────┘
          ↓                                   ↓
    ┌──────────────┐                   ┌─────────────────┐
    │  PostgreSQL  │                   │  Vector Store   │
    │  (Production)│                   │  (vector_store  │
    │              │                   │   .py)          │
    │  Categories  │                   │                 │
    │  Tasks       │                   │  Embeddings     │
    │  Notes       │                   │  (384-dim)      │
    │  Events      │                   │                 │
    └──────┬───────┘                   │  Cosine         │
           ↓                           │  Similarity     │
    Auto-vectorize                     └────────┬────────┘
           ↓                                    ↓
    ┌──────────────────────────────────────────────┐
    │      vector_store.json                       │
    │      {id, type, category, content,           │
    │       embedding: [384 floats]}               │
    └──────────────────────────────────────────────┘
```

---

## RAG Implementation

### What is RAG?

**Retrieval-Augmented Generation (RAG)** combines:
1. **Retrieval**: Find relevant documents using semantic search
2. **Augmentation**: Provide context to LLM
3. **Generation**: LLM generates answer using retrieved context

### Life OS RAG Architecture

```python
# Simplified flow:

# 1. User asks question
query = "what was my bench press info from last week"

# 2. Convert query to 384-dim embedding
query_embedding = model.encode(query)
# → [0.123, -0.456, 0.789, ..., 0.234]  # 384 numbers

# 3. Load all stored embeddings
vector_store = load_vector_store()
# → [{id: 1, embedding: [...], content: "bench press 3x10 at 135"}, ...]

# 4. Calculate cosine similarity for each item
similarities = []
for item in vector_store:
    similarity = cosine_similarity(query_embedding, item['embedding'])
    similarities.append((item, similarity))

# 5. Sort by similarity, return top 10
results = sorted(similarities, key=lambda x: x[1], reverse=True)[:10]

# 6. Format and return
return format_results(results)
```

### Vector Embeddings

**Model:** `all-MiniLM-L6-v2` (sentence-transformers)
- **Dimensions:** 384
- **Size:** ~90MB
- **Speed:** ~50ms per embedding
- **Quality:** Excellent for semantic similarity

**Example Embedding:**
```python
text = "bench press 3 sets 10 reps at 135 lbs"
embedding = model.encode(text)
# → array([0.123, -0.456, 0.789, ..., 0.234], dtype=float32)
# → Shape: (384,)
```

### Cosine Similarity

Measures angle between two vectors (0 = different, 1 = identical):

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

# Example:
query = "bench press last week"
item1 = "bench press 3x10 at 135 lbs"  # High similarity
item2 = "buy groceries tomorrow"        # Low similarity

similarity1 = cosine_similarity(encode(query), encode(item1))
# → 0.87 (very similar)

similarity2 = cosine_similarity(encode(query), encode(item2))
# → 0.12 (not similar)
```

### Auto-Vectorization

Every new task/note is automatically vectorized on creation:

```python
# In execute_add_task() and execute_add_note():
def execute_add_task(category, content, due_date):
    # 1. Insert into database
    task_id = insert_task(category, content, due_date)

    # 2. Auto-vectorize
    add_to_vector_store(
        item_id=task_id,
        item_type="task",
        category=category,
        content=content,
        due_date=due_date
    )

    return task_id
```

**Result:** New items are instantly searchable, no manual re-indexing.

---

## Database Design

### PostgreSQL Schema (Production)

```sql
-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    parent_category TEXT,
    sort_order INTEGER
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    content TEXT NOT NULL,
    due_date DATE,
    completed BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notes table
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    content TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Future: Events table (Phase 2B)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    title TEXT NOT NULL,
    description TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    location TEXT,
    calendar_id TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### SQLite Schema (Local Development)

Identical structure, but uses INTEGER PRIMARY KEY instead of SERIAL:

```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent_category TEXT,
    sort_order INTEGER
);
-- ... same for tasks, notes
```

### Database Abstraction (db_helper.py)

**Auto-detects PostgreSQL vs SQLite:**

```python
import os
import sqlite3
import psycopg2

def get_db_connection():
    """Auto-detect and return appropriate database connection"""
    database_url = os.getenv('DATABASE_URL')

    if database_url:
        # Production: PostgreSQL
        return psycopg2.connect(database_url)
    else:
        # Local: SQLite
        return sqlite3.connect('data.db')

def execute_query(query, params=None):
    """Execute query on appropriate database"""
    conn = get_db_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    conn.commit()
    conn.close()

    return result
```

### Vector Store Schema (JSON)

Stored in `vector_store.json`:

```json
{
  "items": [
    {
      "id": 1,
      "type": "task",
      "category": "Gym",
      "content": "bench press 3 sets 10 reps at 135 lbs",
      "due_date": "2025-10-20",
      "completed": false,
      "embedding": [0.123, -0.456, 0.789, ..., 0.234],
      "created_date": "2025-10-20T10:30:00"
    },
    {
      "id": 2,
      "type": "note",
      "category": "Wedding",
      "content": "florist 1 and 2 were great",
      "embedding": [0.345, 0.678, -0.234, ..., 0.567],
      "created_date": "2025-10-19T14:20:00"
    }
  ],
  "metadata": {
    "total_items": 95,
    "last_updated": "2025-10-20T15:45:00",
    "model": "all-MiniLM-L6-v2",
    "dimensions": 384
  }
}
```

**Size:** ~11KB per 1,000 items
**Scalability:** Works well up to 10,000 items (~110KB)

---

## Agentic Router

### What is Agentic Routing?

Instead of if/else logic, an **AI agent** (Claude 3.5 Haiku) decides which tool to use based on user intent.

### Router Architecture

```python
# router.py (simplified)

def route_message(user_message):
    """
    Send message to Claude with tool definitions.
    Claude chooses tool and extracts parameters.
    """

    # 1. Load tools manifest
    tools = load_tools_manifest()
    # → [add_task, add_note, ask_question]

    # 2. Create prompt for Claude
    prompt = f"""
    User message: {user_message}

    Available tools:
    - add_task: Create a task with due date
    - add_note: Save a note or observation
    - ask_question: Search memory with RAG

    Choose the appropriate tool and extract parameters.
    """

    # 3. Call Claude API
    response = anthropic_client.messages.create(
        model="claude-3-5-haiku-20241022",
        messages=[{"role": "user", "content": prompt}],
        tools=tools
    )

    # 4. Extract tool choice and parameters
    tool_name = response.tool_use.name
    tool_params = response.tool_use.parameters

    # 5. Execute tool
    if tool_name == "add_task":
        return execute_add_task(**tool_params)
    elif tool_name == "add_note":
        return execute_add_note(**tool_params)
    elif tool_name == "ask_question":
        return execute_ask_question(**tool_params)
```

### Tool Definitions (tools_manifest.py)

```python
TOOLS = [
    {
        "name": "add_task",
        "description": "Create a task with optional due date",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category name from 41 categories"
                },
                "content": {
                    "type": "string",
                    "description": "Task content"
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date (YYYY-MM-DD) or null"
                }
            },
            "required": ["category", "content"]
        }
    },
    {
        "name": "add_note",
        "description": "Save a note or observation",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Category name"
                },
                "content": {
                    "type": "string",
                    "description": "Note content"
                }
            },
            "required": ["category", "content"]
        }
    },
    {
        "name": "ask_question",
        "description": "Search memory using RAG",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "filters": {
                    "type": "object",
                    "description": "Optional filters (category, type, status)"
                }
            },
            "required": ["query"]
        }
    }
]
```

### Tool Execution Flow

```
User: "buy milk tomorrow"
       ↓
Router sends to Claude:
  Message: "buy milk tomorrow"
  Tools: [add_task, add_note, ask_question]
       ↓
Claude analyzes and responds:
  {
    "tool_name": "add_task",
    "parameters": {
      "category": "Home",
      "content": "buy milk tomorrow",
      "due_date": "2025-10-21"
    }
  }
       ↓
Router calls execute_add_task():
  - Inserts into PostgreSQL
  - Auto-vectorizes
  - Returns confirmation
       ↓
Bot responds: "✓ Task added to Home. Due: 2025-10-21"
```

### Why Claude 3.5 Haiku?

**Performance:**
- 10x cheaper than Sonnet ($0.25 vs $3 per million input tokens)
- Fast enough for real-time responses (~2 seconds)
- Sufficient accuracy for categorization and routing

**Cost Calculation:**
```
Average message: ~500 tokens input + 100 tokens output
Cost per message: ~$0.0006
20 messages/day × 30 days = 600 messages/month
Monthly cost: 600 × $0.0006 = $0.36
```

---

## Vector Store

### Implementation (vector_store.py)

**Key Functions:**

```python
from sentence_transformers import SentenceTransformer
import numpy as np
import json

# Load model once at startup
model = SentenceTransformer('all-MiniLM-L6-v2')

def add_to_vector_store(item_id, item_type, category, content, **kwargs):
    """Add item to vector store with embedding"""

    # 1. Generate embedding
    embedding = model.encode(content).tolist()

    # 2. Create item object
    item = {
        "id": item_id,
        "type": item_type,
        "category": category,
        "content": content,
        "embedding": embedding,
        "created_date": datetime.now().isoformat(),
        **kwargs
    }

    # 3. Load existing vector store
    vector_store = load_vector_store()

    # 4. Append new item
    vector_store["items"].append(item)
    vector_store["metadata"]["total_items"] += 1
    vector_store["metadata"]["last_updated"] = datetime.now().isoformat()

    # 5. Save back to disk
    save_vector_store(vector_store)

def search_memory(query, filters=None, top_k=10):
    """Search vector store using cosine similarity"""

    # 1. Encode query
    query_embedding = model.encode(query)

    # 2. Load vector store
    vector_store = load_vector_store()

    # 3. Calculate similarities
    results = []
    for item in vector_store["items"]:
        # Apply filters
        if filters:
            if "type" in filters and item["type"] != filters["type"]:
                continue
            if "category" in filters and item["category"] != filters["category"]:
                continue

        # Calculate similarity
        item_embedding = np.array(item["embedding"])
        similarity = cosine_similarity(query_embedding, item_embedding)

        results.append((item, similarity))

    # 4. Sort by similarity
    results.sort(key=lambda x: x[1], reverse=True)

    # 5. Return top K
    return results[:top_k]

def vectorize_all_data():
    """Batch vectorize all tasks and notes (one-time migration)"""

    # 1. Get all tasks
    tasks = get_all_tasks()
    for task in tasks:
        add_to_vector_store(
            item_id=task['id'],
            item_type='task',
            category=task['category'],
            content=task['content'],
            due_date=task['due_date'],
            completed=task['completed']
        )

    # 2. Get all notes
    notes = get_all_notes()
    for note in notes:
        add_to_vector_store(
            item_id=note['id'],
            item_type='note',
            category=note['category'],
            content=note['content']
        )
```

### Performance Optimization

**1. Model Caching:**
```python
# Load model once at module import (not per request)
model = SentenceTransformer('all-MiniLM-L6-v2')
```

**2. Batch Embeddings:**
```python
# Vectorize multiple items at once
contents = [item['content'] for item in items]
embeddings = model.encode(contents, batch_size=32)
```

**3. NumPy Vectorization:**
```python
# Use NumPy for fast similarity calculations
similarities = np.dot(query_embedding, embeddings.T)
```

### Scaling Considerations

**Current (JSON):**
- ✅ 10,000 items: ~110KB, <1 second search
- ✅ Simple, portable, version-controllable

**Future (pgvector):**
- When >10,000 items or >10MB vector store
- PostgreSQL extension for vector similarity
- HNSW index for <100ms search at 1M+ items

---

## Deployment Architecture

### Render Configuration

**Service Type:** Background Worker
**Plan:** Starter ($7/month, always-on)
**Region:** Oregon (us-west)
**Runtime:** Python 3.11

**render.yaml:**
```yaml
services:
  - type: background
    name: life-os
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python scripts/telegram_bot.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: TELEGRAM_USER_ID
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: lifeos
          property: connectionString
```

**requirements.txt:**
```
python-telegram-bot==20.6
anthropic==0.39.0
sentence-transformers==2.2.2
torch==2.1.0
numpy==1.24.3
psycopg2-binary==2.9.9
```

### Environment Variables

```bash
# Telegram
TELEGRAM_BOT_TOKEN=8479331593:AAEdxa4w7pWeATybTnC_bXZT9J4QrpUx3n4
TELEGRAM_USER_ID=6573778096

# Claude AI
ANTHROPIC_API_KEY=sk-ant-api03-Ove-FFX8...

# Database (auto-set by Render)
DATABASE_URL=postgresql://lifeos_user:nS2SUCw1PRQ4...@dpg-.../lifeos
```

### Deployment Flow

```
Local Development
      ↓
git commit & push
      ↓
GitHub (parthakker/life-os)
      ↓
Render auto-detects push
      ↓
Build Process:
  1. pip install -r requirements.txt
  2. Download sentence-transformers model (~90MB)
  3. Prepare runtime environment
      ↓
Start Process:
  1. python scripts/telegram_bot.py
  2. Load vector store
  3. Load embedding model
  4. Connect to PostgreSQL
  5. Start Telegram bot polling
      ↓
Production (24/7)
```

### Data Persistence

**PostgreSQL:**
- Managed by Render
- Automatic backups (free tier: 7 days)
- Connection pooling
- Encrypted at rest

**vector_store.json:**
- Deployed with code (in repository)
- Persists on Render filesystem
- Re-vectorize if needed via shell

---

## Code Structure

```
life-os/
├── scripts/
│   ├── telegram_bot.py          # Main entry point, message handling
│   ├── router.py                 # Agentic routing + tool execution
│   ├── vector_store.py           # Vector embeddings + search
│   ├── rag_query.py              # RAG query execution
│   ├── tools_manifest.py         # Tool definitions for Claude
│   ├── db_helper.py              # Database abstraction
│   ├── migrate_to_postgres.py    # One-time migration script
│   └── init_database.py          # Database initialization
│
├── .agent/
│   ├── decisions/                # Architecture decision records
│   │   ├── phase-2a-rag-system.md
│   │   ├── phase-2b-4-roadmap.md
│   │   └── mcp-integration.md
│   ├── system/                   # System documentation
│   │   ├── current-architecture.md
│   │   ├── category-tree.md
│   │   └── organization-rules.md
│   └── logs/                     # Session logs
│       └── session-summary-2025-10-19.md
│
├── data.db                       # SQLite (local dev, gitignored)
├── vector_store.json             # Vector embeddings (gitignored in prod)
│
├── requirements.txt              # Python dependencies
├── render.yaml                   # Render deployment config
├── Procfile                      # Process definition (legacy)
│
├── README.md                     # Quick start guide
├── PRODUCT_OVERVIEW.md           # User-facing product doc
├── TECHNICAL_ARCHITECTURE.md     # This file
├── DEPLOYMENT.md                 # Deployment guide
├── MCP_SETUP_GUIDE.md            # MCP integration guide
└── QUICK_START_NEXT_SESSION.md   # Session handoff doc
```

### Key File Details

**telegram_bot.py:**
- Entry point, runs 24/7
- Handles /start, /help, /stats commands
- Routes text messages to router.py
- Future: handle_photo(), handle_document() for Phase 3B

**router.py:**
- Calls Claude API with tools manifest
- Executes tool based on Claude's choice
- Handles database operations via db_helper
- Auto-vectorizes new items

**vector_store.py:**
- Loads sentence-transformers model
- add_to_vector_store(): Auto-vectorization
- search_memory(): Semantic search
- vectorize_all_data(): Batch migration

**db_helper.py:**
- get_db_connection(): Auto-detect PostgreSQL vs SQLite
- execute_query(): Database abstraction layer
- Seamless local → production switching

---

## Phase Evolution

### Phase 2A (Complete)

**Delivered:**
- Agentic router with Claude 3.5 Haiku
- Custom JSON vector store
- Auto-vectorization on insert
- 3 tools: add_task, add_note, ask_question
- PostgreSQL migration complete
- Deployed to Render

**Architecture:**
```
Telegram → Router → Tools → Database/Vector Store
```

### Phase 2B (Calendar Integration)

**New Components:**
- Google Calendar MCP
- schedule_event tool
- Calendar read/write operations

**Updated Architecture:**
```
Telegram → Router → Tools → Database/Vector Store/Calendar
                      ↓
        add_task | add_note | ask_question | schedule_event
```

**Implementation:**
```python
# tools_manifest.py - Add new tool
{
    "name": "schedule_event",
    "description": "Create calendar event",
    "input_schema": {
        "properties": {
            "title": {"type": "string"},
            "datetime": {"type": "string"},
            "duration_minutes": {"type": "integer"}
        }
    }
}

# router.py - Add execution function
def execute_schedule_event(title, datetime, duration_minutes=60):
    # Parse natural language date
    event_time = parse_datetime(datetime)

    # Call Google Calendar API via MCP
    event_id = create_calendar_event(
        title=title,
        start=event_time,
        duration=duration_minutes
    )

    # Auto-vectorize event
    add_to_vector_store(
        item_id=event_id,
        item_type="event",
        category=determine_category(title),
        content=title,
        event_time=event_time
    )

    return event_id
```

### Phase 2C (Calendar + RAG)

**Enhancements:**
- Vectorize calendar events
- Unified search across tasks/notes/events
- Date range filtering

**Vector Store Update:**
```json
{
  "id": "cal_123",
  "type": "event",
  "category": "Wedding",
  "content": "Final venue walkthrough",
  "event_time": "2026-03-15T14:00:00",
  "duration": 120,
  "embedding": [...]
}
```

### Phase 3B (Intelligent Import)

**New Components:**
- Image/PDF handlers in telegram_bot.py
- Claude Vision API integration
- Data extraction pipeline

**Flow:**
```
User forwards image/PDF
       ↓
telegram_bot.py detects file
       ↓
Download file
       ↓
Send to Claude Vision API
       ↓
Extract structured data
       ↓
Confirmation flow with user
       ↓
User confirms → Create task/note/event
       ↓
Auto-vectorize
```

**Implementation:**
```python
# telegram_bot.py
async def handle_photo(update: Update, context):
    # 1. Download image
    photo = await update.message.photo[-1].get_file()
    image_path = await photo.download_to_drive()

    # 2. Extract data using Claude Vision
    extracted_data = extract_from_image(image_path)
    # → {"type": "workout", "exercise": "bench press",
    #     "sets": 3, "reps": 10, "weight": 135}

    # 3. Confirm with user
    await update.message.reply_text(
        f"Found: {extracted_data['exercise']} "
        f"{extracted_data['sets']}x{extracted_data['reps']} "
        f"at {extracted_data['weight']} lbs. Correct? (yes/no)"
    )

    # 4. If confirmed → add_note with structured data

# event_extractor.py (new file)
def extract_from_image(image_path):
    """Use Claude Vision to extract data from image"""

    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()

    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Vision capable
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "Extract structured data from this image. "
                            "Look for: workout info, betting slips, "
                            "body composition scans, receipts, etc."
                }
            ]
        }]
    )

    return parse_extracted_data(response.content)
```

---

## Performance & Scalability

### Current Performance (Phase 2A)

**Response Times:**
- Message → Bot response: 2-3 seconds
- RAG search: <1 second
- Auto-vectorization: <50ms

**Throughput:**
- ~20 messages/day (current usage)
- System can handle 100+ messages/minute

**Resource Usage:**
- RAM: ~300MB (sentence-transformers model)
- Disk: ~150MB (model + dependencies)
- PostgreSQL: <10MB data

### Scalability Limits

**Current Architecture:**

| Component | Current | Max Capacity | Bottleneck |
|-----------|---------|--------------|------------|
| Vector Store (JSON) | 95 items | 10,000 items | File I/O |
| Search Latency | <1s | ~2s at 10k | Linear scan |
| PostgreSQL (Free) | <10MB | 1GB | Render limit |
| Render (Starter) | 300MB RAM | 512MB | Model size |

**When to Scale:**

1. **>10,000 items** → Migrate to pgvector
   ```sql
   CREATE EXTENSION vector;

   CREATE TABLE embeddings (
       id SERIAL PRIMARY KEY,
       item_id INTEGER,
       embedding vector(384),
       created_date TIMESTAMP
   );

   CREATE INDEX ON embeddings
   USING ivfflat (embedding vector_cosine_ops);
   ```

2. **>1GB database** → Upgrade PostgreSQL to paid tier ($7/month)

3. **>512MB RAM** → Upgrade Render to Standard ($25/month, 2GB RAM)

### Future Optimizations

**Phase 3+ Considerations:**

1. **Caching:**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def search_memory(query, filters_hash):
       # Cache frequent queries
   ```

2. **Async Processing:**
   ```python
   import asyncio

   async def vectorize_async(items):
       # Parallelize embeddings generation
       embeddings = await asyncio.gather(
           *[model.encode_async(item) for item in items]
       )
   ```

3. **Database Indexing:**
   ```sql
   CREATE INDEX idx_tasks_category ON tasks(category_id);
   CREATE INDEX idx_tasks_due_date ON tasks(due_date);
   CREATE INDEX idx_notes_created ON notes(created_date);
   ```

4. **Connection Pooling:**
   ```python
   from psycopg2 import pool

   connection_pool = pool.SimpleConnectionPool(
       minconn=1,
       maxconn=10,
       dsn=DATABASE_URL
   )
   ```

---

## Appendix: Key Algorithms

### A. Cosine Similarity (Detailed)

```python
def cosine_similarity_detailed(vec1, vec2):
    """
    Calculate cosine similarity between two vectors

    Formula: cos(θ) = (A · B) / (||A|| × ||B||)

    Where:
    - A · B = dot product
    - ||A|| = magnitude of A
    - ||B|| = magnitude of B
    """

    # Step 1: Dot product
    # Multiply corresponding elements and sum
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # Step 2: Magnitude of vec1
    # sqrt(sum of squares)
    magnitude1 = np.sqrt(sum(a ** 2 for a in vec1))

    # Step 3: Magnitude of vec2
    magnitude2 = np.sqrt(sum(b ** 2 for b in vec2))

    # Step 4: Cosine similarity
    similarity = dot_product / (magnitude1 * magnitude2)

    return similarity
```

### B. Natural Language Date Parsing

```python
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import datetime

def parse_natural_date(date_string):
    """Parse natural language dates"""

    today = datetime.date.today()

    # Handle relative dates
    if "tomorrow" in date_string.lower():
        return today + datetime.timedelta(days=1)

    elif "next week" in date_string.lower():
        return today + datetime.timedelta(days=7)

    elif "next month" in date_string.lower():
        return today + relativedelta(months=1)

    # Handle specific dates
    try:
        parsed = parse(date_string, fuzzy=True)
        return parsed.date()
    except:
        return None
```

---

**Document Version:** 1.0
**Last Updated:** October 20, 2025
**Phase:** 2A Production
**Status:** Deployed to Render

*For user-facing documentation, see PRODUCT_OVERVIEW.md*
*For deployment instructions, see DEPLOYMENT.md*
