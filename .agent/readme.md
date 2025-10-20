# Life OS Documentation Index
## Your Personal Operating System Knowledge Base

**Created:** October 18, 2024
**Purpose:** Organize everything in your life - nothing forgotten, always visible
**Philosophy:** Capture, organize, visualize. Build knowledge over time.

---

## 📁 Folder Structure

```
life-os/
├── inbox/           # Raw input - paste organized dumps here
│   └── processed/   # Archive of what's been organized
├── data/            # All your life data, organized by category
├── documents/       # Photos, PDFs, receipts, contracts
├── .agent/          # You are here - knowledge base
└── dashboard/       # Visual interface (open index.html)
```

---

## 🎯 Quick Start: Adding New Items

### Method 1: Organized Dump (Recommended)
1. Speak your brain dump → Get transcript
2. Process with temp Claude (see `system/transcript-prompt.md`)
3. Paste organized output into `inbox/raw.md`
4. Tell organization agent to process
5. Answer any clarifying questions
6. Everything gets filed automatically

### Method 2: Direct Input
1. Tell organization agent what to add
2. Agent asks clarifying questions
3. Agent files it for you

### Method 3: Manual
1. Navigate to correct category folder in `data/`
2. Edit the appropriate `.md` file
3. Dashboard will show it on next refresh

---

## 📚 System Documentation

### Core Workflow
| Doc | When to Read | Purpose |
|-----|--------------|---------|
| `core-principles.md` | Before starting | Understand how Life OS works |
| `organization-rules.md` | Reference | How items get categorized |
| `keyword-mapping.md` | Reference | Your specific terms & mappings |

### Structure & Formats
| Doc | When to Read | Purpose |
|-----|--------------|---------|
| `category-tree.md` | When adding categories | Current folder structure |
| `data-format-spec.md` | When adding data | How to format different entry types |
| `transcript-prompt.md` | Every brain dump | Template for Claude processing |

---

## 🤖 Organization Agent Guidelines

### How It Works
1. Reads `inbox/raw.md` when you tell it to organize
2. Parses items based on `organization-rules.md`
3. Asks questions about ambiguous items
4. Learns your preferences (updates `keyword-mapping.md`)
5. Files items into correct `data/` folders
6. Updates dashboard
7. Logs actions to `logs/organization-log.md`

### Agent Philosophy
✅ **Agent executes** - You decide
✅ **Agent asks** - Doesn't assume
✅ **Agent learns** - Remembers your answers
✅ **Agent documents** - Logs everything

❌ **Agent doesn't make decisions** - You do
❌ **Agent doesn't analyze** - Just organizes (for now)

---

## 📊 Dashboard

**Location:** `dashboard/index.html`

**Views:**
- **Today** - Critical items due today
- **Next 7 Days** - Upcoming deadlines chronologically
- **This Month** - Current month overview
- **Life Areas** - All categories with counts (clickable)
- **Quick Add** - Text input for new items

**How to Use:**
- Open `dashboard/index.html` in browser
- Keep it open on your desktop
- Refresh to see updates
- Click categories to expand details

---

## 📝 Data Organization

### Life Categories

**People:**
- `family/` - 7 family members
- `friends/` - 11 core friends
- `preeti/` - Fiancé

**Major Life Areas:**
- `wedding/` - May 3, 2026 (multi-event Indian wedding)
- `work/` - Projects, tasks, governance
- `home/` - Bills, tenant, maintenance
- `buddy/` - Dog health, insurance, care

**Activities:**
- `fitness/` - Gym, jujitsu
- `hobbies/` - NFL, video games, guitar, photography
- `side-hustles/` - Betting, Princeton AI Partners
- `personal-projects/` - AI projects, websites

### File Types

Each person/category can have:
- `notes.md` - General notes
- `tasks.md` - Things to do
- `dates.md` - Important dates
- `conversations.md` - Important things to remember
- Custom files as needed

---

## 🔄 Documentation Workflow

### Before Adding Data
1. Check if category exists in `data/`
2. Check `category-tree.md` for structure
3. Check `data-format-spec.md` for format

### During Data Entry
1. Add to `inbox/raw.md` or tell agent
2. Agent processes and asks questions
3. Review where items were filed
4. Dashboard updates automatically

### After Completion
1. Items archived to `inbox/processed/[date].md`
2. Organization logged to `logs/organization-log.md`
3. Keyword mapping updated if new terms learned

---

## 🚀 Future Upgrades

Planned enhancements:
- [ ] Telegram bot integration (add items via message)
- [ ] Advanced betting analytics
- [ ] Financial tracking & budgeting
- [ ] Wedding detailed planning tools
- [ ] Calendar integration
- [ ] Reminders & notifications
- [ ] Search functionality
- [ ] Mobile-friendly dashboard

---

## 🎯 Philosophy

### Capture Everything
Every responsibility, task, idea, deadline - nothing forgotten.

### Organize Naturally
Categories match how you think about your life.

### Visualize Clearly
Dashboard shows what matters right now.

### Build Knowledge
System gets smarter as you use it.

### Stay Flexible
Easy to add categories, change structure, upgrade features.

---

## 🔗 Related Docs

**System Documentation:**
- `system/core-principles.md` - How Life OS works
- `system/organization-rules.md` - Categorization logic
- `system/keyword-mapping.md` - Your terms
- `system/category-tree.md` - Folder structure
- `system/data-format-spec.md` - Entry formats

**Decision Log:**
- `decisions/structure-choices.md` - Why this approach

**Processing:**
- `inbox-processor/instructions.md` - How organization works
- `logs/organization-log.md` - What's been organized

---

## 📞 Quick Reference Card

**Add New Item?**
1. Paste in `inbox/raw.md` → Tell agent to organize
2. Or tell agent directly
3. Agent files it → Dashboard updates

**Check What's Coming Up?**
1. Open `dashboard/index.html`
2. See Today, Next 7 Days, This Month

**Find Something?**
1. Check dashboard for category
2. Navigate to `data/[category]/`
3. Open relevant `.md` file

**Stuck?**
1. Check this readme
2. Check `system/` docs
3. Ask organization agent

---

**Last Updated:** October 18, 2024
**Version:** 1.0
**Status:** Active
**Next Review:** As needed (update when structure changes)
