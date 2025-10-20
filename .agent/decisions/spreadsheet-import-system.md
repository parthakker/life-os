# Decision: Spreadsheet Import System

**Date:** 2025-10-18
**Status:** Implemented
**Decision Makers:** User + Claude

## Context

User has extensive life data across multiple categories (work, wedding, family, home, etc.) and wanted an efficient way to bulk edit and populate the Life OS system. Manually editing 27+ markdown files item-by-item is tedious and error-prone.

## Problem Statement

**Primary Need:**
- Bulk editing capability for tasks and structured data
- Familiar interface (Excel/Google Sheets)
- Efficient initial population of Life OS
- Easy to share template with friends

**Two Types of Content:**
1. **Tasks** - Action items with due dates, priorities, status
2. **Notes** - Reference information (contacts, project context, health records)

## Decision

Implement a **CSV-based import/export system** for bulk data management.

### Architecture

```
Markdown Files (source of truth) ←→ CSV Files (bulk editing interface)
                    ↓
            Dashboard (visualization)
```

**Bidirectional Flow:**
- Export: Markdown → CSV (for editing)
- Import: CSV → Markdown (after editing)

### CSV Files Created

**Tasks:**
- `tasks.csv` - Master list of all tasks across categories
- Columns: task, due_date, priority, status, category, project, notes, added_date, file

**Structured Data (Templates):**
- `bills.csv` - Recurring bill information
- `wedding-vendors.csv` - Vendor contacts and costs
- `family-people.csv` - Family member details
- `friends-people.csv` - Friend contacts

### Scripts Created

1. **`export-tasks-to-csv.py`** - Extract all tasks from markdown to CSV
2. **`import-from-csv.py`** - Update markdown files from edited CSV (with --dry-run option)

## Alternatives Considered

### Option A: Direct Markdown Editing Only
**Pros:**
- Simple, no conversion needed
- Files already there
- Version control friendly

**Cons:**
- Tedious for bulk operations
- Hard to see all tasks at once
- No sorting/filtering
- Not familiar to non-technical users

**Why rejected:** Doesn't solve the bulk editing problem

### Option B: Database (SQLite)
**Pros:**
- Powerful queries
- Proper relational data
- Enforced schemas

**Cons:**
- Adds complexity
- Not easily shareable
- Hard to version control
- Requires SQL knowledge

**Why rejected:** Overcomplicated for user's needs

### Option C: Notion/Airtable Integration
**Pros:**
- Nice UI
- Collaboration features
- Mobile apps

**Cons:**
- Requires internet
- Vendor lock-in
- Not locally controlled
- Costs money
- Doesn't align with "local-first" philosophy

**Why rejected:** User wants local control

### Option D: Excel/JSON Format
**Pros:**
- Rich formatting
- Formulas
- Multiple sheets

**Cons:**
- Binary format (bad for git)
- Requires Excel
- Platform-specific

**Why rejected:** CSV is more universal

## Why CSV Was Chosen

**✓ Universal Format**
- Works with Excel, Google Sheets, LibreOffice, Numbers
- Plain text (git-friendly)
- No proprietary software required

**✓ Bulk Operations**
- Sort, filter, copy-paste
- Formulas for date calculations
- Conditional formatting
- Easy to see all data at once

**✓ Future-Proof**
- Import/export from other tools (Notion, Todoist, etc.)
- Telegram bot can use same format
- Friends can use same templates

**✓ Simple**
- No database setup
- No server required
- Just edit and import

## Implementation Details

### Directionality Choice

**Decision:** Start with **Option A** (CSV → Markdown one-way import)

**Phases:**
1. **Phase 1 (Now):** One-way import for initial population
2. **Phase 2 (Later):** Add reverse export for syncing changes back
3. **Phase 3 (Future):** Potential live bidirectional sync

**Rationale:**
- Simpler to implement correctly
- Most value from initial bulk import
- Can add complexity later if needed

### File Paths in CSV

**Decision:** Store source file path in `file` column

**Why:**
- Preserves mapping between CSV rows and markdown files
- Allows tasks to be organized in their proper category files
- User can reorganize by changing file column

### Dry Run Feature

**Decision:** Add `--dry-run` flag to import script

**Why:**
- Safe testing before modifying files
- Shows preview of changes
- Builds confidence in system

## Benefits Achieved

1. **Efficiency** - Edit 60+ tasks in one spreadsheet view
2. **Familiar** - Everyone knows Excel/Google Sheets
3. **Shareable** - Friends get same CSV templates
4. **Flexible** - Can still edit markdown directly
5. **Future-proof** - CSV format works everywhere

## Risks & Mitigations

**Risk:** CSV and markdown get out of sync
**Mitigation:** Export script always available to refresh CSV from markdown

**Risk:** User edits both CSV and markdown
**Mitigation:** Documentation clarifies workflow options

**Risk:** Merge conflicts in CSV
**Mitigation:** CSV is plain text, git can merge. Use markdown as source of truth if conflicts occur.

**Risk:** Data loss during import
**Mitigation:** Dry-run mode, backup recommendations in docs

## Success Metrics

- ✓ Can extract 63 tasks from 17 files to single CSV
- ✓ Can bulk edit in familiar spreadsheet
- ✓ Can import back to markdown with `--dry-run` validation
- ✓ Preserves task metadata (due dates, priorities, notes)
- ✓ Friends can use same system with their own data

## Future Enhancements

**Phase 2 - Life Area Detail View:**
- Click category cards to view tasks + notes
- Makes CSV-generated content visible in dashboard

**Phase 3 - Direct Dashboard Editing:**
- Edit tasks in dashboard UI
- Auto-saves to markdown
- Eliminates CSV step for day-to-day use

**Potential:**
- Import scripts for bills.csv, vendors.csv (generate markdown pages)
- Validation script (check dates, detect duplicates)
- Smart categorization based on keywords
- Export to other formats (JSON, YAML)

## Lessons Learned

**What Worked:**
- CSV is perfect middle ground between simple and powerful
- Separation of tasks vs notes clarified data model
- Dry-run builds user confidence

**What to Improve:**
- Could add data validation in CSV (dropdowns for priority)
- Template CSVs could have example rows
- Import script could detect and merge duplicate tasks

## References

- Initial context dump: User has complex life data needing organization
- Dashboard implementation: Needed data source beyond manual markdown editing
- PrincetonAI .agent structure: Guides this documentation approach
- User feedback: "Spreadsheet makes way more sense, way more efficient"

## Conclusion

CSV import system solves the bulk editing problem elegantly. It maintains markdown as source of truth while providing a familiar, powerful interface for managing large amounts of data. This approach scales to user's friends and future Telegram bot integration.

The key insight: **Don't fight against what users already know.** Excel/CSV is familiar, powerful, and universal. Use it.
