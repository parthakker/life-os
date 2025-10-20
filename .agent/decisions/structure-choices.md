# Decision: Life OS Structure Choices

**Date:** October 18, 2024
**Status:** Active
**Decision Made By:** Parth + AI planning session

---

## Context

**Problem we were solving:**
- Life overwhelming with multiple responsibilities:
  - Wedding planning (May 3, 2026)
  - Demanding job with multiple projects
  - Side hustles (Princeton AI, betting)
  - Home ownership (bills, tenant)
  - Dog with health issues (Buddy)
  - Family & friends relationships
  - Personal projects & hobbies
- Things falling through cracks
- No single view of everything
- Need system to capture, organize, and visualize all of life

**Key constraints:**
- Must be simple to use daily
- Must handle complex, multi-faceted life
- Must work with voice dumps (natural input)
- Must be always-visible (desktop dashboard)
- Must learn and improve over time

---

## Options Considered

### Option A: Use Existing Tools (Notion, Obsidian, Todoist)
**Pros:**
- Already built
- Feature-rich
- Mobile apps

**Cons:**
- ❌ Generic structure doesn't match mental model
- ❌ Can't customize AI organization logic
- ❌ Data locked in proprietary systems
- ❌ Requires learning their way of thinking
- ❌ Monthly costs for some
- ❌ No control over future development

### Option B: Simple Spreadsheet Tracking
**Pros:**
- Easy to start
- Familiar tool

**Cons:**
- ❌ Doesn't scale to complex life
- ❌ Hard to visualize across categories
- ❌ No intelligent organization
- ❌ Becomes messy quickly
- ❌ Can't handle voice dumps

### Option C: Custom Life OS with .agent Structure (CHOSEN)
**Pros:**
- ✅ Structure matches YOUR life exactly
- ✅ Intelligent organization agent learns your patterns
- ✅ Local files - own your data
- ✅ Customizable to any degree
- ✅ Visual dashboard always-on
- ✅ Handles voice dumps naturally
- ✅ Scales infinitely
- ✅ Future upgrades (Telegram, calendar, etc.)

**Cons:**
- Requires initial build time (~2 hours)
- Need to maintain it yourself
- No mobile app (yet)

---

## Decision

**We chose Option C: Custom Life OS**

### Implementation Details

**Folder Structure:**
- `inbox/` - Where organized dumps go
- `data/` - All life data in markdown files
- `documents/` - Photos, PDFs, receipts
- `.agent/` - Knowledge base & organization rules
- `dashboard/` - Visual interface

**Organization Agent:**
- Reads `inbox/raw.md`
- Parses based on keyword rules
- Asks questions when ambiguous
- Learns from answers
- Files into correct categories
- Updates dashboard

**Dashboard Design:**
- Always-visible on desktop
- Temporal views (Today, Next 7 Days, This Month)
- Life areas overview (clickable)
- Quick add functionality
- Refresh to update

**Data Format:**
- Markdown files (human-readable, future-proof)
- Consistent structure (see data-format-spec.md)
- Flexible enough for custom fields

---

## Consequences

### Positive

✅ **Perfect Fit:** Structure exactly matches how you think about life
✅ **Intelligent:** Agent learns your terminology and patterns
✅ **Scalable:** Add categories, upgrade features anytime
✅ **Visibility:** Always-on dashboard = nothing forgotten
✅ **Ownership:** Your data, your rules, your system
✅ **Future-Proof:** Markdown files readable forever
✅ **Upgradeable:** Can add Telegram, calendar, analytics later

### Negative

⚠️ **Build Time:** Requires 2-2.5 hours initial setup
- Mitigation: One-time cost, worth it for long-term benefit

⚠️ **Maintenance:** Need to maintain yourself
- Mitigation: System designed to be simple to maintain
- Documentation makes it easy

⚠️ **No Mobile App:** Desktop-only initially
- Mitigation: Can add Telegram bot for mobile input
- Dashboard accessible via mobile browser

### What This Means Going Forward

**Daily Use:**
- Voice dump → Process → Paste in inbox
- Organization agent files everything
- Dashboard shows what's up
- Always know what's happening

**Weekly:**
- Review dashboard
- Add missing items
- Check upcoming week

**Monthly:**
- Full life review
- Adjust structure if needed
- Archive completed items

**Future Enhancements:**
- Telegram bot integration (mobile input)
- Calendar sync (see on phone calendar)
- Financial analytics (budget tracking)
- Betting analytics (ROI, profit tracking)
- Automated reminders

---

## Specific Structure Decisions

### Why These Categories?

**People-Centric (Family, Friends, Preeti):**
- Relationships are core to life
- Each person has unique context
- Need to remember conversations, dates, tasks per person

**Event-Centric (Wedding):**
- Major life events need dedicated structure
- Multi-day wedding needs event breakdown
- Financial tracking separate from event details
- Will archive after wedding complete

**Work Separation:**
- Work complex enough for own category tree
- High-dollar RCAs, governance, projects distinct
- Need to see work deadlines separately from life

**Home as Category:**
- Bills, tenant, maintenance all home-related
- Could have been in "Finance" but home-specific makes more sense
- Easier to think "home stuff" than "financial stuff"

**Buddy Dedicated Category:**
- Dog health complex enough (insurance, vet, medications)
- Important enough to warrant own section
- Easier than nesting under "Pets" or "Home"

**Side Hustles vs Personal Projects:**
- Side hustles = income-generating
- Personal projects = learning/building
- Clear distinction matters for prioritization

### Why Temporal Dashboard (Today, 7 Days, Month)?

**Alternative Considered:** Priority-based (High/Med/Low)
- Problem: Everything feels high priority
- Solution: Time-based forces realistic view
- "What's actually due soon?" vs "What's important?"

**Why This Works:**
- Can't ignore what's due today
- Week view helps planning
- Month view prevents surprises
- Can still tag priorities within time view

### Why Markdown Files Not Database?

**Alternative Considered:** SQL database or JSON
- Problem: Not human-readable
- Problem: Requires tools to view/edit
- Problem: Harder to backup/version control

**Why Markdown:**
- Open in any text editor
- Readable without tools
- Git-friendly (version control)
- Future-proof (readable in 50 years)
- Can still be parsed/aggregated

### Why Interactive Dashboard Not Static?

**Alternative Considered:** Just markdown files, no dashboard
- Problem: Hard to get overview
- Problem: Can't see what's coming up quickly
- Problem: No always-visible view

**Why Dashboard:**
- Visual overview in seconds
- Always-on desktop = constant awareness
- Click to see details
- Motivating to see everything organized

---

## Review & Reassessment

**Review this decision if:**
- Structure doesn't match how you use it (3 months)
- Categories too broad or too specific (1 month)
- Dashboard not actually used daily (1 week)
- Better tools emerge (yearly)

**Success metrics** (informal):
- Do you use it daily? (Should be YES)
- Do things fall through cracks? (Should trend to NO)
- Does structure feel natural? (Should be YES)
- Is it quick to add items? (Should be YES, <1 min)

**When to pivot:**
- If not using after 2 weeks → Too complex, simplify
- If always searching for categories → Structure wrong, reorganize
- If dashboard not helpful → Redesign views
- If agent asks too many questions → Improve rules

---

## Related Decisions

**Future Decisions to Document:**
- When to add calendar integration
- When to upgrade to Telegram bot
- When to add financial analysis
- When to archive wedding category (post-May 2026)
- Mobile app strategy

---

## References

- `.agent/readme.md` - How Life OS works
- `.agent/system/core-principles.md` - Philosophy behind approach
- `.agent/system/category-tree.md` - Detailed structure

---

**Last Updated:** October 18, 2024
**Next Review:** After 1 week of use - see what's working
**Status:** Active - living with these decisions
