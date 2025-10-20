# Data Format Specification
## How to Format Different Entry Types

**Created:** October 18, 2024
**Purpose:** Standardize data entry formats across all categories
**Philosophy:** Consistent structure, flexible enough for variation

---

## 🎯 General Principles

### Standard Format
- Markdown syntax
- Bullet points for lists
- Checkboxes for tasks
- Clear headers for sections
- Dates in YYYY-MM-DD format (sortable)

### Flexibility
- Required fields in every entry
- Optional fields as needed
- Custom fields allowed
- Keep it human-readable

---

## ✅ Task Entry Format

### Standard Task
```markdown
- [ ] Task description
  - Due: YYYY-MM-DD
  - Priority: High/Medium/Low
  - Added: YYYY-MM-DD
  - Notes: Additional context
```

### Completed Task
```markdown
- [x] Task description
  - Due: YYYY-MM-DD
  - Priority: High
  - Completed: YYYY-MM-DD
  - Notes: How it went
```

### Examples
```markdown
- [ ] Call mom about wedding guest list
  - Due: 2024-10-21
  - Priority: High
  - Added: 2024-10-18
  - Notes: She mentioned wanting to invite extended family

- [x] Dryer vent cleaning
  - Due: 2024-10-20
  - Priority: Medium
  - Completed: 2024-10-19
  - Notes: Cost $150, company was great
```

---

## 💰 Financial Entry Format

### Bill/Payment
```markdown
- **[Item Name]**: $X,XXX
  - Due: YYYY-MM-DD or "Monthly on [day]"
  - Status: Paid/Pending/Overdue
  - Payment method: Auto-pay/Manual/Check
  - Account: Where it's paid from
  - Notes: Additional context
```

### Examples
```markdown
- **HOA Fee**: $TBD
  - Due: Monthly on 1st
  - Status: Pending
  - Payment method: Need to set up auto-pay
  - Account: Chase checking
  - Notes: PRIORITY - automate this!

- **Wedding Venue Final Payment**: $5,000
  - Due: 2024-10-10
  - Status: Paid
  - Payment method: Credit card
  - Account: Amex
  - Notes: Called and confirmed - receipt in email
```

---

## 📅 Appointment/Event Entry Format

### Standard Appointment
```markdown
- **[Date & Time]**: [Description]
  - Location: [Where]
  - Duration: [How long]
  - Reminder: [When to remind]
  - Prep needed: [What to prepare]
  - Notes: [Additional context]
```

### Examples
```markdown
- **2024-10-15 3:00 PM**: Buddy vet appointment
  - Location: Main Street Vet
  - Duration: 30 min
  - Reminder: Day before
  - Prep needed: Bring vaccination records
  - Notes: Regular checkup - ask about fat growths

- **2026-05-03 Morning**: Wedding Ceremony
  - Location: The Grove, Cedar Grove NJ
  - Duration: All day
  - Reminder: Multiple leading up
  - Prep needed: Everything!
  - Notes: Main event - ceremony AM, reception PM
```

---

## 📝 Note Entry Format

### General Note
```markdown
- **[Date]**: [Content]
  - Tags: #tag1 #tag2
  - Category: [Type of note]
  - Follow-up: [If action needed]
```

### Examples
```markdown
- **2024-10-18**: Preeti mentioned wanting to visit Italy for honeymoon
  - Tags: #honeymoon #travel #ideas
  - Category: Travel planning
  - Follow-up: Research Italy honeymoon packages

- **2024-10-17**: Jay (work) mentioned geolocation rules need review
  - Tags: #work #rules #Florida
  - Category: Work task
  - Follow-up: Schedule meeting with Jay
```

---

## 👤 Person Profile Format

### notes.md
```markdown
# [Person Name]

## Basic Info
- Birthday: [Date]
- Relationship: [How you know them]
- Contact: [Phone/email if needed]

## Important Info
- [Key thing to remember]
- [Another important detail]

## Recent Notes
- **[Date]**: [Note content]
- **[Date]**: [Note content]
```

### tasks.md
```markdown
# Tasks for/with [Person Name]

## Active Tasks
- [ ] Task 1
  - Due: [Date]
  - Notes: [Context]

## Completed Tasks
- [x] Task 1
  - Completed: [Date]
```

### dates.md
```markdown
# Important Dates - [Person Name]

## Recurring
- **Birthday**: [MM-DD]
- **Anniversary**: [MM-DD] (if applicable)

## One-Time
- **[Event]**: [Date]
  - Notes: [Details]
```

### conversations.md
```markdown
# Conversations - [Person Name]

## [Date] - [Topic]
[Summary of important things discussed]
- Key point 1
- Key point 2
- Follow-up needed: [If any]

---
```

---

## 📊 Project/Work Entry Format

### Project File Structure
```markdown
# [Project Name]

## Overview
- **Status**: In Progress/On Hold/Completed
- **Start Date**: YYYY-MM-DD
- **Target End**: YYYY-MM-DD
- **Priority**: High/Medium/Low

## Objective
[What you're trying to achieve]

## Deliverables
- [ ] Deliverable 1
  - Due: YYYY-MM-DD
  - Status: [Status]

## Timeline
- **[Date]**: Milestone 1
- **[Date]**: Milestone 2

## Notes
- **[Date]**: [Note content]

## Decisions
- **[Date]**: [Decision made and why]
```

### Example
```markdown
# Uplevel Resume Contract

## Overview
- **Status**: In Progress - CRITICAL
- **Start Date**: 2024-10-14
- **Target End**: 2024-10-28 (2 weeks!)
- **Priority**: HIGH

## Objective
Complete resume redesign project for Uplevel client

## Deliverables
- [ ] Initial mockups
  - Due: 2024-10-20
  - Status: In progress

- [ ] Final designs
  - Due: 2024-10-28
  - Status: Not started

## Timeline
- **2024-10-20**: Client review of mockups
- **2024-10-25**: Revisions complete
- **2024-10-28**: Final delivery

## Notes
- **2024-10-18**: Client wants modern, clean aesthetic
- **2024-10-18**: Needs to work on mobile

## Decisions
- **2024-10-18**: Using Figma for mockups
```

---

## 🎉 Wedding Event Format

```markdown
# [Event Name] - [Day/Date]

## Details
- **Date**: [Full date]
- **Time**: [Start - End]
- **Location**: [Venue name & address]
- **Attendees**: [Expected count]

## Vendors
- **[Vendor Type]**: [Vendor name]
  - Contact: [Phone/email]
  - Cost: $X,XXX
  - Status: Booked/Pending

## Timeline
- **[Time]**: [Activity]
- **[Time]**: [Activity]

## My Tasks
- [ ] Task 1
  - Due: [Date]

## Parents' Tasks
- [ ] Task 1
  - Assigned to: Mom/Dad
  - Due: [Date]

## Notes
- [Important details]
```

---

## 🐕 Buddy Health Format

### Health Issue
```markdown
- **[Issue Name]**
  - First noticed: YYYY-MM-DD
  - Severity: Mild/Moderate/Severe
  - Current status: Ongoing/Resolved/Monitoring
  - Treatment: [What's being done]
  - Vet notes: [What vet said]
  - Follow-up: [When to check again]
```

### Vet Appointment
```markdown
- **[Date Time]**: [Appointment type]
  - Vet: [Which vet/location]
  - Reason: [Why going]
  - Cost: $XXX
  - Outcome: [What happened]
  - Next steps: [Follow-up needed]
```

---

## 🎮 Hobby/Activity Format

### General Activity
```markdown
## [Activity/Game Name]

### Current Status
- Last played/done: YYYY-MM-DD
- Progress: [Where you are]
- Goal: [What you're working toward]

### Notes
- **[Date]**: [Note]
- **[Date]**: [Note]

### Ideas
- [Idea 1]
- [Idea 2]
```

### NFL/Fantasy Football
```markdown
## Week [#]

### My Team
- Record: [W-L]
- Players: [Key players]
- Matchup: vs [Opponent]

### Bets/Predictions
- [Bet details]

### Notes
- [Weekly observations]
```

---

## 💡 Ideas Format

```markdown
# [Idea Category]

## [Idea Title]
- **Added**: YYYY-MM-DD
- **Status**: Idea/Planning/In Progress/Shelved
- **Priority**: High/Medium/Low

### Description
[What is the idea]

### Why
[Why this is interesting/valuable]

### Next Steps
- [ ] Step 1
- [ ] Step 2

### Resources Needed
- [Resource 1]
- [Resource 2]

### Notes
- [Additional thoughts]
```

---

## 🏠 Bill Tracking Format

```markdown
# [Bill Category]

## [Specific Bill]

### Details
- **Amount**: $X,XXX
- **Due Date**: [Monthly on X] or [Specific date]
- **Payment Method**: Auto-pay/Manual
- **Account**: [Which account pays this]

### History
- **[Date]**: Paid $XXX
- **[Date]**: Paid $XXX

### Notes
- [Important info about this bill]
- [Changes needed]

### Actions
- [ ] [Any todo related to this bill]
```

---

## 📸 Media Reference Format

When referencing photos, screenshots, or documents:

```markdown
- [Description of item]
  - File: `documents/[subfolder]/filename.ext`
  - Date: YYYY-MM-DD
  - Notes: [What this is]
```

### Example
```markdown
- Wedding venue contract
  - File: `documents/wedding/the-grove-contract.pdf`
  - Date: 2024-09-15
  - Notes: Signed contract, final payment due 10/10
```

---

## 🔄 Status Indicators

Use consistent status labels:

### Task Status
- `Not Started`
- `In Progress`
- `Blocked` (if waiting on something)
- `Completed`
- `Cancelled`

### Priority Levels
- `High` or 🔴 - Urgent, important
- `Medium` or 🟡 - Important, not urgent
- `Low` or 🟢 - Nice to have

### Payment Status
- `Paid`
- `Pending`
- `Overdue`
- `Scheduled`

---

## 📏 Date Formats

### Standard Date Format
`YYYY-MM-DD` (e.g., 2024-10-18)

**Why:** Sortable, unambiguous, universal

### Display Formats (Dashboard)
- "Today"
- "Tomorrow"
- "Mon 10/21"
- "Oct 21, 2024"

### Recurring
- "Monthly on [day number]"
- "Every 2 months"
- "Quarterly"
- "Annually on [MM-DD]"

---

## 💭 Placeholder Values

When information is missing, use consistent placeholders:

- `TBD` - To be determined
- `N/A` - Not applicable
- `Unknown` - Don't know yet
- `ASAP` - As soon as possible

### Examples
```markdown
- **HOA Fee**: $TBD
  - Due: Monthly on 1st
  - Status: Pending
  - Notes: Need to check amount

- **Guitar practice goal**: TBD
  - Will set after first few sessions
```

---

## 🔗 Cross-References

When items relate to multiple categories:

```markdown
- [Item description]
  - Related: See `category/subcategory/file.md`
  - Also in: [Other location]
```

### Example
```markdown
- Wedding venue payment $5k due 10/10
  - Category: Wedding > Finance
  - Also in: Wedding > Vendors
  - Related: See `wedding/vendors/the-grove-contract.md`
```

---

## ✨ Best Practices

### Do's
✅ Use consistent date formats
✅ Include priority on tasks
✅ Add notes for context
✅ Use checkboxes for tasks
✅ Cross-reference related items

### Don'ts
❌ Mix date formats
❌ Leave tasks without due dates (use TBD if unknown)
❌ Forget to update status
❌ Use vague descriptions
❌ Duplicate information across files unnecessarily

---

## 🔗 Related Docs

- `organization-rules.md` - How items get categorized
- `category-tree.md` - Where files live
- `keyword-mapping.md` - Keywords that trigger categories

---

**Last Updated:** October 18, 2024
**Version:** 1.0
**Status:** Reference guide - use for all data entry
