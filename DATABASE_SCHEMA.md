# Life OS - Complete Database Schema Documentation

**Last Updated:** October 21, 2025
**Database Type:** Dual support - SQLite (local) / PostgreSQL (production)
**Current Version:** Phase 2C - Health Tracking Complete

---

## Table of Contents

1. [Overview](#overview)
2. [Schema Evolution](#schema-evolution)
3. [Complete Table Definitions](#complete-table-definitions)
4. [Relationships & Hierarchy](#relationships--hierarchy)
5. [Migration History](#migration-history)
6. [API Endpoints](#api-endpoints)
7. [Design Decisions](#design-decisions)

---

## Overview

The Life OS database consists of **8 tables** organized into two main systems:

### Core System (3 tables)
- `categories` - Hierarchical organization system with AI categorization
- `tasks` - To-do items linked to categories
- `notes` - Free-form notes linked to categories

### Health Tracking System (5 tables)
- `sleep_logs` - Daily sleep tracking
- `water_logs` - Water intake throughout the day
- `exercise_logs` - Exercise activities and duration
- `sauna_logs` - Sauna session tracking
- `inbody_measurements` - Body composition measurements

---

## Schema Evolution

### Phase 1: Flat Structure (Original)
**Problem:** Categories were flat strings with redundant naming
```
"Wedding"
"Wedding - Vendors"
"Wedding - Vendors - Grove"
"Wedding - Vendors - Pasha"
"Wedding - Bachelor Party"
```

**Issues:**
- No parent-child relationships
- Redundant category names
- Hard to display as hierarchical UI
- AI had no context about category purpose

### Phase 2A: Hierarchy Migration
**Solution:** Added `parent_id` column for tree structure
```
Wedding (parent_id: NULL)
├── Vendors (parent_id: Wedding.id)
│   ├── Grove (parent_id: Vendors.id)
│   └── Pasha (parent_id: Vendors.id)
└── Bachelor Party (parent_id: Wedding.id)
```

**Benefits:**
- Clean folder-like UI structure
- Efficient queries for category trees
- Subcategories properly organized
- Database enforces referential integrity

### Phase 2B: AI Categorization
**Solution:** Added `description` field with context for each category

**Example:**
```sql
name: "Buddy"
description: "Dog care, health, vet appointments"

name: "Wedding - Vendors"
description: "Grove, Pasha, photobooth, invitations"
```

**Benefits:**
- Claude can make intelligent categorization decisions
- User just says "schedule Buddy's vet appointment"
- AI uses description to pick correct category
- No need to hardcode category logic in bot code

### Phase 2C: Health Tracking
**Solution:** Added 5 specialized health tables

**Why separate tables instead of unified?**
- Different data structures (sleep = 1/day, water = many/day)
- Different query patterns (sleep trends vs water totals)
- Easier to add table-specific fields later
- Cleaner API endpoints

---

## Complete Table Definitions

### 1. categories

**Purpose:** Hierarchical organization system for tasks and notes

#### Schema (SQLite)
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    sort_order INTEGER DEFAULT 0,
    parent_id INTEGER REFERENCES categories(id)
);
```

#### Schema (PostgreSQL)
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    sort_order INTEGER DEFAULT 0,
    parent_id INTEGER REFERENCES categories(id)
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key, auto-increment |
| `name` | TEXT | NO | Category name (e.g., "Wedding - Vendors") |
| `description` | TEXT | YES | AI categorization context (e.g., "Grove, Pasha, photobooth") |
| `sort_order` | INTEGER | YES | Display order (0 = default) |
| `parent_id` | INTEGER | YES | Foreign key to parent category (NULL = top-level) |

#### Indexes
```sql
CREATE INDEX idx_categories_parent_id ON categories(parent_id);
CREATE INDEX idx_categories_name ON categories(name);
```

#### Example Data
```
id | name                    | description                                  | parent_id
---+-------------------------+----------------------------------------------+----------
1  | Wedding                 | Wedding planning and coordination            | NULL
2  | Vendors                 | Grove, Pasha, photobooth, invitations        | 1
3  | Grove                   | Venue vendor                                 | 2
4  | Buddy                   | Dog care, health, vet appointments           | NULL
5  | Princeton AI            | AI consulting business                       | NULL
6  | Princeton AI Partners   | Client projects and business operations      | 5
```

#### Validation Rules
- Name cannot be empty
- Cannot set parent_id to own id (circular reference)
- Cannot delete category with children (enforce via API)
- Cannot delete category with tasks without reassignment

---

### 2. tasks

**Purpose:** To-do items with due dates and completion tracking

#### Schema (SQLite)
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER REFERENCES categories(id),
    content TEXT NOT NULL,
    due_date TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_date TEXT NOT NULL
);
```

#### Schema (PostgreSQL)
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    content TEXT NOT NULL,
    due_date TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_date TEXT NOT NULL
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key |
| `category_id` | INTEGER | YES | Foreign key to categories table |
| `content` | TEXT | NO | Task description |
| `due_date` | TEXT | YES | ISO 8601 date (YYYY-MM-DD) |
| `completed` | BOOLEAN | NO | Completion status (default: false) |
| `created_date` | TEXT | NO | ISO 8601 date (YYYY-MM-DD) |

#### Indexes
```sql
CREATE INDEX idx_tasks_category_id ON tasks(category_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
```

#### Example Data
```
id | category_id | content                           | due_date   | completed | created_date
---+-------------+-----------------------------------+------------+-----------+-------------
1  | 4           | Schedule Buddy's vet appointment  | 2025-10-25 | false     | 2025-10-21
2  | 1           | Finalize wedding guest list       | 2025-11-01 | false     | 2025-10-21
3  | 5           | Review client proposal            | 2025-10-22 | true      | 2025-10-20
```

---

### 3. notes

**Purpose:** Free-form notes linked to categories

#### Schema (SQLite/PostgreSQL)
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- SERIAL for PostgreSQL
    category_id INTEGER REFERENCES categories(id),
    content TEXT NOT NULL,
    created_date TEXT NOT NULL
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key |
| `category_id` | INTEGER | YES | Foreign key to categories table |
| `content` | TEXT | NO | Note content (can be long-form) |
| `created_date` | TEXT | NO | ISO 8601 date (YYYY-MM-DD) |

#### Indexes
```sql
CREATE INDEX idx_notes_category_id ON notes(category_id);
```

---

### 4. sleep_logs

**Purpose:** Daily sleep tracking (one entry per night)

#### Schema (SQLite)
```sql
CREATE TABLE sleep_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    hours REAL NOT NULL,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### Schema (PostgreSQL)
```sql
CREATE TABLE sleep_logs (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL UNIQUE,
    hours REAL NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key |
| `date` | TEXT | NO | ISO date (YYYY-MM-DD), UNIQUE |
| `hours` | REAL | NO | Hours slept (e.g., 7.5) |
| `notes` | TEXT | YES | Optional notes (e.g., "woke up at 3am") |
| `created_at` | TEXT/TIMESTAMP | NO | When log was created |

#### Usage Examples
```
Telegram: "I slept 8 hours last night"
Result: INSERT INTO sleep_logs (date, hours) VALUES ('2025-10-20', 8.0)

Telegram: "slept 7.5 hours, woke up feeling tired"
Result: INSERT INTO sleep_logs (date, hours, notes)
        VALUES ('2025-10-20', 7.5, 'woke up feeling tired')
```

---

### 5. water_logs

**Purpose:** Water intake tracking (multiple entries per day)

#### Schema (SQLite)
```sql
CREATE TABLE water_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    cups INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### Schema (PostgreSQL)
```sql
CREATE TABLE water_logs (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL,
    cups INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key |
| `date` | TEXT | NO | ISO date (YYYY-MM-DD), NOT UNIQUE |
| `cups` | INTEGER | NO | Number of cups (usually 1 per log) |
| `timestamp` | TEXT | NO | ISO timestamp with time |
| `created_at` | TEXT/TIMESTAMP | NO | When log was created |

#### Design Decision: Why NOT UNIQUE date?
Water is logged multiple times per day. Each entry represents a single drinking event.

#### Query Pattern
```sql
-- Get total water for a day
SELECT SUM(cups) as total_cups
FROM water_logs
WHERE date = '2025-10-21'

-- Get timeline for a day
SELECT timestamp, cups
FROM water_logs
WHERE date = '2025-10-21'
ORDER BY timestamp
```

#### Usage Examples
```
Telegram: "drank 3 cups of water"
Result: INSERT INTO water_logs (date, cups, timestamp)
        VALUES ('2025-10-21', 3, '2025-10-21T14:30:00')

Telegram: "water" (log 1 cup)
Result: INSERT INTO water_logs (date, cups, timestamp)
        VALUES ('2025-10-21', 1, '2025-10-21T15:45:00')
```

---

### 6. exercise_logs

**Purpose:** Exercise activity tracking (multiple entries per day allowed)

#### Schema (SQLite)
```sql
CREATE TABLE exercise_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### Schema (PostgreSQL)
```sql
CREATE TABLE exercise_logs (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key |
| `date` | TEXT | NO | ISO date (YYYY-MM-DD) |
| `activity_type` | TEXT | NO | Activity name (e.g., "Pickleball", "Gym", "BJJ") |
| `duration_minutes` | INTEGER | NO | Duration in minutes |
| `notes` | TEXT | YES | Optional notes |
| `created_at` | TEXT/TIMESTAMP | NO | When log was created |

#### Common Activity Types
- Pickleball
- Gym
- BJJ (Brazilian Jiu-Jitsu)
- Yoga
- Running
- Swimming

#### Query Pattern
```sql
-- Activity breakdown for last 30 days
SELECT activity_type,
       SUM(duration_minutes) as total_minutes,
       COUNT(*) as sessions
FROM exercise_logs
WHERE date >= DATE('now', '-30 days')
GROUP BY activity_type
ORDER BY total_minutes DESC
```

#### Usage Examples
```
Telegram: "played pickleball for 45 minutes"
Result: INSERT INTO exercise_logs (date, activity_type, duration_minutes)
        VALUES ('2025-10-21', 'Pickleball', 45)

Telegram: "1 hour gym session, upper body focus"
Result: INSERT INTO exercise_logs (date, activity_type, duration_minutes, notes)
        VALUES ('2025-10-21', 'Gym', 60, 'upper body focus')
```

---

### 7. sauna_logs

**Purpose:** Sauna session tracking (one entry per day, but tracks multiple visits)

#### Schema (SQLite)
```sql
CREATE TABLE sauna_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    num_visits INTEGER NOT NULL DEFAULT 1,
    duration_minutes INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### Schema (PostgreSQL)
```sql
CREATE TABLE sauna_logs (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL UNIQUE,
    num_visits INTEGER NOT NULL DEFAULT 1,
    duration_minutes INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key |
| `date` | TEXT | NO | ISO date (YYYY-MM-DD), UNIQUE |
| `num_visits` | INTEGER | NO | Number of sauna visits that day (default: 1) |
| `duration_minutes` | INTEGER | NO | Total duration in minutes |
| `created_at` | TEXT/TIMESTAMP | NO | When log was created |

#### Design Decision: UNIQUE date
Sauna is aggregated per day (unlike water/exercise which are logged individually).

#### Usage Examples
```
Telegram: "15 minutes in sauna"
Result: INSERT INTO sauna_logs (date, num_visits, duration_minutes)
        VALUES ('2025-10-21', 1, 15)

Telegram: "did sauna twice today, 30 minutes total"
Result: INSERT INTO sauna_logs (date, num_visits, duration_minutes)
        VALUES ('2025-10-21', 2, 30)
```

---

### 8. inbody_measurements

**Purpose:** Body composition tracking from InBody scans

#### Schema (SQLite)
```sql
CREATE TABLE inbody_measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    weight REAL NOT NULL,
    smm REAL NOT NULL,
    pbf REAL NOT NULL,
    ecw_tbw_ratio REAL NOT NULL,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

#### Schema (PostgreSQL)
```sql
CREATE TABLE inbody_measurements (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL UNIQUE,
    weight REAL NOT NULL,
    smm REAL NOT NULL,
    pbf REAL NOT NULL,
    ecw_tbw_ratio REAL NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Columns

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| `id` | INTEGER/SERIAL | NO | Primary key |
| `date` | TEXT | NO | ISO date (YYYY-MM-DD), UNIQUE |
| `weight` | REAL | NO | Body weight in pounds |
| `smm` | REAL | NO | Skeletal Muscle Mass in pounds |
| `pbf` | REAL | NO | Percent Body Fat (%) |
| `ecw_tbw_ratio` | REAL | NO | Extracellular Water / Total Body Water ratio |
| `notes` | TEXT | YES | Optional notes |
| `created_at` | TEXT/TIMESTAMP | NO | When log was created |

#### InBody Metrics Explained

**Weight:** Total body weight
**SMM (Skeletal Muscle Mass):** Muscle you can actively control
**PBF (Percent Body Fat):** Body fat percentage
**ECW/TBW Ratio:** Hydration and inflammation indicator
- Normal range: 0.360 - 0.390
- Higher = potential inflammation/water retention
- Lower = good muscle hydration

#### Usage Examples
```
Telegram: "InBody: 174 lbs, 84.5 SMM, 18.2% PBF, 0.385 ECW/TBW"
Result: INSERT INTO inbody_measurements
        (date, weight, smm, pbf, ecw_tbw_ratio)
        VALUES ('2025-10-21', 174.0, 84.5, 18.2, 0.385)
```

#### Typical Trends
```
Goal: Gaining weight with muscle
- Weight: 170 → 174 lbs (+4 lbs over 4 weeks)
- SMM: 82 → 84.5 lbs (+2.5 lbs muscle)
- PBF: 14.5% → 18.2% (+3.7% - some fat gain expected)
- ECW/TBW: 0.38-0.39 (stable, healthy range)
```

---

## Relationships & Hierarchy

### Entity Relationship Diagram (Text)

```
categories (parent-child hierarchy)
    ↓ (1:many)
tasks (many tasks per category)

categories (parent-child hierarchy)
    ↓ (1:many)
notes (many notes per category)

(Health tables are independent, no foreign keys)
sleep_logs
water_logs
exercise_logs
sauna_logs
inbody_measurements
```

### Category Tree Example

```
Wedding (id: 1, parent_id: NULL)
├── Vendors (id: 2, parent_id: 1)
│   ├── Grove (id: 3, parent_id: 2)
│   ├── Pasha (id: 4, parent_id: 2)
│   └── Photobooth (id: 5, parent_id: 2)
├── Bachelor Party (id: 6, parent_id: 1)
└── Dances (id: 7, parent_id: 1)

Princeton AI (id: 8, parent_id: NULL)
├── Princeton AI Partners (id: 9, parent_id: 8)
│   ├── UpLevel Resume (id: 10, parent_id: 9)
│   └── Hamilton Deli (id: 11, parent_id: 9)
└── Generic Tasks (id: 12, parent_id: 8)
```

### Querying Hierarchy

**Get all top-level categories:**
```sql
SELECT * FROM categories WHERE parent_id IS NULL
ORDER BY sort_order, name
```

**Get immediate children of a category:**
```sql
SELECT * FROM categories WHERE parent_id = ?
ORDER BY sort_order, name
```

**Get all tasks in a category AND its children:**
```sql
WITH RECURSIVE category_tree AS (
    SELECT id FROM categories WHERE id = ?
    UNION ALL
    SELECT c.id FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT t.* FROM tasks t
WHERE t.category_id IN (SELECT id FROM category_tree)
```

---

## Migration History

### Migration 1: Base Schema (migrate_to_postgres.py)
**Date:** October 21, 2025
**Purpose:** Migrate SQLite → PostgreSQL for production deployment

**Changes:**
- Created categories, tasks, notes tables
- Migrated 50 categories
- Migrated 77 tasks
- Migrated 20 notes
- Two-pass strategy for parent_id relationships

**SQLite → PostgreSQL Syntax Changes:**
```sql
-- SQLite
INTEGER PRIMARY KEY AUTOINCREMENT
cursor.lastrowid
'?' placeholders

-- PostgreSQL
SERIAL PRIMARY KEY
RETURNING id
'%s' placeholders
```

### Migration 2: Category Hierarchy (migrate_category_hierarchy.py)
**Date:** October 2025 (Phase 2A)
**Purpose:** Add parent-child relationships to categories

**Changes:**
1. Added `parent_id` column (foreign key to categories.id)
2. Parsed category names with " - " separators
3. Created missing parent categories
4. Built parent_id relationships

**Example Transformation:**
```
Before:
- "Wedding - Vendors - Grove" (flat)

After:
- "Wedding" (parent_id: NULL)
- "Wedding - Vendors" (parent_id: Wedding.id)
- "Wedding - Vendors - Grove" (parent_id: Vendors.id)
```

**Result:**
- Top-level categories: 15
- Subcategories: 35
- Total: 50 categories

### Migration 3: Category Descriptions (migrate_category_descriptions.py)
**Date:** October 2025 (Phase 2B)
**Purpose:** Move hardcoded category context to database

**Changes:**
- Added `description` column
- Populated 60+ category descriptions
- Removed hardcoded logic from router.py

**Before (hardcoded in router.py):**
```python
CATEGORY_CONTEXT = {
    "Buddy": "Dog care, health, vet appointments",
    # ... 60+ more
}
```

**After (in database):**
```sql
UPDATE categories
SET description = 'Dog care, health, vet appointments'
WHERE name = 'Buddy'
```

### Migration 4: Health Tables (migrate_health_tables.py)
**Date:** October 21, 2025 (Phase 2C)
**Purpose:** Create health tracking system

**Changes:**
- Created 5 health tables (sleep, water, exercise, sauna, InBody)
- Generated 30 days of dummy data for local testing
- Production tables created empty (ready for real data)

**PostgreSQL Version (migrate_health_tables_postgres.py):**
- Same schema, different syntax (SERIAL, TIMESTAMP)
- No dummy data in production
- Ready for Telegram bot logging

---

## API Endpoints

### Core Endpoints

#### Categories
```
GET    /api/categories              # Get all categories (hierarchical)
GET    /api/categories/:id          # Get single category
POST   /api/categories              # Create new category
PUT    /api/categories/:id          # Update category
DELETE /api/categories/:id          # Delete category (checks for children/tasks)
```

#### Tasks
```
GET    /api/tasks                   # Get all tasks (filterable)
       ?category_id=X               # Filter by category
       &include_children=true       # Include subcategory tasks
       &completed=false             # Filter by completion status
GET    /api/tasks/:id               # Get single task
POST   /api/tasks                   # Create new task
PUT    /api/tasks/:id               # Update task
DELETE /api/tasks/:id               # Delete task
```

#### Notes
```
GET    /api/notes                   # Get all notes
       ?category_id=X               # Filter by category
GET    /api/notes/:id               # Get single note
POST   /api/notes                   # Create new note
PUT    /api/notes/:id               # Update note
DELETE /api/notes/:id               # Delete note
```

### Health Endpoints

#### Sleep
```
GET    /api/health/sleep            # Get sleep logs
       ?start_date=YYYY-MM-DD       # Optional date range
       &end_date=YYYY-MM-DD
POST   /api/health/sleep            # Log sleep
       Body: { date, hours, notes }
```

#### Water
```
GET    /api/health/water            # Get water logs
       ?date=YYYY-MM-DD             # Specific day (default: today)
POST   /api/health/water            # Log water
       Body: { date, cups, timestamp }
```

#### Exercise
```
GET    /api/health/exercise         # Get exercise logs
       ?start_date=YYYY-MM-DD
       &end_date=YYYY-MM-DD
POST   /api/health/exercise         # Log exercise
       Body: { date, activity_type, duration_minutes, notes }
```

#### Sauna
```
GET    /api/health/sauna            # Get sauna logs
       ?start_date=YYYY-MM-DD
       &end_date=YYYY-MM-DD
POST   /api/health/sauna            # Log sauna
       Body: { date, num_visits, duration_minutes }
```

#### InBody
```
GET    /api/health/inbody           # Get InBody measurements (last 20)
POST   /api/health/inbody           # Log InBody
       Body: { date, weight, smm, pbf, ecw_tbw_ratio, notes }
```

#### Summary
```
GET    /api/health/summary          # Get today's health summary
       Response: {
         sleep: { hours, date },
         water: { total_cups, entries },
         exercise: [ {activity, duration} ],
         sauna: { duration, num_visits } | null,
         latest_inbody: { weight, smm, pbf, ecw_tbw_ratio, date }
       }
```

---

## Design Decisions

### Why Hierarchical Categories?

**Problem:** Flat categories like "Wedding - Vendors - Grove" were:
- Redundant (repeating parent names)
- Hard to display as folders in UI
- No referential integrity

**Solution:** parent_id foreign key
- Clean tree structure
- Database enforces relationships
- Efficient queries for subtrees
- Better UX (collapsible folders)

### Why Category Descriptions?

**Problem:** Bot code had 150+ lines of hardcoded category context

**Solution:** Move context to database
- AI reads descriptions for categorization
- Easier to add new categories (no code changes)
- Users can update descriptions via UI
- Single source of truth

**Example Use Case:**
```
User: "Schedule Buddy's grooming"
AI reads: "Buddy" description = "Dog care, health, vet appointments"
AI decision: Categorize under "Buddy"
```

### Why Separate Health Tables?

**Alternative:** Single `health_logs` table with `type` column
```sql
CREATE TABLE health_logs (
    id, date, type, value, metadata_json
)
```

**Why we chose separate tables:**
1. **Different data structures**
   - Sleep: 1 entry/day (hours)
   - Water: Many entries/day (cups + timestamps)
   - InBody: 4 metrics + 1 ratio

2. **Query performance**
   - No filtering by `type` needed
   - Each table optimized for its access pattern

3. **Schema flexibility**
   - Can add InBody-specific columns without affecting water table
   - Type safety (weight is REAL, not JSON)

4. **API clarity**
   - `/api/health/sleep` vs `/api/health?type=sleep`
   - Clear separation of concerns

### Why TEXT for Dates Instead of DATE type?

**Reasoning:**
- SQLite doesn't have native DATE type
- ISO 8601 format (YYYY-MM-DD) sorts correctly as text
- Works identically in SQLite and PostgreSQL
- Easier date comparisons: `WHERE date >= '2025-10-01'`

**Alternative Considered:**
- PostgreSQL DATE type with migration complexity
- Chose TEXT for SQLite compatibility

### Why UNIQUE on Some Tables but Not Others?

**UNIQUE constraints:**
- `sleep_logs.date` - Only 1 sleep entry per night
- `sauna_logs.date` - Aggregate visits per day
- `inbody_measurements.date` - Only 1 scan per day

**NO UNIQUE constraint:**
- `water_logs.date` - Multiple entries throughout day
- `exercise_logs.date` - Can exercise multiple times per day

---

## Database Access Layer

### db_helper.py - Auto-Detection

**Purpose:** Single codebase works with both SQLite and PostgreSQL

```python
def get_db_connection():
    if DATABASE_URL and PSYCOPG2_AVAILABLE:
        return psycopg2_connection, cursor, 'postgres'
    else:
        return sqlite3_connection, cursor, 'sqlite'
```

**Features:**
- Auto-detects database type via `DATABASE_URL` env var
- Converts query placeholders (`?` → `%s` for PostgreSQL)
- Handles `RETURNING id` vs `cursor.lastrowid`
- Returns RealDictCursor (rows as dictionaries)

**Benefits:**
- Develop locally with SQLite
- Deploy to production with PostgreSQL
- No code changes needed
- Same migration scripts work for both

---

## Production vs Local

### Local Development (SQLite)
```bash
Database: data.db (file-based)
Location: life-os/data.db
Dummy Data: 30 days of health logs
Tables: All 8 tables
Frontend: localhost:5173
Backend: localhost:5000
```

### Production (PostgreSQL on Render)
```bash
Database: lifeos (PostgreSQL 15)
Host: dpg-d3r8oj6uk2gs73cbdlu0-a.ohio-postgres.render.com
Real Data: Tasks, notes, categories from SQLite migration
Empty Tables: Health tables (ready for real logging)
Bot: Render Background Worker
Connection: DATABASE_URL environment variable
```

### Data Separation

**IMPORTANT:** Local and production databases are completely separate!

- Local changes do NOT affect production
- Test health logging locally first
- Migrate data explicitly when ready
- Use environment variable to switch

---

## Common Queries

### Get Today's Health Summary
```sql
SELECT
    (SELECT hours FROM sleep_logs WHERE date = '2025-10-21') as sleep_hours,
    (SELECT SUM(cups) FROM water_logs WHERE date = '2025-10-21') as total_water,
    (SELECT COUNT(*) FROM exercise_logs WHERE date = '2025-10-21') as exercise_count
```

### Get Category Tree with Task Counts
```sql
SELECT
    c.id,
    c.name,
    c.description,
    c.parent_id,
    COUNT(t.id) as task_count
FROM categories c
LEFT JOIN tasks t ON c.id = t.category_id AND t.completed = false
GROUP BY c.id, c.name, c.description, c.parent_id
ORDER BY c.sort_order, c.name
```

### Get Exercise Breakdown (Last 30 Days)
```sql
SELECT
    activity_type,
    COUNT(*) as sessions,
    SUM(duration_minutes) as total_minutes,
    ROUND(AVG(duration_minutes), 1) as avg_duration
FROM exercise_logs
WHERE date >= DATE('now', '-30 days')
GROUP BY activity_type
ORDER BY total_minutes DESC
```

### Get InBody Trends
```sql
SELECT
    date,
    weight,
    smm,
    pbf,
    ecw_tbw_ratio,
    weight - LAG(weight) OVER (ORDER BY date) as weight_change,
    smm - LAG(smm) OVER (ORDER BY date) as smm_change
FROM inbody_measurements
ORDER BY date DESC
LIMIT 10
```

### Get Sleep Average (Last 7 Days)
```sql
SELECT
    AVG(hours) as avg_sleep,
    MIN(hours) as min_sleep,
    MAX(hours) as max_sleep
FROM sleep_logs
WHERE date >= DATE('now', '-7 days')
```

---

## Future Enhancements

### Planned Schema Changes

**Phase 3: Food Tracking**
```sql
CREATE TABLE food_logs (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL,
    meal_time TEXT,  -- breakfast, lunch, dinner, snack
    description TEXT,
    calories INTEGER,
    protein_grams REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Phase 3: Voice Notes**
```sql
CREATE TABLE voice_notes (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    audio_file_path TEXT,
    transcription TEXT,
    duration_seconds INTEGER,
    created_date TEXT NOT NULL
);
```

**Phase 3: Image Support**
```sql
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    image_file_path TEXT,
    caption TEXT,
    clip_embedding BYTEA,  -- CLIP embeddings for semantic search
    created_date TEXT NOT NULL
);
```

### Optimization Opportunities

**Full-text search on tasks/notes:**
```sql
-- PostgreSQL
CREATE INDEX idx_tasks_content_fts ON tasks USING GIN(to_tsvector('english', content));

-- SQLite
CREATE VIRTUAL TABLE tasks_fts USING fts5(content);
```

**Materialized views for health summaries:**
```sql
CREATE MATERIALIZED VIEW health_weekly_summary AS
SELECT
    DATE_TRUNC('week', date::date) as week,
    AVG(hours) as avg_sleep
FROM sleep_logs
GROUP BY week;
```

---

## Troubleshooting

### Common Schema Issues

**Issue:** "no such column: parent_id"
**Fix:** Run `migrate_category_hierarchy.py`

**Issue:** Categories have empty descriptions
**Fix:** Run `migrate_category_descriptions.py`

**Issue:** Health tables don't exist
**Fix:** Run `migrate_health_tables.py` (SQLite) or `migrate_health_tables_postgres.py` (PostgreSQL)

**Issue:** PostgreSQL syntax errors (AUTOINCREMENT)
**Fix:** Use `migrate_*_postgres.py` scripts for PostgreSQL, not SQLite scripts

**Issue:** Foreign key constraint violations
**Fix:** Ensure categories exist before creating tasks/notes

---

## Schema Verification

### Check All Tables Exist
```sql
-- SQLite
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

-- PostgreSQL
SELECT table_name FROM information_schema.tables
WHERE table_schema='public' ORDER BY table_name;
```

### Verify Row Counts
```sql
SELECT
    (SELECT COUNT(*) FROM categories) as categories,
    (SELECT COUNT(*) FROM tasks) as tasks,
    (SELECT COUNT(*) FROM notes) as notes,
    (SELECT COUNT(*) FROM sleep_logs) as sleep,
    (SELECT COUNT(*) FROM water_logs) as water,
    (SELECT COUNT(*) FROM exercise_logs) as exercise,
    (SELECT COUNT(*) FROM sauna_logs) as sauna,
    (SELECT COUNT(*) FROM inbody_measurements) as inbody;
```

### Check Hierarchy Integrity
```sql
-- Find categories with invalid parent_id
SELECT c1.id, c1.name, c1.parent_id
FROM categories c1
LEFT JOIN categories c2 ON c1.parent_id = c2.id
WHERE c1.parent_id IS NOT NULL AND c2.id IS NULL;

-- Should return 0 rows (no orphaned categories)
```

---

## Conclusion

This schema is designed for:
- Hierarchical organization (parent_id relationships)
- AI-powered categorization (description fields)
- Comprehensive health tracking (5 specialized tables)
- Dual database support (SQLite + PostgreSQL)
- Future extensibility (voice, images, food tracking)

**Current Status:** Phase 2C Complete
- 50 categories with hierarchy
- 77 tasks migrated
- 20 notes migrated
- 5 health tables ready for logging
- Dashboard visualizations working locally

**Next Phase:** Health logging via Telegram + Dashboard deployment to Vercel

---

**Last Updated:** October 21, 2025
**Maintained By:** Parth + Claude Code
**Version:** 2.0 (Phase 2C - Health Tracking Complete)
