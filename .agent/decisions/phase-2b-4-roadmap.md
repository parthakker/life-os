# Life OS Roadmap: Phases 2B-4

**Created:** October 19, 2025
**Status:** Planning
**Current Phase:** 2A Complete (RAG System deployed)

## Overview

This document outlines the feature roadmap for Life OS from basic calendar integration through advanced intelligent import capabilities.

---

## Phase 2A: RAG System ✅ COMPLETE

**Status:** Deployed to production
**Completion Date:** October 19, 2025

**Delivered:**
- ✅ Agentic router with Claude 3.5 Haiku
- ✅ Custom JSON-based vector store
- ✅ Auto-vectorization on insert
- ✅ Semantic search across tasks and notes
- ✅ 3 tools: add_task, add_note, ask_question
- ✅ 41 categories with hierarchical structure
- ✅ Telegram bot interface
- ✅ Production deployment ready

**Architecture:**
```
Telegram → Router (Haiku) → Tools → Database/Vector Store
```

---

## Phase 2B: Basic Calendar Integration

**Timeline:** Week 2 (1-2 days)
**Status:** Planned

### Goals

Enable users to create and manage calendar events via natural language through the Telegram bot.

### Features

1. **schedule_event Tool**
   - Create calendar events from natural language
   - "schedule dinner with mom next Friday at 7pm"
   - "meeting with photographer on March 15 at 2pm"

2. **Natural Language Date Parsing**
   - "next Friday"
   - "tomorrow at 3pm"
   - "March 15 at 2:00 PM"
   - "in 2 hours"

3. **Event Operations**
   - Create events
   - List events ("what's on my calendar today")
   - Update events ("move dinner to 8pm")
   - Delete events ("cancel meeting with photographer")

4. **Basic Calendar Support**
   - Connect to primary Google Calendar
   - All events go to default calendar

### Technical Implementation

**New Tool Definition (`tools_manifest.py`):**
```python
"schedule_event": {
    "description": "Create calendar event with smart date parsing",
    "parameters": {
        "event_title": "string",
        "event_description": "string",
        "date_time": "string",  # Natural language
        "duration_minutes": "integer"  # Optional, default 60
    }
}
```

**Router Updates (`router.py`):**
- Add `execute_schedule_event()` function
- Integrate Google Calendar MCP
- Parse natural language dates
- Create event in Google Calendar
- Return confirmation

**Dependencies:**
- Google Calendar MCP installed
- OAuth credentials configured
- Google Calendar API enabled

### Success Criteria

✅ Can create events via Telegram
✅ Natural language dates work correctly
✅ Events appear in Google Calendar
✅ Can query calendar ("what's today")
✅ Update/delete operations work

### Example Usage

```
User: "schedule dinner with mom next Friday at 7pm"
Bot: ✅ Event created: Dinner with mom
     📅 Friday, October 25, 2025 at 7:00 PM
     🔗 Added to your calendar

User: "what's on my calendar tomorrow"
Bot: 📅 Tomorrow, October 21, 2025:
     • 9:00 AM - Team standup (30 min)
     • 2:00 PM - Dentist appointment (1 hour)
     • 7:00 PM - Dinner with mom (2 hours)
```

---

## Phase 2C: Calendar + RAG Integration

**Timeline:** Week 2 (1 day)
**Status:** Planned

### Goals

Integrate calendar events into the RAG system for unified search across tasks, notes, and events.

### Features

1. **Event Vectorization**
   - Auto-vectorize events on creation
   - Include in vector_store.json
   - Searchable like tasks/notes

2. **Unified Search**
   - "what are my wedding events this week"
   - "show me everything related to dentist"
   - "am I free tomorrow afternoon"

3. **Smart Filtering**
   - Filter by event type (task vs note vs event)
   - Filter by date range
   - Filter by category/calendar

### Technical Implementation

**Vector Store Updates (`vector_store.py`):**
```python
def add_event_to_vector_store(event_id, event_title, event_description,
                               start_time, end_time, calendar):
    """Add calendar event to vector store"""
    # Similar to add_to_vector_store but for events
    # Store: title, description, datetime, calendar
```

**RAG Query Updates (`rag_query.py`):**
- Support event type in filters
- Format events in results
- Show date/time for events

**Router Integration:**
- Auto-vectorize in execute_schedule_event()
- Query events in execute_ask_question()

### Success Criteria

✅ Events vectorized on creation
✅ Events searchable via RAG
✅ Can filter by event vs task vs note
✅ Date range filtering works
✅ Results show event details

### Example Usage

```
User: "what are my wedding tasks and events"
Bot: 🔍 Found 15 results:

     TASKS:
     ⏳ [Wedding] Book photographer
     ⏳ [Wedding] Send invitations
     ⏳ [Wedding] Choose menu

     EVENTS:
     📅 [Wedding] Venue walkthrough - March 15, 2026 at 2:00 PM
     📅 [Wedding] Cake tasting - April 3, 2026 at 3:00 PM
     📅 [Wedding] Final fitting - April 20, 2026 at 11:00 AM
```

---

## Phase 3A: Multi-Calendar Support

**Timeline:** Week 3 (2-3 days)
**Status:** Planned

### Goals

Support multiple Google Calendars with automatic calendar selection based on category.

### Features

1. **Multiple Calendar Connections**
   - Work calendar
   - Personal calendar
   - Wedding calendar
   - Shared calendars

2. **Category → Calendar Mapping**
   - Wedding category → Wedding calendar
   - Princeton AI → Work calendar
   - Home → Personal calendar
   - Configurable mappings

3. **Calendar-Aware Operations**
   - Auto-select calendar based on category
   - "schedule meeting with Hamilton Deli next week" → Work calendar
   - "schedule date night Friday" → Personal calendar
   - "schedule vendor meeting" → Wedding calendar

4. **Calendar Filtering**
   - "show me work events this week"
   - "what's on my personal calendar"
   - "wedding events in March"

### Technical Implementation

**Database Schema Update:**
```sql
ALTER TABLE categories ADD COLUMN calendar_id TEXT;
```

**Category → Calendar Mapping:**
```python
CALENDAR_MAPPINGS = {
    'Wedding': 'wedding@parthakker.com',
    'Princeton AI Partners': 'work@parthakker.com',
    'Home': 'personal@parthakker.com',
    ...
}
```

**Router Updates:**
- Detect category from message
- Auto-select appropriate calendar
- Support explicit calendar override

### Success Criteria

✅ Multiple calendars configured
✅ Category mappings working
✅ Auto-calendar selection works
✅ Can filter by calendar
✅ Events go to correct calendar

### Example Usage

```
User: "schedule venue walkthrough next Tuesday at 2pm"
Bot: ✅ Event created: Venue walkthrough
     📅 Tuesday, March 12, 2026 at 2:00 PM
     📆 Added to Wedding calendar

User: "what's on my work calendar this week"
Bot: 📅 Work Calendar - This Week:
     • Mon 9:00 AM - Team standup
     • Wed 2:00 PM - Hamilton Deli check-in
     • Fri 3:00 PM - UpLevel Resume strategy call
```

---

## Phase 3B: Intelligent Import - Images/PDFs

**Timeline:** Week 3-4 (3-4 days)
**Status:** Planned (High Priority)

### Goals

Enable users to forward images and PDFs to extract event details and automatically create calendar events.

### Features

1. **Image Event Extraction**
   - Forward wedding vendor flyer → extract event
   - Screenshot of email confirmation → create event
   - Photo of business card → extract contact + event

2. **PDF Event Extraction**
   - Vendor contracts with meeting dates
   - Event tickets (Eventbrite, Ticketmaster)
   - Email confirmations exported as PDF
   - Invoice with appointment dates

3. **Smart Extraction**
   - Event title
   - Date and time
   - Location/address
   - Description/notes
   - Duration (if specified)

4. **Confirmation Flow**
   - Extract details
   - Show to user for confirmation
   - User confirms or edits
   - Create event

### Technical Implementation

**Telegram Bot Updates (`telegram_bot.py`):**
```python
async def handle_photo(update: Update, context):
    """Handle photo messages"""
    # Download image
    # Send to Claude vision API
    # Extract event details
    # Confirm with user
    # Create event

async def handle_document(update: Update, context):
    """Handle PDF documents"""
    # Download PDF
    # Extract text + images
    # Parse with Claude
    # Extract event details
    # Confirm with user
    # Create event
```

**Event Extraction (`event_extractor.py`):**
```python
def extract_event_from_image(image_path):
    """Use Claude vision to extract event details"""
    # OCR with Claude
    # Identify: title, date, time, location
    # Return structured event data

def extract_event_from_pdf(pdf_path):
    """Extract event from PDF"""
    # Extract text and images
    # Parse with Claude
    # Return structured event data
```

**Router Integration:**
- New tool: `import_event_from_file`
- Confirmation before creating
- Add to appropriate calendar

### Success Criteria

✅ Can extract events from images
✅ Can extract events from PDFs
✅ Extraction accuracy >90%
✅ Confirmation flow works
✅ Events created in correct calendar
✅ User can edit before confirming

### Example Usage

```
User: *forwards vendor contract PDF*
Bot: 📄 Found event in document:

     Event: Final Venue Walkthrough
     Date: March 15, 2026 at 2:00 PM
     Duration: 2 hours
     Location: The Grand Ballroom, 123 Main St

     Add to Wedding calendar? (yes/no/edit)

User: "yes"
Bot: ✅ Event created: Final Venue Walkthrough
     📅 Saturday, March 15, 2026 at 2:00 PM
     📆 Added to Wedding calendar
     📍 The Grand Ballroom, 123 Main St
```

---

## Phase 3C: Intelligent Import - Web Links

**Timeline:** Week 4 (2 days)
**Status:** Planned

### Goals

Enable users to share web links (Eventbrite, Facebook events, etc.) and automatically extract event details.

### Features

1. **URL Detection**
   - Detect event URLs in messages
   - Support multiple platforms:
     - Eventbrite
     - Facebook Events
     - Google Calendar links
     - Ticketmaster
     - Email confirmations

2. **Event Extraction from Web**
   - Fetch page content
   - Parse structured data (JSON-LD)
   - Extract event details with Claude
   - Handle dynamic content

3. **Confirmation Flow**
   - Show extracted details
   - User confirms or edits
   - Create event
   - Add source URL to description

### Technical Implementation

**URL Detector (`router.py`):**
```python
def detect_event_url(message):
    """Detect if message contains event URL"""
    # Check for eventbrite.com, facebook.com/events, etc.
    # Return URL if found
```

**Web Event Extractor (`web_event_extractor.py`):**
```python
def extract_event_from_url(url):
    """Fetch and extract event from URL"""
    # Fetch page
    # Parse structured data (JSON-LD, microdata)
    # Extract with Claude if no structured data
    # Return event details
```

**Router Integration:**
- Detect URLs in messages
- Route to import_event_from_url tool
- Confirmation flow
- Create event with source URL

### Success Criteria

✅ URL detection works
✅ Event extraction from major platforms
✅ Structured data parsing works
✅ Fallback to Claude extraction works
✅ Confirmation flow functional
✅ Source URL saved in event

### Example Usage

```
User: "https://www.eventbrite.com/e/spring-wedding-expo-tickets"
Bot: 🔗 Found event from link:

     Event: Spring Wedding Expo 2026
     Date: April 20, 2026, 10:00 AM - 6:00 PM
     Location: Convention Center, Hall A
     Description: Annual wedding expo featuring 100+ vendors

     Add to Wedding calendar? (yes/no/edit)

User: "yes"
Bot: ✅ Event created: Spring Wedding Expo 2026
     📅 Sunday, April 20, 2026, 10:00 AM - 6:00 PM
     📆 Added to Wedding calendar
     🔗 Source: https://www.eventbrite.com/...
```

---

## Phase 4: Advanced Features

**Timeline:** Week 5+ (Future)
**Status:** Ideas / Low Priority

### Potential Features

1. **Recurring Event Modification**
   - "move all team standups to 10am"
   - Modify series vs single instance
   - Advanced recurrence rules

2. **Smart Conflict Detection**
   - Detect scheduling conflicts
   - Suggest alternative times
   - "you have a conflict with dentist appointment"

3. **Calendar Sharing**
   - Share Wedding calendar with Judy
   - Collaborative event planning
   - Permissions management

4. **Event Reminders**
   - Custom reminder settings
   - Telegram notifications for events
   - Smart reminder timing

5. **Travel Time Integration**
   - Calculate travel time to location
   - Suggest departure time
   - Traffic-aware scheduling

6. **Event Templates**
   - "weekly team standup"
   - "monthly dentist checkup"
   - Reusable event patterns

7. **Voice Event Creation**
   - Telegram voice messages
   - Speech-to-text → event
   - Hands-free scheduling

---

## Migration Path

### Database Evolution

**Phase 2B:**
```sql
-- No database changes (events stay in Google Calendar)
```

**Phase 2C:**
```sql
-- Add events to vector store (JSON)
-- No database schema changes
```

**Phase 3A:**
```sql
-- Add calendar mapping to categories
ALTER TABLE categories ADD COLUMN calendar_id TEXT;
```

**Future (PostgreSQL Migration):**
```sql
-- When migrating to Postgres for scale
-- Add pgvector extension for vector store
-- Migrate SQLite → PostgreSQL
```

---

## Technology Stack Evolution

### Current (Phase 2A)
- Python 3.11+
- SQLite (data.db)
- JSON vector store (vector_store.json)
- python-telegram-bot
- anthropic (Claude 3.5 Haiku)
- sentence-transformers

### Phase 2B Addition
- Google Calendar MCP
- google-auth libraries
- dateutil for date parsing

### Phase 3B Addition
- PyPDF2 or pdfplumber for PDF extraction
- Claude vision API for OCR
- Image processing libraries

### Phase 3C Addition
- BeautifulSoup for HTML parsing
- Requests for URL fetching
- JSON-LD parser for structured data

### Future Considerations
- PostgreSQL with pgvector
- Redis for caching
- FastAPI for dashboard backend
- React + shadcn/ui for web dashboard

---

## Cost Estimates

### Current (Phase 2A)
- **Render:** $0/month (free tier)
- **Claude API:** ~$0.36/month (20 msgs/day, Haiku)
- **Total:** ~$0.36/month

### Phase 2B-3 (Calendar + Import)
- **Render:** $0/month (still within free tier)
- **Claude API:** ~$1-2/month (more messages, vision API)
- **Google Calendar API:** Free (< 1M requests/day)
- **Total:** ~$1-2/month

### Phase 4+ (Advanced Features)
- **Render:** $0/month (or upgrade to $7/month if needed)
- **Claude API:** ~$3-5/month (heavy usage)
- **Total:** ~$3-12/month (depending on usage)

**Goal:** Keep under $5/month for personal use

---

## Success Metrics

### Phase 2B
- [ ] 100% of calendar events created successfully
- [ ] <5% date parsing errors
- [ ] <1 second event creation latency
- [ ] User satisfaction with natural language interface

### Phase 2C
- [ ] All events searchable via RAG
- [ ] <2 second search latency
- [ ] Relevant results in top 10 (90%+ accuracy)

### Phase 3B
- [ ] >90% event extraction accuracy from images/PDFs
- [ ] <10 second processing time
- [ ] User confirms without edits 80%+ of time

### Phase 3C
- [ ] Support top 5 event platforms (Eventbrite, Facebook, etc.)
- [ ] >85% extraction accuracy
- [ ] Structured data fallback working

---

## Risk Mitigation

### Technical Risks

1. **Google Calendar API Rate Limits**
   - Mitigation: Batch operations, caching
   - Free tier: 1M requests/day (plenty for personal use)

2. **Image/PDF Extraction Accuracy**
   - Mitigation: Confirmation flow before creating
   - User can edit extracted details
   - Fallback to manual entry

3. **Cost Overruns (Claude API)**
   - Mitigation: Monitor usage, use Haiku for most operations
   - Only use vision API when necessary
   - Set budget alerts

4. **Database Migration Complexity**
   - Mitigation: Defer PostgreSQL migration until needed
   - Keep migration scripts tested
   - Backup before migration

### User Experience Risks

1. **Overwhelming Features**
   - Mitigation: Progressive feature rollout
   - Phase 2B first (basic calendar)
   - Phase 3 only after 2B is validated

2. **Confirmation Fatigue**
   - Mitigation: Smart defaults, learn from user patterns
   - Auto-confirm if high confidence (>95%)
   - Allow "always confirm" preference

---

## Next Steps

**Immediate (This Week):**
1. ✅ Install all MCPs (GitHub, Filesystem, Google Calendar)
2. ✅ Push Life OS to GitHub
3. ✅ Deploy Phase 2A to Render
4. ✅ Test in production

**Week 2:**
5. 📅 Implement Phase 2B (Calendar integration)
6. 📅 Test calendar operations
7. 📅 Implement Phase 2C (Calendar + RAG)

**Week 3-4:**
8. 🖼️ Implement Phase 3B (Intelligent import - images/PDFs)
9. 🔗 Implement Phase 3C (Web link import)
10. 📊 Gather user feedback

**Future:**
11. 🚀 Phase 4 features based on usage patterns
12. 📈 Scale infrastructure if needed
13. 🌐 Consider web dashboard

---

## Conclusion

This roadmap takes Life OS from a task/note management system to a comprehensive personal assistant with intelligent calendar integration and multi-modal event import capabilities. Each phase builds on the previous, maintaining a clean architecture while adding progressively more sophisticated features.

The focus on wedding planning use cases (vendor meetings, event flyers, contract parsing) ensures the features deliver immediate value while remaining general enough for all life areas.

**Vision:** By Phase 3, you can forward a wedding vendor contract PDF to your Telegram bot, and it automatically extracts the meeting date, creates a calendar event in your Wedding calendar, and makes it searchable alongside your tasks and notes. That's the power of Life OS.
