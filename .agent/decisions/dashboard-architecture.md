# Decision: Dashboard Architecture

**Date:** 2025-10-18
**Status:** Implemented
**Decision Makers:** User + Claude

## Context

Life OS needed a visual interface to see tasks, deadlines, and life areas at a glance. Pure markdown files work for storage but lack temporal organization (Today, Next 7 Days, This Month) and visual overview.

## Problem Statement

**Requirements:**
- Visual dashboard showing temporal views of tasks
- Today section (immediate focus)
- Next 7 Days (upcoming deadlines)
- This Month (broader planning)
- Life Areas grid (category overview with counts)
- Must be simple to use and share with friends
- Local-first (no cloud dependency)
- Fast to load and update

## Decision

Build an **HTML/CSS/JavaScript dashboard** with a **Python data builder** and **local web server**.

### Architecture

```
data/*.md files
      ↓
build-dashboard-data.py (parses markdown → JSON)
      ↓
dashboard/data.json
      ↓
Local Python web server (http://localhost:8000)
      ↓
dashboard/index.html + script.js (loads JSON, displays UI)
```

## Alternatives Considered

### Option A: Static HTML (file:// protocol)
**Approach:** Open index.html directly in browser

**Pros:**
- Simple, no server needed
- Double-click to open
- Fast

**Cons:**
- CORS blocks loading data.json
- Browser security prevents JavaScript file access
- Would need to embed data in HTML directly (messy)

**Why rejected:** Browser security restrictions prevent JSON loading

### Option B: Electron App
**Approach:** Package as desktop application

**Pros:**
- Full file system access
- Native app experience
- No CORS issues

**Cons:**
- Complex packaging (100MB+ download)
- Platform-specific builds (Windows, Mac, Linux)
- Overkill for this use case
- Hard to share with friends (requires install)

**Why rejected:** Too heavy for simple dashboard

### Option C: VS Code Extension
**Approach:** Build extension that renders dashboard in VS Code

**Pros:**
- Already in VS Code editing markdown
- Full file access
- Can edit and view in one place

**Cons:**
- Requires VS Code
- Complex extension API
- Not standalone
- Hard to keep open while working elsewhere

**Why rejected:** Too tightly coupled to VS Code

### Option D: Cloud-Hosted Dashboard
**Approach:** Deploy to Netlify/Vercel, upload data

**Pros:**
- Access from anywhere
- No local server needed
- Shareable URL

**Cons:**
- Defeats "local-first" philosophy
- Privacy concerns (life data in cloud)
- Requires internet
- Complex sync mechanism

**Why rejected:** User wants local control

### Option E: Local Web Server (CHOSEN)
**Approach:** Python HTTP server serving dashboard

**Pros:**
- No CORS issues
- Simple built-in Python server
- Localhost only (privacy)
- Friends just need Python (ubiquitous)
- Fast and lightweight

**Cons:**
- Terminal must stay open
- Extra step to start server

**Why chosen:** Best balance of simplicity and functionality

## Implementation Details

### Technology Stack

**Backend:** Python
- Built-in `http.server` module (no dependencies!)
- Runs on port 8000
- Simple one-liner: `python -m http.server 8000`

**Data Builder:** Python script
- Walks data/ folder
- Parses markdown for tasks (checkbox items)
- Extracts due dates, priorities, categories
- Outputs structured JSON

**Frontend:** Vanilla HTML/CSS/JS
- No frameworks (fast, simple)
- Pure JavaScript (no build step)
- Responsive CSS Grid
- Modern browser features only

### Data Flow

1. User edits markdown files
2. Runs: `python scripts/build-dashboard-data.py`
3. Script generates `dashboard/data.json`
4. User runs: `refresh-dashboard.bat` (or `.sh`)
5. Script starts web server and opens browser
6. Dashboard loads data.json via fetch()
7. JavaScript populates UI sections

### Refresh Script Design

**Windows (`refresh-dashboard.bat`):**
```batch
1. Run build-dashboard-data.py
2. Start http.server on port 8000
3. Wait 2 seconds
4. Open http://localhost:8000/dashboard/ in browser
5. Keep terminal open (server runs)
```

**Mac/Linux (`refresh-dashboard.sh`):**
- Same flow but with bash syntax
- Uses `open` (Mac) or `xdg-open` (Linux) for browser

### Why Local Server Specifically

**CORS (Cross-Origin Resource Sharing) Issue:**
- Browsers block `fetch('data.json')` when using `file://` protocol
- This is a security feature to prevent local file access exploits
- Only HTTP/HTTPS origins can load resources

**Solution:**
- Local web server provides `http://localhost:8000` origin
- fetch() works perfectly
- Still completely local (localhost only)
- No network access required

## Dashboard UI Design

### Sections

**1. Today**
- Shows tasks due today
- Red accent (urgent)
- Empty state: "No items due today 🎉"

**2. Next 7 Days**
- Upcoming deadlines
- Orange/yellow accent (warning)
- Sorted by date
- Shows day of week + date

**3. This Month**
- Broader view
- Blue accent (informational)
- Month-level planning

**4. Life Areas Grid**
- 11 category cards: Family, Friends, Preeti, Wedding, Work, Side Hustles, Home, Buddy, Fitness, Hobbies, Projects
- Shows count of items
- Shows status (e.g., "3 critical" for work)
- Click to view details (Phase 2)

**5. Quick Add**
- Text area for quick capture
- Copies to clipboard
- User pastes into inbox/raw.md
- Organization agent processes

### Why This Layout

**Temporal Priority:**
- User said: "What's happening NOW is most important"
- Today section first (immediate focus)
- Then week view (planning horizon)
- Then month (longer term)

**Life Areas Grid:**
- Visual overview of all categories
- Counts show what needs attention
- Color coding for priority
- Click for details (future)

## Technical Decisions

### Python Data Builder

**Why Python:**
- User already has Python (for data science background)
- Simple script, no dependencies
- Friends likely have Python
- Easy to extend

**Why JSON Output:**
- JavaScript natively parses JSON
- Human-readable for debugging
- Easy to inspect
- Future Telegram bot can use same format

**Parsing Strategy:**
- Regex for checkbox items: `- [ ] Task`
- Look-ahead for metadata (Due:, Priority:, Notes:)
- Extract dates using multiple format patterns
- Categorize by file path

### Dashboard JavaScript

**Why Vanilla JS:**
- No build step (no webpack, no npm)
- Fast load (no framework overhead)
- Simple for friends to understand
- Modern browsers have all features needed

**Data Loading:**
```javascript
fetch('data.json')
  .then(res => res.json())
  .then(data => populateDashboard(data))
```

**Dynamic UI Generation:**
- Create DOM elements from JSON
- Populate timeline views
- Update category card counts
- Show empty states when no data

### Styling Approach

**Why CSS Variables:**
- Easy theme switching (future dark mode)
- Consistent colors throughout
- Readable code

**Why CSS Grid:**
- Responsive layout
- Auto-fit columns
- Clean code

**Why No CSS Framework:**
- Tailwind/Bootstrap adds bulk
- Custom styling is lightweight
- Full control over design

## Benefits Achieved

1. **Visual Clarity** - See everything at a glance
2. **Temporal Organization** - Today/Week/Month views
3. **Fast** - Loads in milliseconds
4. **Simple** - Just double-click refresh script
5. **Shareable** - Friends copy folder + run script
6. **Private** - Localhost only, no cloud
7. **Future-Proof** - JSON format, standard tech

## Risks & Mitigations

**Risk:** Server port 8000 already in use
**Mitigation:** Error message shows, user can kill other process or change port

**Risk:** User forgets to rebuild data after editing markdown
**Mitigation:** Dashboard shows stale data timestamp. Refresh script rebuilds automatically.

**Risk:** Server stops when terminal closes
**Mitigation:** Documentation emphasizes keeping terminal open. Can run in background if needed.

**Risk:** Complex setup for friends
**Mitigation:** Single script handles everything. Python is only requirement.

## Performance

**Load Time:** < 100ms
- Minimal HTML
- Small CSS file
- Vanilla JS (no framework parsing)
- JSON is tiny (63 tasks = ~10KB)

**Build Time:** < 1 second
- Python script processes 27 files in ~500ms
- Generates JSON instantly

**Refresh Time:** 2 seconds total
- 1 second to rebuild data
- 1 second to start server
- Browser opens immediately

## Future Enhancements

**Phase 2 - Life Area Details:**
- Click category card → modal/panel
- Show all tasks + notes for category
- Inline expansion of details

**Phase 3 - Live Editing:**
- Edit tasks directly in dashboard
- Save to markdown via Python backend API
- WebSocket for live updates (no page refresh)

**Potential:**
- Dark mode toggle
- Custom date range filters
- Search across all tasks
- Calendar view
- Mobile-responsive (already mostly done)
- Desktop notifications for deadlines

## Lessons Learned

**What Worked:**
- Local server solves CORS elegantly
- Refresh script makes it one-click simple
- Temporal views match user's mental model
- Vanilla JS is fast and simple

**What Surprised Us:**
- CORS issue wasn't obvious initially
- User opened file:// directly and got errors
- Quick pivot to local server fixed everything

**What to Improve:**
- Could add auto-rebuild on file change (file watcher)
- Could embed server in Electron later if needed
- Could add PWA features for offline support

## References

- CORS documentation: Why file:// doesn't work
- User feedback: "Dashboard needs to show what's happening NOW"
- Python http.server docs: Simple built-in server
- Modern JS fetch API: Standard data loading

## Conclusion

The local web server + Python builder architecture is the sweet spot:
- Simple enough for non-technical friends
- Powerful enough for advanced features later
- Fast and responsive
- Completely local and private
- Built on standard, ubiquitous tech

Key insight: **The "extra step" of starting a server is worth it** for the clean architecture and future flexibility it enables. The refresh script makes it feel simple anyway.
