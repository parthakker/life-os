# Category Tree
## Complete Life OS Folder Structure

**Created:** October 18, 2024
**Purpose:** Document current organization structure
**Status:** Living document - updates when structure changes

---

## 📊 Complete Structure

```
life-os/
│
├── inbox/                           # Raw input processing
│   ├── raw.md                       # Paste organized dumps here
│   └── processed/                   # Archive of processed dumps
│       └── YYYY-MM-DD.md           # Dated archives
│
├── data/                            # All life data organized
│   │
│   ├── family/                      # 7 family members
│   │   ├── mom/
│   │   │   ├── notes.md
│   │   │   ├── tasks.md
│   │   │   ├── dates.md
│   │   │   └── conversations.md
│   │   ├── dad/
│   │   ├── mansi/
│   │   ├── aayushi/
│   │   ├── jay/
│   │   ├── suraj/
│   │   └── surekha-aunty/
│   │
│   ├── friends/                     # 11 core friends
│   │   ├── soham/
│   │   │   ├── notes.md
│   │   │   ├── tasks.md
│   │   │   ├── dates.md
│   │   │   └── conversations.md
│   │   ├── veenay/
│   │   ├── jon/
│   │   ├── varun/
│   │   ├── akhil/
│   │   ├── vineeth/
│   │   ├── vijay/
│   │   ├── shiraz/
│   │   ├── viren/
│   │   ├── steven-schilder/
│   │   └── shivam/
│   │
│   ├── preeti/                      # Fiancé
│   │   ├── tasks.md
│   │   ├── dates-ideas.md
│   │   └── notes.md
│   │
│   ├── wedding/                     # May 3, 2026
│   │   ├── overview.md              # Timeline & overview
│   │   ├── finance.md               # All costs (no analysis yet)
│   │   ├── my-todos.md
│   │   ├── parents-tasks.md
│   │   ├── my-tasks-for-parents.md
│   │   ├── guest-management.md
│   │   ├── events/
│   │   │   ├── haldi-wednesday.md   # Wed: Both haldis
│   │   │   ├── pooja-thursday.md    # Thu: Parth pooja
│   │   │   ├── sangeet-friday.md    # Fri: Sangeet at Rasoi
│   │   │   ├── welcome-dinner-saturday.md
│   │   │   └── ceremony-reception-sunday.md  # The Grove
│   │   └── vendors/
│   │       ├── contracts/           # PDFs of contracts
│   │       └── vendor-contacts.md
│   │
│   ├── work/
│   │   ├── high-dollar-rcas/
│   │   │   ├── account-backlog.md
│   │   │   ├── trends-monitoring.md
│   │   │   └── digital-compromise.md
│   │   ├── governance-controls/
│   │   │   ├── idv-rules-docs.md
│   │   │   ├── idb-ruleset-master.md
│   │   │   └── tech-idb-rules.md
│   │   ├── major-projects/
│   │   │   ├── not-ato-bot.md
│   │   │   ├── dash-migration.md
│   │   │   ├── pii-tokenization.md
│   │   │   └── notification-strategy.md
│   │   ├── tasks.md
│   │   ├── deadlines.md
│   │   └── networking.md
│   │
│   ├── home/
│   │   ├── bills/
│   │   │   ├── mortgage.md
│   │   │   ├── hoa.md
│   │   │   ├── utilities.md         # Electric, water, wifi, sewage
│   │   │   └── taxes.md
│   │   ├── tenant/
│   │   │   └── brad-rent.md
│   │   └── maintenance.md
│   │
│   ├── buddy/
│   │   ├── health-issues.md
│   │   ├── vet-appointments.md
│   │   ├── medical-records.md
│   │   ├── insurance.md
│   │   ├── care-schedule.md
│   │   └── supplies.md
│   │
│   ├── fitness/
│   │   ├── gym.md
│   │   └── jujitsu.md
│   │
│   ├── hobbies/
│   │   ├── nfl/
│   │   │   ├── fantasy-football.md
│   │   │   └── madden.md
│   │   ├── video-games/
│   │   │   ├── league-of-legends.md
│   │   │   └── playstation.md
│   │   ├── guitar.md
│   │   └── photography.md
│   │
│   ├── side-hustles/
│   │   ├── betting/
│   │   │   ├── active-bets.md
│   │   │   ├── bet-tracking.md
│   │   │   └── bankroll.md
│   │   └── princeton-ai/
│   │       ├── uplevel-resume.md    # CRITICAL: 2-week contract
│   │       ├── uplevel-website.md
│   │       ├── company-website.md
│   │       ├── hamilton-deli.md
│   │       └── jhopri.md
│   │
│   └── personal-projects/
│       ├── personal-assistant-ai.md
│       ├── nfl-learning-website.md
│       └── bot-with-varun.md
│
├── documents/                       # All media & files
│   ├── photos/                      # Photos
│   ├── screenshots/                 # Screenshots
│   ├── receipts/                    # Receipt images
│   ├── medical/                     # Buddy's medical docs
│   └── wedding/                     # Wedding contracts & docs
│
├── .agent/                          # Knowledge base
│   ├── readme.md                    # Main documentation index
│   ├── system/                      # Core knowledge
│   │   ├── core-principles.md       # How Life OS works
│   │   ├── organization-rules.md    # Categorization logic
│   │   ├── keyword-mapping.md       # Learned patterns
│   │   ├── category-tree.md         # This file
│   │   ├── data-format-spec.md      # Entry formatting
│   │   └── transcript-prompt.md     # Claude dump template
│   ├── decisions/
│   │   └── structure-choices.md     # Why this organization
│   ├── inbox-processor/
│   │   └── instructions.md          # How to organize
│   └── logs/
│       └── organization-log.md      # Audit trail
│
└── dashboard/                       # Visual interface
    ├── index.html                   # Main dashboard
    ├── styles.css                   # Styling
    ├── script.js                    # Interactive logic
    └── data/
        └── aggregated-data.json     # Dashboard data
```

---

## 📈 Statistics

### Categories
- **Top-level categories:** 10
- **Subcategories:** 40+
- **Person folders:** 18 (7 family + 11 friends)

### File Counts

**People (Family + Friends + Preeti):** 18 people × 4 files each = ~72 files
**Wedding:** ~12 files
**Work:** ~12 files
**Home:** ~6 files
**Buddy:** ~6 files
**Fitness:** ~2 files
**Hobbies:** ~6 files
**Side Hustles:** ~8 files
**Personal Projects:** ~3 files

**Total:** ~125+ markdown files (when fully populated)

---

## 🎯 Category Purposes

### People Categories

**family/** - 7 family members
- Purpose: Track tasks, important dates, conversations with each family member
- Use case: "What do I need to do for mom?", "When is dad's birthday?"

**friends/** - 11 core friends
- Purpose: Maintain relationships, remember important details
- Use case: "When did I last hang out with Soham?", "What gift ideas for Jon?"

**preeti/** - Fiancé
- Purpose: Relationship management, date ideas, special tasks
- Use case: "Date night ideas", "Things Preeti wants to do"

### Life Area Categories

**wedding/** - May 3, 2026
- Purpose: Manage complex multi-day Indian wedding
- Events: 5 days of events (Wed-Sun)
- Use case: "What vendors need payment?", "What are parents responsible for?"

**work/**
- Purpose: Track projects, deadlines, tasks
- Subcategories by project type
- Use case: "What's due this week?", "DASH Migration status?"

**home/**
- Purpose: Bills, tenant, maintenance
- Use case: "When is HOA due?", "Did Brad pay rent?", "What needs fixing?"

**buddy/**
- Purpose: Dog health & care management
- Use case: "When is next vet appointment?", "What medications does Buddy need?"

### Activity Categories

**fitness/**
- Purpose: Track gym & jujitsu activities
- Use case: "When did I last go to gym?", "Class schedule?"

**hobbies/**
- Purpose: Fun activities (NFL, gaming, guitar, photography)
- Use case: "Fantasy football notes", "Which games am I playing?"

**side-hustles/**
- Purpose: Income-generating activities
- Betting + Princeton AI Partners clients
- Use case: "Active client projects?", "Betting performance?"

**personal-projects/**
- Purpose: Personal development & side projects
- Use case: "Project ideas", "What am I building?"

---

## 🔄 Evolution Over Time

### Initial Structure (Oct 18, 2024)
Complete folder tree created based on initial life dump.

### Future Additions
Structure will evolve as life changes:
- New categories as new life areas emerge
- Archive categories when life phases end (e.g., wedding)
- Reorganize based on actual usage patterns

### Archive Strategy
When major life events complete (e.g., wedding in May 2026):
- Keep folder but move to `data/archive/wedding/`
- Maintain for reference
- Remove from active dashboard

---

## 📝 File Templates

### Person File Structure
Each person folder contains:
- `notes.md` - General notes, important info
- `tasks.md` - Things to do for/with them
- `dates.md` - Birthday, important dates
- `conversations.md` - Important things discussed

### Event File Structure
Each event (wedding, etc.) contains:
- Overview/timeline
- Vendor/participant list
- Tasks/checklist
- Budget/costs
- Notes

### Project File Structure
Each project (work/side hustle) contains:
- Objective/goal
- Deliverables
- Timeline/deadlines
- Status updates
- Notes

---

## 🚀 Expansion Guidelines

### When to Add Category
- New major life area emerges
- Existing category becomes too broad
- 5+ items don't fit current structure

### When to Add Subcategory
- Category has 10+ files
- Clear subdivision emerges
- Different types of items in one category

### When to Consolidate
- Category has <3 items long-term
- Overlap with another category
- Life phase ended

### Document Changes
When structure changes:
1. Update this file
2. Update `organization-rules.md`
3. Update `keyword-mapping.md`
4. Log in `../decisions/structure-choices.md`
5. Update dashboard

---

## 🔗 Related Docs

- `organization-rules.md` - How items get categorized
- `keyword-mapping.md` - Keywords → categories mapping
- `data-format-spec.md` - How to format entries
- `../decisions/structure-choices.md` - Why this structure

---

**Last Updated:** October 18, 2024
**Version:** 1.0
**Next Review:** After 1 month of use
**Total Files:** ~125+ markdown files when populated
