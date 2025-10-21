# Phase 2D: React Dashboard - Detailed Implementation Plan

**Created:** October 21, 2025
**Phase:** 2D - Visual Interface
**Timeline:** 2-3 days
**Status:** Planning - Ready to Implement

---

## Executive Summary

Build a clean, modern web dashboard using React.js and shadcn/ui to provide visual access to all Life OS data. The dashboard will complement the Telegram bot interface by offering bulk management, visual organization, and easier data manipulation.

**Key Principle:** Keep it very simple - focus on core CRUD operations and clean UI.

---

## User Requirements

From user conversation:
> "we will continue tomorrow with a react js shadcn style dashboard where I can actually see all my data and stuff. I want a very very simple dashboard where I can edit all my stuff, see my calendar, and mark tasks as complete. also move tasks/notes around if needed. just a very clean modern customizable interactive dashboard with my database."

**Breakdown:**
1. ✅ See all data (tasks, notes, calendar)
2. ✅ Edit everything
3. ✅ Mark tasks complete
4. ✅ Move tasks/notes between categories
5. ✅ Clean, modern design (shadcn/ui)
6. ✅ Customizable and interactive
7. ✅ Connect to existing database

---

## Architecture Overview

### System Components

```
┌──────────────────────────────────────────────────────────┐
│                    User                                  │
└────────────┬─────────────────────────┬───────────────────┘
             │                         │
             v                         v
    ┌────────────────┐       ┌─────────────────────┐
    │  Telegram Bot  │       │  React Dashboard    │
    │  (Mobile/Fast) │       │  (Desktop/Visual)   │
    └────────┬───────┘       └──────────┬──────────┘
             │                          │
             v                          v
    ┌────────────────┐       ┌─────────────────────┐
    │ telegram_bot.py│       │  Flask REST API     │
    │  + router.py   │       │  (api_server.py)    │
    └────────┬───────┘       └──────────┬──────────┘
             │                          │
             └────────┬─────────────────┘
                      v
          ┌───────────────────────┐
          │   Shared Database     │
          │                       │
          │  • data.db (SQLite)   │
          │  • vector_store.json  │
          │  • OpenAI Embeddings  │
          └───────────────────────┘
```

### Key Architectural Decisions

**1. Dual Interface Approach**
- Telegram: Quick capture, mobile-friendly, always available
- Dashboard: Visual organization, bulk operations, detailed view
- Both share same database (no sync issues)

**2. Local-First Development**
- Dashboard runs locally (localhost:5173)
- API runs locally (localhost:5000)
- Database is local data.db file
- No deployment complexity initially

**3. Shared Database**
- Both Telegram bot and dashboard read/write to data.db
- SQLite handles concurrent access
- Changes visible immediately in both interfaces

---

## Technology Stack

### Frontend

**Core:**
- **React 18+** - UI library
- **Vite** - Build tool (fast dev server, HMR)
- **TypeScript** - Type safety
- **React Router** - Client-side routing

**UI Components:**
- **shadcn/ui** - Pre-built components (https://ui.shadcn.com)
- **shadcn MCP** - For easy component installation
- **Tailwind CSS** - Utility-first styling
- **Radix UI** - Primitives (via shadcn)
- **Lucide Icons** - Icon library

**Data Fetching:**
- **TanStack Query (React Query)** - Server state management
- **Axios** - HTTP client

**Forms:**
- **React Hook Form** - Form state management
- **Zod** - Schema validation

### Backend

**API:**
- **Flask** - Python web framework (already in requirements.txt)
- **Flask-CORS** - Cross-origin requests (already in requirements.txt)
- **SQLite3** - Database (built into Python)

**Existing Code Reuse:**
- `scripts/db.py` - Database operations
- `scripts/vector_store.py` - RAG operations
- `scripts/categories.py` - Category definitions

### Development Tools

- **npm/pnpm** - Package management
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Git** - Version control

---

## Detailed Component Breakdown

### Page Structure

```
Dashboard (/)
├── Sidebar Navigation
│   ├── 📋 Tasks
│   ├── 📝 Notes
│   ├── 📅 Calendar
│   └── 🔍 Search
│
├── Tasks Page (/tasks)
│   ├── Filter Bar (All/Today/Week/Overdue)
│   ├── Category Filter
│   ├── Task List
│   │   └── Task Card (editable)
│   └── Create Task Button
│
├── Notes Page (/notes)
│   ├── Category Filter
│   ├── Note Grid
│   │   └── Note Card (editable)
│   └── Create Note Button
│
├── Calendar Page (/calendar)
│   ├── Month View
│   ├── Event List
│   └── Create Event Button
│
└── Search Page (/search)
    ├── Search Bar
    ├── Filter Options
    └── Results List
```

### Component Hierarchy

**1. Layout Components**
```tsx
<DashboardLayout>
  <Sidebar />
  <Header>
    <SearchBar />
    <UserMenu />
  </Header>
  <MainContent>
    <Outlet /> {/* React Router outlet */}
  </MainContent>
</DashboardLayout>
```

**2. Task Components**
```tsx
<TasksPage>
  <FilterBar />
  <TaskList>
    <TaskCard
      task={task}
      onEdit={handleEdit}
      onDelete={handleDelete}
      onToggleComplete={handleToggleComplete}
      onMoveCategory={handleMoveCategory}
    />
  </TaskList>
  <CreateTaskDialog />
</TasksPage>
```

**3. Note Components**
```tsx
<NotesPage>
  <CategoryFilter />
  <NoteGrid>
    <NoteCard
      note={note}
      onEdit={handleEdit}
      onDelete={handleDelete}
      onMoveCategory={handleMoveCategory}
    />
  </NoteGrid>
  <CreateNoteDialog />
</NotesPage>
```

**4. Shared Components**
```tsx
// shadcn/ui components
- Button
- Card
- Dialog
- Input
- Select
- Checkbox
- Badge
- Separator
- DropdownMenu
- Calendar
- Popover
- Textarea
- Label

// Custom components
- CategoryBadge
- TaskStatusBadge
- DeleteConfirmDialog
- EditTaskDialog
- EditNoteDialog
- CategorySelector
```

---

## API Specification

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Tasks

```
GET    /api/tasks
Query params:
  - category: string (optional)
  - status: 'complete' | 'incomplete' | 'all' (optional)
  - due_date_filter: 'today' | 'week' | 'overdue' | 'all' (optional)

Response: {
  tasks: [
    {
      id: number,
      content: string,
      category: string,
      due_date: string | null,
      priority: string | null,
      is_completed: boolean,
      created_date: string
    }
  ]
}
```

```
GET    /api/tasks/:id
Response: { task: {...} }
```

```
POST   /api/tasks
Body: {
  content: string,
  category: string,
  due_date: string | null,
  priority: string | null
}
Response: { task: {...} }
Action: Creates task + auto-vectorizes
```

```
PUT    /api/tasks/:id
Body: {
  content: string,
  category: string,
  due_date: string | null,
  priority: string | null
}
Response: { task: {...} }
Action: Updates task + updates vector store
```

```
PATCH  /api/tasks/:id/complete
Body: { is_completed: boolean }
Response: { task: {...} }
Action: Toggles completion status
```

```
DELETE /api/tasks/:id
Response: { success: true }
Action: Deletes task + removes from vector store
```

#### Notes

```
GET    /api/notes
Query params:
  - category: string (optional)

Response: {
  notes: [
    {
      id: number,
      content: string,
      category: string,
      created_date: string
    }
  ]
}
```

```
GET    /api/notes/:id
Response: { note: {...} }
```

```
POST   /api/notes
Body: {
  content: string,
  category: string
}
Response: { note: {...} }
Action: Creates note + auto-vectorizes
```

```
PUT    /api/notes/:id
Body: {
  content: string,
  category: string
}
Response: { note: {...} }
Action: Updates note + updates vector store
```

```
DELETE /api/notes/:id
Response: { success: true }
Action: Deletes note + removes from vector store
```

#### Categories

```
GET    /api/categories
Response: {
  categories: [
    {
      name: string,
      parent: string | null,
      level: number
    }
  ]
}
```

#### Search

```
GET    /api/search
Query params:
  - q: string (required)
  - type: 'all' | 'tasks' | 'notes' (optional, default: 'all')
  - limit: number (optional, default: 10)

Response: {
  results: [
    {
      id: string, // "task_123" or "note_456"
      type: 'task' | 'note',
      content: string,
      category: string,
      similarity: number,
      metadata: {...}
    }
  ]
}
Action: Uses vector_store.py RAG query
```

#### Calendar (Future - Phase 2B)

```
GET    /api/calendar/events
Query params:
  - start_date: string (ISO)
  - end_date: string (ISO)

Response: {
  events: [
    {
      id: string,
      title: string,
      description: string,
      start: string (ISO),
      end: string (ISO),
      calendar: string
    }
  ]
}
```

---

## Database Schema (Existing)

**Tasks Table:**
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    due_date TEXT,
    priority TEXT,
    is_completed BOOLEAN DEFAULT 0,
    created_date TEXT NOT NULL
);
```

**Notes Table:**
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    created_date TEXT NOT NULL
);
```

**Vector Store (JSON):**
```json
{
  "metadata": {
    "model": "text-embedding-3-small",
    "provider": "openai",
    "dimensions": 384
  },
  "items": [
    {
      "id": "task_123",
      "type": "task",
      "category": "Wedding Planning",
      "content": "Book photographer",
      "embedding": [0.123, 0.456, ...],
      "created_date": "2025-10-21T10:00:00"
    }
  ]
}
```

---

## Implementation Timeline

### Day 1: Foundation & Tasks View

**Morning (2-3 hours):**
1. Set up React + Vite + TypeScript project
2. Configure shadcn/ui using MCP
3. Install base components (Button, Card, Input, etc.)
4. Set up Tailwind CSS
5. Create basic layout (Sidebar, Header, MainContent)
6. Set up React Router

**Afternoon (3-4 hours):**
7. Build Flask API foundation (`api_server.py`)
8. Implement GET /api/tasks endpoint
9. Implement POST /api/tasks endpoint
10. Test with existing data.db
11. Enable CORS

**Evening (2-3 hours):**
12. Build TaskList component
13. Build TaskCard component
14. Implement task display from API
15. Add basic styling with shadcn/ui

**End of Day 1:** Can view all tasks in clean UI

---

### Day 2: Full CRUD & Notes

**Morning (2-3 hours):**
1. Implement PUT /api/tasks/:id endpoint
2. Implement DELETE /api/tasks/:id endpoint
3. Implement PATCH /api/tasks/:id/complete endpoint
4. Build EditTaskDialog component
5. Build DeleteConfirmDialog component
6. Wire up edit/delete/complete actions

**Afternoon (3-4 hours):**
7. Implement Notes API endpoints (GET, POST, PUT, DELETE)
8. Build NotesPage component
9. Build NoteCard component
10. Build EditNoteDialog component
11. Wire up notes CRUD operations

**Evening (2-3 hours):**
12. Add category filtering to both Tasks and Notes
13. Build CategorySelector component
14. Implement move to category functionality
15. Add filter bar (Today, Week, Overdue)

**End of Day 2:** Full CRUD for tasks and notes working

---

### Day 3: Search, Calendar, Polish

**Morning (2-3 hours):**
1. Implement GET /api/search endpoint (using vector_store.py)
2. Build SearchPage component
3. Build SearchBar component
4. Implement semantic search UI
5. Test search with existing vector store

**Afternoon (2-3 hours):**
6. Build CalendarPage placeholder (for Phase 2B)
7. Add loading states to all components
8. Add error handling and toast notifications
9. Improve mobile responsiveness
10. Add dark mode toggle (optional)

**Evening (2-3 hours):**
11. Polish UI/UX (spacing, colors, animations)
12. Test all CRUD operations thoroughly
13. Test concurrent access (Telegram bot + dashboard)
14. Fix any bugs
15. Write README for dashboard

**End of Day 3:** Production-ready dashboard!

---

## Step-by-Step Implementation Guide

### Step 1: Project Setup

```bash
# Create frontend directory
cd /path/to/life-os
mkdir frontend
cd frontend

# Initialize Vite + React + TypeScript
npm create vite@latest . -- --template react-ts

# Install dependencies
npm install

# Install shadcn/ui CLI
npm install -D @shadcn/ui

# Initialize shadcn/ui
npx shadcn@latest init
# Choose:
# - Style: Default
# - Base color: Slate
# - CSS variables: Yes

# Install additional dependencies
npm install @tanstack/react-query axios react-router-dom
npm install react-hook-form zod @hookform/resolvers
npm install lucide-react
npm install -D tailwindcss-animate
```

### Step 2: Configure shadcn MCP

```bash
# Install shadcn MCP
pnpm dlx shadcn@latest mcp init --client claude

# Restart Claude Code to load MCP

# Then use natural language:
# "Add button, card, dialog, input, select, checkbox components"
```

### Step 3: Set Up Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn components
│   │   ├── layout/
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Header.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── EditTaskDialog.tsx
│   │   │   └── CreateTaskDialog.tsx
│   │   ├── notes/
│   │   │   ├── NoteList.tsx
│   │   │   ├── NoteCard.tsx
│   │   │   └── EditNoteDialog.tsx
│   │   └── shared/
│   │       ├── CategoryBadge.tsx
│   │       ├── DeleteConfirmDialog.tsx
│   │       └── SearchBar.tsx
│   ├── pages/
│   │   ├── TasksPage.tsx
│   │   ├── NotesPage.tsx
│   │   ├── CalendarPage.tsx
│   │   └── SearchPage.tsx
│   ├── lib/
│   │   ├── api.ts          # API client
│   │   ├── queries.ts      # React Query hooks
│   │   └── utils.ts        # Utility functions
│   ├── types/
│   │   └── index.ts        # TypeScript types
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

### Step 4: Create API Client

```typescript
// src/lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const tasksApi = {
  getAll: (filters?: { category?: string; status?: string }) =>
    api.get('/tasks', { params: filters }),

  getById: (id: number) =>
    api.get(`/tasks/${id}`),

  create: (task: CreateTaskDto) =>
    api.post('/tasks', task),

  update: (id: number, task: UpdateTaskDto) =>
    api.put(`/tasks/${id}`, task),

  toggleComplete: (id: number, isCompleted: boolean) =>
    api.patch(`/tasks/${id}/complete`, { is_completed: isCompleted }),

  delete: (id: number) =>
    api.delete(`/tasks/${id}`),
};

export const notesApi = {
  getAll: (filters?: { category?: string }) =>
    api.get('/notes', { params: filters }),

  create: (note: CreateNoteDto) =>
    api.post('/notes', note),

  update: (id: number, note: UpdateNoteDto) =>
    api.put(`/notes/${id}`, note),

  delete: (id: number) =>
    api.delete(`/notes/${id}`),
};

export const categoriesApi = {
  getAll: () => api.get('/categories'),
};

export const searchApi = {
  search: (query: string, type?: 'all' | 'tasks' | 'notes') =>
    api.get('/search', { params: { q: query, type } }),
};
```

### Step 5: Create Flask API

```python
# scripts/api_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from db import get_db_connection
from vector_store import add_to_vector_store, remove_from_vector_store, update_in_vector_store
from rag_query import rag_query
from categories import CATEGORIES

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Tasks endpoints
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    category = request.args.get('category')
    status = request.args.get('status', 'all')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tasks"
    conditions = []
    params = []

    if category:
        conditions.append("category = ?")
        params.append(category)

    if status == 'complete':
        conditions.append("is_completed = 1")
    elif status == 'incomplete':
        conditions.append("is_completed = 0")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_date DESC"

    cursor.execute(query, params)
    tasks = cursor.fetchall()
    conn.close()

    return jsonify({
        'tasks': [dict(task) for task in tasks]
    })

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get single task by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'task': dict(task)})

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create new task"""
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (content, category, due_date, priority, is_completed, created_date)
        VALUES (?, ?, ?, ?, 0, ?)
    """, (
        data['content'],
        data['category'],
        data.get('due_date'),
        data.get('priority'),
        datetime.now().isoformat()
    ))

    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Auto-vectorize
    add_to_vector_store(
        'task',
        task_id,
        data['category'],
        data['content'],
        due_date=data.get('due_date')
    )

    return jsonify({'task': {'id': task_id, **data}}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task"""
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET content = ?, category = ?, due_date = ?, priority = ?
        WHERE id = ?
    """, (
        data['content'],
        data['category'],
        data.get('due_date'),
        data.get('priority'),
        task_id
    ))
    conn.commit()
    conn.close()

    # Update vector store
    update_in_vector_store(
        f'task_{task_id}',
        data['category'],
        data['content']
    )

    return jsonify({'task': {'id': task_id, **data}})

@app.route('/api/tasks/<int:task_id>/complete', methods=['PATCH'])
def toggle_task_complete(task_id):
    """Toggle task completion status"""
    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks
        SET is_completed = ?
        WHERE id = ?
    """, (data['is_completed'], task_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    # Remove from vector store
    remove_from_vector_store(f'task_{task_id}')

    return jsonify({'success': True})

# Notes endpoints (similar structure)
@app.route('/api/notes', methods=['GET'])
def get_notes():
    # Similar to get_tasks
    pass

@app.route('/api/notes', methods=['POST'])
def create_note():
    # Similar to create_task
    pass

# Categories endpoint
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    return jsonify({
        'categories': [
            {'name': cat, 'parent': None, 'level': 1}
            for cat in CATEGORIES.keys()
        ]
    })

# Search endpoint
@app.route('/api/search', methods=['GET'])
def search():
    """Semantic search using RAG"""
    query = request.args.get('q')
    search_type = request.args.get('type', 'all')
    limit = int(request.args.get('limit', 10))

    if not query:
        return jsonify({'error': 'Query required'}), 400

    results = rag_query(query, limit=limit)

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Step 6: Create Basic Components

**DashboardLayout.tsx:**
```tsx
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

export function DashboardLayout() {
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
```

**TaskCard.tsx:**
```tsx
import { Card } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';
import { Pencil, Trash2 } from 'lucide-react';
import { CategoryBadge } from '@/components/shared/CategoryBadge';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number, isCompleted: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

export function TaskCard({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) {
  return (
    <Card className="p-4">
      <div className="flex items-start gap-3">
        <Checkbox
          checked={task.is_completed}
          onCheckedChange={(checked) =>
            onToggleComplete(task.id, checked as boolean)
          }
        />
        <div className="flex-1">
          <p className={task.is_completed ? 'line-through text-muted-foreground' : ''}>
            {task.content}
          </p>
          <div className="mt-2 flex items-center gap-2">
            <CategoryBadge category={task.category} />
            {task.due_date && (
              <span className="text-sm text-muted-foreground">
                Due: {new Date(task.due_date).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>
        <div className="flex gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onEdit(task)}
          >
            <Pencil className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDelete(task.id)}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </Card>
  );
}
```

---

## Key Features Detail

### 1. View All Data

**Tasks View:**
- List all tasks from database
- Show: content, category, due date, completion status
- Filter by: category, status (complete/incomplete), due date
- Sort by: created date, due date, category

**Notes View:**
- Grid or list layout
- Show: content, category, created date
- Filter by: category
- Sort by: created date, category

**Calendar View:** (Placeholder for Phase 2B)
- Month view calendar component
- Empty state message: "Calendar integration coming in Phase 2B"

### 2. Edit Functionality

**Edit Task:**
- Click edit button on task card
- Modal/dialog opens with form
- Fields: content (textarea), category (select), due date (date picker), priority (select)
- Save button → API PUT request → updates database + vector store
- Cancel button → closes dialog

**Edit Note:**
- Click edit button on note card
- Modal opens with form
- Fields: content (textarea), category (select)
- Save → API PUT request
- Cancel → closes

**Inline Editing (Optional enhancement):**
- Click on content to edit in-place
- Press Enter to save, Esc to cancel

### 3. Mark Tasks Complete

**Checkbox Interaction:**
- Click checkbox on task card
- Optimistic update (UI updates immediately)
- API PATCH request in background
- If fails, revert UI change and show error toast

**Visual Indication:**
- Completed tasks: strikethrough text, muted color
- Incomplete tasks: normal text, full color
- Optional: Move completed tasks to bottom or separate section

### 4. Move Between Categories

**Dropdown Method:**
- Category badge is clickable
- Opens dropdown menu with all 41 categories
- Select new category → API PUT request → updates task/note
- Visual feedback: badge animates to new category

**Drag-and-Drop (Future enhancement):**
- Drag task card to category in sidebar
- Drop → updates category
- Nice animation

### 5. Search Functionality

**Search Bar:**
- Prominent in header
- Type query → shows results as you type (debounced)
- Uses semantic RAG search
- Shows results grouped by type (tasks, notes)
- Click result → navigates to item or opens quick view

**Search Page:**
- Dedicated page for advanced search
- Filters: type (tasks/notes), category, date range
- Results with similarity scores
- Highlight matching text

---

## Data Flow Examples

### Example 1: Creating a Task

```
User clicks "New Task" button
  ↓
CreateTaskDialog opens
  ↓
User fills form:
  - Content: "Buy groceries for Preeti"
  - Category: "Preeti - Tasks"
  - Due: "ASAP"
  ↓
User clicks "Create"
  ↓
Frontend validates form (Zod schema)
  ↓
API POST /api/tasks
  {
    content: "Buy groceries for Preeti",
    category: "Preeti - Tasks",
    due_date: "ASAP"
  }
  ↓
Backend (api_server.py):
  1. Insert into data.db
  2. Call add_to_vector_store()
  3. Return new task with ID
  ↓
Frontend:
  1. React Query cache invalidates
  2. Task list re-fetches
  3. New task appears in UI
  4. Success toast shows
  5. Dialog closes
```

### Example 2: Toggling Task Complete

```
User clicks checkbox on task
  ↓
Frontend (optimistic update):
  1. Immediately update UI
  2. Show task as completed
  ↓
API PATCH /api/tasks/123/complete
  { is_completed: true }
  ↓
Backend:
  1. Update data.db
  2. Return success
  ↓
Frontend:
  - If success: keep UI as is
  - If error: revert UI, show error toast
```

### Example 3: Semantic Search

```
User types in search bar:
  "show me preeti tasks"
  ↓
Frontend (debounced):
  Wait 300ms for user to stop typing
  ↓
API GET /api/search?q=show+me+preeti+tasks
  ↓
Backend:
  1. Call rag_query() from vector_store.py
  2. Get embeddings from OpenAI
  3. Calculate similarity
  4. Return top 10 results
  ↓
Frontend:
  1. Display results grouped by type
  2. Show similarity scores
  3. Highlight "Preeti" in results
```

---

## Error Handling

### API Errors

```typescript
// Use React Query error handling
const { data, error, isError } = useQuery({
  queryKey: ['tasks'],
  queryFn: tasksApi.getAll,
  onError: (error) => {
    toast.error('Failed to load tasks');
  }
});
```

### Network Errors

- Show toast notification
- Retry button for failed requests
- Offline indicator when API unreachable

### Validation Errors

```typescript
// Use Zod for form validation
const taskSchema = z.object({
  content: z.string().min(1, 'Content is required'),
  category: z.string().min(1, 'Category is required'),
  due_date: z.string().nullable(),
  priority: z.enum(['High', 'Medium', 'Low']).nullable(),
});
```

---

## Testing Strategy

### Manual Testing Checklist

**Tasks:**
- [ ] Can view all tasks
- [ ] Can create new task
- [ ] Can edit task content
- [ ] Can edit task category
- [ ] Can edit task due date
- [ ] Can mark task complete
- [ ] Can mark task incomplete
- [ ] Can delete task
- [ ] Can filter by category
- [ ] Can filter by status
- [ ] Can filter by due date

**Notes:**
- [ ] Can view all notes
- [ ] Can create new note
- [ ] Can edit note content
- [ ] Can edit note category
- [ ] Can delete note
- [ ] Can filter by category

**Search:**
- [ ] Search returns relevant results
- [ ] Search works for tasks
- [ ] Search works for notes
- [ ] Results show correct similarity

**Integration:**
- [ ] Changes in dashboard appear in Telegram bot
- [ ] Changes in Telegram bot appear in dashboard
- [ ] Vector store stays in sync
- [ ] No database corruption

---

## Performance Considerations

### Frontend Optimization

1. **Code Splitting:**
   ```tsx
   // Lazy load pages
   const TasksPage = lazy(() => import('./pages/TasksPage'));
   const NotesPage = lazy(() => import('./pages/NotesPage'));
   ```

2. **Virtualization (if >100 items):**
   - Use `@tanstack/react-virtual` for long lists
   - Only render visible items

3. **Memoization:**
   ```tsx
   const TaskList = React.memo(({ tasks }) => {
     // Prevent unnecessary re-renders
   });
   ```

4. **Debouncing:**
   ```tsx
   const debouncedSearch = useDe bounce((query) => {
     searchApi.search(query);
   }, 300);
   ```

### Backend Optimization

1. **Database Indexing:**
   ```sql
   CREATE INDEX idx_tasks_category ON tasks(category);
   CREATE INDEX idx_tasks_due_date ON tasks(due_date);
   CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
   ```

2. **Query Optimization:**
   - Use WHERE clauses efficiently
   - Limit results when appropriate
   - Avoid N+1 queries

3. **Caching (future):**
   - Cache category list
   - Cache frequently accessed tasks

---

## Security Considerations

### Local Development

- No authentication needed (local only)
- API only accessible on localhost
- Database file has local file permissions

### Future Production (Optional)

If deploying publicly:
- Add JWT authentication
- Rate limiting on API
- Input sanitization
- SQL injection prevention (use parameterized queries)
- CORS restricted to specific origin

---

## Accessibility

### WCAG Compliance

1. **Keyboard Navigation:**
   - All actions accessible via keyboard
   - Logical tab order
   - Focus indicators visible

2. **Screen Readers:**
   - Semantic HTML
   - ARIA labels on interactive elements
   - Alt text for icons

3. **Color Contrast:**
   - AAA compliance for text
   - Don't rely on color alone for information

4. **Forms:**
   - Label all inputs
   - Error messages linked to fields
   - Clear validation feedback

---

## Deployment (Future)

### Local Development

**Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

**Backend:**
```bash
python scripts/api_server.py
# Runs on http://localhost:5000
```

### Production (Optional - Phase 3 or 4)

**Frontend:**
- Deploy to Vercel or Netlify
- Static site build: `npm run build`
- Auto-deploys on git push

**Backend:**
- Deploy to Render alongside Telegram bot
- Add API routes to existing service
- Or separate API service

---

## Success Metrics

### Functionality ✅

- [ ] Dashboard loads in <1 second
- [ ] All CRUD operations work
- [ ] Changes sync with Telegram bot
- [ ] Vector store stays updated
- [ ] Search returns relevant results
- [ ] No console errors
- [ ] No database errors

### UX ✅

- [ ] Clean, modern design
- [ ] Intuitive navigation
- [ ] Responsive on desktop
- [ ] Fast interactions (<100ms)
- [ ] Clear feedback on actions
- [ ] Error states handled gracefully

### Code Quality ✅

- [ ] TypeScript types used throughout
- [ ] Components are reusable
- [ ] Code is well-organized
- [ ] No linting errors
- [ ] Follows React best practices

---

## Future Enhancements (Post-Phase 2D)

1. **Dark Mode** - Toggle between light/dark themes
2. **Bulk Operations** - Select multiple tasks and complete/delete
3. **Drag-and-Drop** - Reorder tasks, drag to change category
4. **Recurring Tasks** - Set tasks to repeat
5. **Task Templates** - Save frequently used tasks as templates
6. **Export** - Export tasks/notes to CSV or PDF
7. **Analytics** - Dashboard stats (tasks completed, by category, etc.)
8. **Notifications** - Browser notifications for due tasks
9. **Offline Mode** - Service worker for offline access
10. **Mobile App** - React Native or PWA

---

## Questions to Answer Before Starting

### User Questions:

1. **Calendar Integration:**
   - Include calendar in Phase 2D (empty/placeholder)?
   - Or wait until Phase 2B calendar integration is done?
   - **Suggestion:** Include empty placeholder for now

2. **Priority:**
   - Start with Tasks only (Day 1)?
   - Or build Tasks + Notes together?
   - **Suggestion:** Tasks first, then Notes

3. **Authentication:**
   - Needed for local dev?
   - **Suggestion:** No auth for local

4. **Database:**
   - Use existing data.db shared with bot?
   - **Answer:** Yes

### Technical Decisions:

1. **Component Library:**
   - shadcn/ui confirmed ✅
   - Use MCP for installation ✅

2. **State Management:**
   - React Query for server state ✅
   - React Context for UI state (theme, etc.) ✅

3. **Routing:**
   - React Router ✅
   - Pages: Tasks, Notes, Calendar, Search ✅

4. **Forms:**
   - React Hook Form + Zod ✅

---

## Next Steps

Once user confirms approach:

1. **Set up shadcn MCP** in Claude Code
2. **Create frontend directory** and initialize Vite
3. **Install dependencies** and configure shadcn/ui
4. **Create api_server.py** with first endpoints
5. **Build TasksPage** and test end-to-end
6. **Iterate** based on user feedback

---

## Summary

This plan provides:
- ✅ Complete technical specification
- ✅ Day-by-day timeline
- ✅ Detailed component breakdown
- ✅ API specification
- ✅ Code examples
- ✅ Testing checklist
- ✅ Clear success criteria

**Ready to build a beautiful dashboard that makes Life OS even more powerful!**

---

**Document Status:** Ready for Implementation
**Next Action:** User reviews plan and answers questions
**Then:** Begin Day 1 implementation!
