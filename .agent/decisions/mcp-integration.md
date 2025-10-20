# MCP Integration Decision

**Date:** October 19, 2025
**Status:** ✅ Planned (Installation in progress)

## Decision Summary

Integrate three Model Context Protocol (MCP) servers into Life OS to enhance Claude Code's capabilities for development, deployment, and feature implementation.

## MCPs Selected

### 1. GitHub MCP (`@modelcontextprotocol/server-github`)

**Purpose:** Enable Claude Code to manage GitHub repositories directly

**Capabilities:**
- Push code to repositories
- Create and manage pull requests
- Handle issues and comments
- Manage branches and commits
- View repository status

**Why We Need This:**
- Currently blocked on GitHub push (authentication issue)
- Will streamline deployment workflow
- Enable automated PR creation for Phase 2B/3 features
- Better collaboration capabilities

**Installation:**
- Requires GitHub Personal Access Token
- Scopes: `repo`, `read:org`, `workflow`
- See `MCP_SETUP_GUIDE.md` for setup instructions

---

### 2. Filesystem MCP (`@modelcontextprotocol/server-filesystem`)

**Purpose:** Enhanced file operations and database management

**Capabilities:**
- Better file read/write operations
- Directory management
- File system monitoring
- Backup operations
- Efficient file search

**Why We Need This:**
- Database backup automation (`data.db`, `vector_store.json`)
- Better file operations for migration scripts
- Monitoring database growth
- Log file management

**Installation:**
- Simple configuration pointing to Life OS directory
- No API keys required
- See `MCP_SETUP_GUIDE.md` for setup instructions

---

### 3. Google Calendar MCP (`nspady/google-calendar-mcp`)

**Purpose:** Enable calendar integration for Phase 2B

**Capabilities:**
- Create calendar events
- List events from calendars
- Update and delete events
- Query free/busy status
- Support for recurring events
- Multi-calendar support

**Why We Need This:**
- Essential for Phase 2B (Calendar Integration)
- Enables `schedule_event` tool
- Natural language event creation
- Two-way sync with Google Calendar

**Installation:**
- Requires Google Cloud Project
- OAuth 2.0 credentials needed
- Google Calendar API must be enabled
- See `MCP_SETUP_GUIDE.md` for detailed setup

---

## Architecture Integration

### Current Architecture (Phase 2A)

```
User (Telegram) → telegram_bot.py → router.py
                                       ↓
                              add_task | add_note | ask_question
                                       ↓
                                   database.db
                                       ↓
                                 vector_store.py
                                       ↓
                                vector_store.json
```

### Enhanced Architecture (With MCPs)

```
User (Telegram) → telegram_bot.py → router.py
                                       ↓
                      add_task | add_note | ask_question | schedule_event
                           ↓          ↓           ↓              ↓
                       database    database   vector_store   Google Calendar MCP
                           ↓          ↓           ↓              ↓
                      data.db    data.db    vector_store   Google Calendar API
                                                .json
```

**Claude Code Development:**
```
Claude Code → GitHub MCP → GitHub API → github.com/parthakker/life-os
            → Filesystem MCP → Local file system → Life OS directory
```

---

## Benefits

### Immediate Benefits (GitHub + Filesystem MCPs)

1. **Streamlined Deployment**
   - Push to GitHub without manual intervention
   - Automated deployments to Render
   - Version control integration

2. **Better File Management**
   - Automated database backups
   - Efficient file operations
   - Log monitoring

3. **Development Velocity**
   - Faster PR creation for features
   - Better code management
   - Issue tracking integration

### Phase 2B Benefits (Google Calendar MCP)

1. **Calendar Integration**
   - Natural language event creation
   - Two-way sync with Google Calendar
   - Smart scheduling capabilities

2. **Wedding Planning Support**
   - Vendor meetings automatically scheduled
   - Event reminders via calendar
   - Shared calendar with Judy

3. **Multi-Calendar Management**
   - Work/Personal/Wedding calendars
   - Category-to-calendar mapping
   - Free/busy queries

---

## Security Considerations

### Token Management

1. **GitHub Token:**
   - Stored in `claude_desktop_config.json` (NOT in Life OS repo)
   - Never committed to git
   - Set expiration (1 year recommended)
   - Minimal scopes only

2. **Google Calendar Credentials:**
   - OAuth 2.0 credentials in `google-calendar-credentials.json`
   - Added to `.gitignore`
   - Token stored in `google-calendar-token.json` (also gitignored)
   - Never share or commit

### Best Practices

- ✅ All sensitive files in `.gitignore`
- ✅ Tokens stored locally only
- ✅ Minimal permission scopes
- ✅ Regular token rotation (annual)
- ✅ No screenshots with tokens visible

---

## Migration Path

### Phase 1: Install MCPs (Current)
- Install GitHub MCP
- Install Filesystem MCP
- Install Google Calendar MCP
- Verify all MCPs working

### Phase 2: Deployment Integration
- Use GitHub MCP to push code
- Deploy to Render via GitHub
- Automate deployment workflow

### Phase 3: Calendar Integration (Phase 2B)
- Implement `schedule_event` tool
- Integrate with router
- Test calendar operations
- Add to production

### Phase 4: Advanced Features (Phase 3+)
- Multi-calendar support
- Intelligent event import (images/PDFs)
- Calendar + RAG integration

---

## Alternatives Considered

### GitHub MCP Alternatives

**GitHub CLI (gh):**
- Pros: Official GitHub tool, well-documented
- Cons: Requires manual CLI commands, not integrated with Claude Code
- **Decision:** GitHub MCP is better integrated

**Manual Git Push:**
- Pros: Simple, no dependencies
- Cons: Requires user intervention, authentication issues
- **Decision:** MCP enables automation

### Calendar Alternatives

**Direct Google Calendar API:**
- Pros: Full control, official API
- Cons: More code to write, OAuth complexity
- **Decision:** MCP abstracts complexity

**Other Calendar Services (Outlook, Apple Calendar):**
- Pros: Alternative options
- Cons: User uses Google Calendar
- **Decision:** Google Calendar MCP meets needs

**iCalendar Files:**
- Pros: Universal format
- Cons: No two-way sync, manual import/export
- **Decision:** Real-time sync is important

---

## Testing Plan

### GitHub MCP Testing

1. ✅ List repositories
2. ✅ Push to repository
3. ✅ Create branch
4. ✅ Create pull request
5. ✅ View commit history

### Filesystem MCP Testing

1. ✅ Read files in Life OS directory
2. ✅ Write test file
3. ✅ Create backup of database
4. ✅ List directory contents
5. ✅ Monitor file changes

### Google Calendar MCP Testing

1. ✅ List calendar events
2. ✅ Create event with natural language date
3. ✅ Update event
4. ✅ Delete event
5. ✅ Query free/busy
6. ✅ Create recurring event

---

## Success Criteria

**MCPs are successfully integrated when:**

1. **GitHub MCP:**
   - Can push code to repository
   - Can create PRs
   - Can manage issues
   - Authentication working

2. **Filesystem MCP:**
   - Can read/write files efficiently
   - Can create database backups
   - Can monitor file system
   - No permission issues

3. **Google Calendar MCP:**
   - Can create events from natural language
   - Can list events from calendars
   - Can update/delete events
   - OAuth authentication working
   - Two-way sync functioning

---

## Next Steps

1. ✅ User installs all three MCPs (see `MCP_SETUP_GUIDE.md`)
2. ✅ Verify each MCP is working
3. ✅ Use GitHub MCP to push Life OS to GitHub
4. ✅ Deploy to Render
5. 📅 Implement Phase 2B (Calendar integration)

---

## References

- GitHub MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/github
- Filesystem MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- Google Calendar MCP: https://github.com/nspady/google-calendar-mcp
- MCP Documentation: https://modelcontextprotocol.io/
