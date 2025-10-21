# 🔄 Restart Here - Phase 2D Dashboard Development

**Created:** October 21, 2025
**Purpose:** Continue building React dashboard after Claude Code restart

---

## ✅ What's Already Done

1. ✅ **shadcn MCP** added to config (needs restart to load)
2. ✅ **React + Vite + TypeScript** project created in `frontend/`
3. ✅ **shadcn/ui** configured with Tailwind CSS
4. ✅ **Flask API server** created with full CRUD endpoints
5. ✅ **API client** created with TypeScript types
6. ✅ **Git committed** - all progress saved

---

## 🚀 Quick Start After Restart

### Step 1: Verify shadcn MCP is Loaded
After restarting Claude Code, the shadcn MCP server should be active.

**Test it:**
- Ask Claude: "List available shadcn components"
- Or: "Add a card component"

### Step 2: Add shadcn/ui Components
Use natural language or CLI:

```bash
cd frontend
npx shadcn@latest add card button checkbox badge input textarea select dialog
```

**Components needed:**
- `card` - Task and note cards
- `button` - Actions
- `checkbox` - Task completion
- `badge` - Category tags
- `input` - Form fields
- `textarea` - Note content
- `select` - Category dropdown
- `dialog` - Edit modals

### Step 3: Start Development Servers

**Terminal 1 - Backend API:**
```bash
cd scripts
python api_server.py
```
Expected output:
```
🚀 Life OS API Server starting...
📊 Database: sqlite
🌐 CORS enabled for frontend development
📡 Server running on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Expected output:
```
VITE ready in XXX ms
➜  Local:   http://localhost:5173/
```

---

## 📝 Next Tasks (In Order)

### Task 1: Build TaskList Component
**File:** `frontend/src/components/TaskList.tsx`

**Features:**
- Fetch tasks using React Query
- Display in shadcn/ui cards
- Checkbox to mark complete
- Edit button → opens dialog
- Delete button with confirmation
- Category badge
- Due date display

### Task 2: Build TaskCard Component
**File:** `frontend/src/components/TaskCard.tsx`

Individual task display with actions.

### Task 3: Build TaskEditDialog
**File:** `frontend/src/components/TaskEditDialog.tsx`

Modal for editing task content, category, and due date.

### Task 4: Create React Query Hooks
**File:** `frontend/src/hooks/useTasks.ts`

```typescript
- useTasksQuery() - Fetch all tasks
- useCreateTask() - Create new task
- useUpdateTask() - Update task
- useDeleteTask() - Delete task
- useToggleTaskCompletion() - Toggle complete
```

### Task 5: Build Dashboard Layout
**File:** `frontend/src/App.tsx`

Main layout with sidebar navigation.

### Task 6: Repeat for Notes
Similar structure as tasks.

### Task 7: Add Search & Calendar Placeholder
Semantic search interface and calendar view.

---

## 📂 Key Files Reference

| File | Purpose |
|------|---------|
| `frontend/src/lib/api.ts` | API client with all endpoints |
| `frontend/src/lib/utils.ts` | Utility functions (cn helper) |
| `frontend/components.json` | shadcn/ui config |
| `frontend/tailwind.config.js` | Tailwind theme config |
| `scripts/api_server.py` | Flask REST API |
| `.agent/logs/phase-2d-progress.md` | Detailed progress report |

---

## 🔗 API Endpoints Available

```
Health:
  GET /api/health

Categories:
  GET /api/categories

Tasks:
  GET /api/tasks
  GET /api/tasks/:id
  POST /api/tasks
  PUT /api/tasks/:id
  PATCH /api/tasks/:id/complete
  DELETE /api/tasks/:id

Notes:
  GET /api/notes
  GET /api/notes/:id
  POST /api/notes
  PUT /api/notes/:id
  DELETE /api/notes/:id

Search:
  GET /api/search?q=<query>
```

---

## 💡 Tips for Continuing

1. **Use shadcn MCP** - Let Claude use natural language to add components
2. **Start with one component** - Build TaskList first, then expand
3. **Test frequently** - Run both servers and test in browser
4. **Follow the plan** - See `NEXT_SESSION_DASHBOARD.md` for full details

---

## 🎯 Session Goal

Build a clean, modern dashboard where you can:
- View all tasks and notes with filters
- Edit content, dates, categories
- Mark tasks complete/incomplete
- Delete items
- Semantic search via RAG
- Calendar placeholder

**Let's build this! 🚀**

---

## 📞 What to Say After Restart

> "Hey! Let's continue building the Phase 2D dashboard. We've set up React + shadcn/ui and created the Flask API. The shadcn MCP should now be loaded. Let's add the shadcn/ui components we need and start building the TaskList component!"

