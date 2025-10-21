# Next Session: Dashboard Development (Phase 2D)

**Date Created:** October 21, 2025
**Updated:** October 21, 2025 (User preferences confirmed!)
**Status:** ✅ Ready to Start - All decisions made
**Priority:** High - User Interface for Life OS v1.0

---

## ✅ User Confirmed Approach

1. **Calendar:** Include UI placeholder (ready for Phase 2B)
2. **Priority:** Tasks first (Day 1), then Notes (Day 2)
3. **Database:** Shared data.db with Telegram bot ✅
4. **Authentication:** No login needed - local only

**See `Parth_Learning_Databases.md` for detailed explanation of how SQLite works!**

---

## 🎯 Session Goal

Build a **simple, clean, modern dashboard** using React.js + shadcn/ui to interact with Life OS data.

**User Request:**
> "we will continue tomorrow with a react js shadcn style dashboard where I can actually see all my data and stuff. I want a very very simple dashboard where I can edit all my stuff, see my calendar, and mark tasks as complete. also move tasks/notes around if needed. just a very clean modern customizable interactive dashboard with my database. this is also going to be in phase 2"

---

## 📋 Dashboard Requirements

### Core Features (Must-Have)

1. **View All Data**
   - Display all tasks from database
   - Display all notes from database
   - Display calendar events (from Google Calendar via MCP)
   - Filter by category
   - Search functionality

2. **Edit Functionality**
   - Edit task content
   - Edit task due dates
   - Edit task categories
   - Edit note content
   - Edit note categories
   - Delete tasks/notes

3. **Task Management**
   - Mark tasks as complete
   - Mark tasks as incomplete
   - Visual indication of completion status

4. **Organization**
   - Move tasks between categories
   - Move notes between categories
   - Drag-and-drop interface (optional, nice-to-have)

5. **Calendar Integration**
   - Display Google Calendar events
   - Create new events from dashboard
   - Edit existing events
   - Visual calendar view

### Design Principles

- ✨ **Very simple** - No feature bloat
- 🎨 **Clean and modern** - shadcn/ui aesthetic
- ⚙️ **Customizable** - User can adjust views
- 🖱️ **Interactive** - Smooth, responsive UX
- 📱 **Responsive** - Works on different screen sizes

---

## 🏗️ Proposed Architecture

### Tech Stack

**Frontend:**
- React.js (with Vite for fast dev)
- shadcn/ui (component library)
- Tailwind CSS (styling)
- TypeScript (type safety)
- React Query / TanStack Query (data fetching)

**Backend API:**
- Flask REST API (already have flask in requirements.txt)
- Endpoints to interact with SQLite database
- CORS enabled for local development

**Database:**
- SQLite (existing data.db)
- Same database used by Telegram bot
- Read/write access via API

**Calendar:**
- Google Calendar MCP integration
- API endpoints to fetch/create/update events

### Project Structure

```
life-os/
├── frontend/                    # React dashboard
│   ├── src/
│   │   ├── components/         # shadcn/ui components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskCard.tsx
│   │   │   ├── NoteList.tsx
│   │   │   ├── Calendar.tsx
│   │   │   └── CategoryFilter.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Tasks.tsx
│   │   │   ├── Notes.tsx
│   │   │   └── Calendar.tsx
│   │   ├── lib/
│   │   │   └── api.ts          # API client
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── scripts/
│   ├── api_server.py           # Flask REST API (NEW)
│   ├── telegram_bot.py         # Existing
│   └── ...                     # Other scripts
│
└── data/
    └── data.db                 # Shared database
```

---

## 🛠️ Implementation Plan

### Step 1: Set Up React + Vite + shadcn/ui

1. Create `frontend/` directory
2. Initialize Vite + React + TypeScript
3. Install shadcn/ui and configure
4. Set up Tailwind CSS
5. Install React Query for data fetching

**Commands:**
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npx shadcn-ui@latest init
npm install @tanstack/react-query
```

### Step 2: Build Flask REST API

Create `scripts/api_server.py` with endpoints:

**Tasks:**
- `GET /api/tasks` - List all tasks
- `GET /api/tasks/:id` - Get single task
- `POST /api/tasks` - Create task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PATCH /api/tasks/:id/complete` - Mark complete/incomplete

**Notes:**
- `GET /api/notes` - List all notes
- `GET /api/notes/:id` - Get single note
- `POST /api/notes` - Create note
- `PUT /api/notes/:id` - Update note
- `DELETE /api/notes/:id` - Delete note

**Categories:**
- `GET /api/categories` - List all categories

**Calendar:**
- `GET /api/calendar/events` - List events
- `POST /api/calendar/events` - Create event
- `PUT /api/calendar/events/:id` - Update event
- `DELETE /api/calendar/events/:id` - Delete event

**Search:**
- `GET /api/search?q=query` - Semantic search via RAG

### Step 3: Build Dashboard UI Components

**Using shadcn/ui components:**

1. **Layout**
   - Sidebar navigation
   - Main content area
   - Header with search

2. **Task Components**
   - Task list with filters
   - Task card (editable)
   - Completion checkbox
   - Category badges

3. **Note Components**
   - Note list
   - Note card (editable)
   - Category badges

4. **Calendar Component**
   - Month view
   - Day view
   - Event list
   - Create event modal

5. **Shared Components**
   - Category filter dropdown
   - Search bar
   - Edit modal
   - Delete confirmation

### Step 4: Integrate with Database

1. Reuse existing `db.py` functions
2. Add API layer in Flask
3. Enable CORS for local dev
4. Test CRUD operations
5. Ensure Telegram bot and dashboard share same DB

### Step 5: Calendar Integration

1. Use Google Calendar MCP
2. Fetch events via MCP
3. Display in calendar view
4. Allow creation from dashboard
5. Sync with Google Calendar

### Step 6: Polish & Deploy

1. Add loading states
2. Add error handling
3. Mobile responsive design
4. Optional: Deploy frontend to Vercel/Netlify
5. Optional: Deploy API alongside Telegram bot on Render

---

## 📐 Design Mockup (Conceptual)

```
┌─────────────────────────────────────────────────────────────┐
│  Life OS Dashboard                     [Search...]  [@User]  │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│ 📋 Tasks │  Today's Tasks (5)                               │
│ 📝 Notes │  ┌─────────────────────────────────────┐         │
│ 📅 Calendar│ │ ☐ Buy groceries for Preeti      │ [Edit]│    │
│ 🔍 Search│  │    📁 Preeti - Tasks  📅 ASAP      │       │  │
│          │  └─────────────────────────────────────┘         │
│ Filter:  │  ┌─────────────────────────────────────┐         │
│ [All]▾   │  │ ☐ Call Mom                         │ [Edit]│  │
│          │  │    📁 Family  📅 2025-10-22         │       │  │
│          │  └─────────────────────────────────────┘         │
│          │                                                   │
│          │  Recent Notes (3)                                │
│          │  ┌─────────────────────────────────────┐         │
│          │  │ I love the eagles                   │ [Edit]│  │
│          │  │ 📁 Hobbies - Sports                 │       │  │
│          │  └─────────────────────────────────────┘         │
│          │                                                   │
└──────────┴──────────────────────────────────────────────────┘
```

---

## 🔧 Technical Considerations

### Database Access

**Challenge:** Telegram bot and dashboard both need DB access

**Solution:**
1. Both read/write to same `data.db` file
2. SQLite handles concurrent access
3. API server runs separately from Telegram bot
4. Use locks/transactions for writes

### Auto-Vectorization

**When data changes via dashboard:**
- Update database via API
- Trigger auto-vectorization (call vector_store.py functions)
- Keep vector store in sync

**API should:**
- Update DB
- Call `add_to_vector_store()` or `remove_from_vector_store()`
- Return updated data

### Development vs Production

**Local Development:**
- Frontend: `http://localhost:5173` (Vite dev server)
- API: `http://localhost:5000` (Flask dev server)
- Database: Local `data.db`

**Production (Optional for Phase 2D):**
- Frontend: Vercel/Netlify (static hosting)
- API: Render (alongside Telegram bot)
- Database: Same SQLite on Render

---

## 📊 Success Metrics

### Functionality
- [ ] Can view all tasks and notes
- [ ] Can edit tasks and notes
- [ ] Can mark tasks complete/incomplete
- [ ] Can move tasks/notes between categories
- [ ] Can view calendar events
- [ ] Can create calendar events from dashboard
- [ ] Search works (semantic via RAG)

### UX
- [ ] Clean, modern design
- [ ] Responsive on desktop
- [ ] Fast loading (<1 second)
- [ ] Smooth interactions
- [ ] No console errors

### Integration
- [ ] Shares database with Telegram bot
- [ ] Changes sync between bot and dashboard
- [ ] Vector store stays updated
- [ ] Calendar syncs with Google Calendar

---

## 🚀 Phase Placement

**This is Phase 2D: Dashboard**

**Updated Phase 2 Roadmap:**

- ✅ **Phase 2A:** RAG System (COMPLETE - v1.0)
- 📅 **Phase 2B:** Google Calendar Integration (1-2 days)
- 📅 **Phase 2C:** Calendar + RAG (1 day)
- 🎯 **Phase 2D:** Dashboard (NEW - 2-3 days)

**Rationale:**
- Dashboard provides visual interface for existing v1.0 functionality
- Natural progression after calendar integration
- Enables easier data management than Telegram alone
- Sets foundation for future features

---

## 📦 Deliverables

By end of Phase 2D, we should have:

1. **React Dashboard**
   - Clean, modern UI with shadcn/ui
   - Task management
   - Note management
   - Calendar view
   - Search functionality

2. **Flask REST API**
   - Full CRUD for tasks and notes
   - Calendar endpoints
   - Search endpoint
   - CORS configured

3. **Documentation**
   - API documentation
   - Dashboard setup guide
   - Development guide
   - Deployment guide (optional)

4. **Version Tag**
   - v1.1.0 or v1.2.0 depending on calendar integration status

---

## 🎯 First Steps Tomorrow

### 1. Confirm Scope
- Review requirements
- Agree on feature set
- Decide on deployment (local-only or production)

### 2. Set Up Project
- Create `frontend/` directory
- Initialize Vite + React + TypeScript
- Install and configure shadcn/ui
- Set up Tailwind CSS

### 3. Build Basic API
- Create `scripts/api_server.py`
- Implement GET /api/tasks endpoint
- Test with existing database
- Enable CORS for dev

### 4. Build First Component
- Create TaskList component
- Fetch tasks from API
- Display in clean shadcn/ui cards
- Test end-to-end

### 5. Iterate
- Add more endpoints
- Add more components
- Build out full dashboard
- Polish and test

---

## 💡 Design Inspirations

**shadcn/ui Examples:**
- https://ui.shadcn.com/examples/dashboard
- https://ui.shadcn.com/examples/tasks
- https://ui.shadcn.com/examples/cards

**Keep It Simple:**
- Focus on core functionality first
- Add features incrementally
- User feedback drives iteration

---

## 📝 Notes for Tomorrow

**User Wants:**
- Very simple (don't overcomplicate)
- Clean and modern (shadcn/ui perfect for this)
- Just view, edit, complete, move tasks/notes
- Calendar view
- Database integration

**Technical Approach:**
- Start with API endpoints
- Build UI component by component
- Test frequently
- Keep it simple and clean

**Remember:**
- v1.0 is working great
- Dashboard is enhancement, not replacement
- Telegram bot stays as primary interface
- Dashboard for when user wants visual overview

---

## ✅ Pre-Session Checklist

Before starting tomorrow:
- [ ] Review this handoff
- [ ] Confirm user requirements
- [ ] Check Node.js installed (for React)
- [ ] Check Python Flask working
- [ ] Review shadcn/ui docs
- [ ] Plan first component to build

---

**Ready to build a beautiful dashboard! 🎨**

**Current Status:** Life OS v1.0 stable and production-ready
**Next Goal:** Add visual dashboard for enhanced data interaction
**Phase:** 2D - Dashboard Development
**Timeline:** 2-3 days

---

**End of Handoff**
**See you tomorrow! 🚀**
