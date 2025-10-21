# Changelog

All notable changes to Life OS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-10-21

### 🎉 Initial Production Release

**First fully functional, production-deployed version of Life OS!**

This release represents the completion of Phase 2A (RAG System) and successful migration to a production-ready, cost-efficient architecture running on Render.

### ✅ Verified

- [x] 3/4 critical tests passed in production
- [x] Bot responding to Telegram messages
- [x] RAG search working with OpenAI embeddings
- [x] Auto-vectorization working correctly
- [x] No crashes or errors in production
- [x] Memory usage stable (~110MB vs 520MB before)

### Added

**Core Features:**
- Agentic router using Claude 3.5 Haiku for natural language understanding
- 3 core tools: `add_task`, `add_note`, `ask_question`
- Custom JSON-based vector store with semantic search
- Auto-vectorization of all tasks and notes
- 41 categories across all life domains
- Telegram bot interface for natural language interaction
- RAG (Retrieval Augmented Generation) system for semantic search

**Infrastructure:**
- Production deployment to Render (Background Worker)
- Auto-deploy on push to main branch
- Environment variable management
- SQLite database for persistent storage
- OpenAI embeddings integration (text-embedding-3-small)

**Documentation:**
- Complete README with architecture overview
- Product overview and vision document
- Deployment guide for Render
- MCP setup guide (GitHub, Filesystem, Google Calendar)
- Quick start testing guide
- Version 1.0 release notes
- Comprehensive decision logs
- System architecture documentation
- Session summaries and logs

**Developer Tools:**
- MCP (Model Context Protocol) integration
- GitHub MCP for repository management
- Filesystem MCP for better file operations
- Google Calendar MCP configured (ready for Phase 2B)

### Changed

**Major Architecture Changes:**
- Migrated from torch/sentence-transformers to OpenAI Embeddings API
- Memory footprint reduced from 520MB to 110MB (78% reduction)
- Improved embedding quality (text-embedding-3-small > all-MiniLM-L6-v2)
- Monthly cost reduced from $25.36 to $7.37 (saves $216/year)

**Codebase Cleanup:**
- Reduced from 99 files to 27 essential files
- Archived old dashboard implementation
- Removed legacy scripts and markdown files
- Clean, production-ready structure

### Fixed

**Critical Bugs:**
- **[CRITICAL]** Fixed `add_to_vector_store()` still using old torch code (commit e00eb6c)
  - Changed from `embedding_model.encode()` to `get_embedding()`
  - This was causing "embedding_model is not defined" errors
  - Prevented auto-vectorization of new tasks/notes
  - Verified fixed with production testing

**Other Fixes:**
- Memory optimization to prevent OOM crashes on Render
- Environment variable configuration for production
- Auto-deploy configuration on Render

### Known Issues

- Semantic search precision can be improved (Test 4 partial pass)
  - Query "Do I need to call anyone?" didn't prioritize "call mom" task
  - Not critical for v1.0, can be tuned in future version
  - RAG search fundamentally working correctly

### Technical Details

**Dependencies:**
```
python-telegram-bot==21.0
anthropic==0.71.0
openai>=1.55.3
numpy==2.0.2
psycopg2-binary==2.9.9
flask==3.1.0
flask-cors==5.0.0
```

**Deployment:**
- Platform: Render
- Service Type: Background Worker
- Region: Ohio
- Memory: 512MB allocated, ~110MB used
- Service ID: srv-d3r9ocbe5dus73b4vs4g

**Environment Variables:**
- TELEGRAM_BOT_TOKEN
- TELEGRAM_USER_ID
- ANTHROPIC_API_KEY
- OPENAI_API_KEY

**Cost Analysis:**
- Render Starter: $7.00/month
- Claude Haiku API: ~$0.36/month
- OpenAI Embeddings: ~$0.01/month
- **Total: $7.37/month**

**Commits in This Release:**
- de13b19 - Backup before migration
- 4eb5b48 - OpenAI migration code
- 1dc821e - OpenAI vector store upload
- cf76542 - Post-migration cleanup and documentation
- e00eb6c - CRITICAL FIX: Update add_to_vector_store to use OpenAI API
- 441f0d1 - Document critical bug fix and verification steps
- cb433a9 - Add restart handoff for Render MCP verification

### Testing

**Test Results (Production):**
- Test 1: Basic task creation - ✅ PASSED
- Test 2: RAG search - ✅ PASSED
- Test 3: Auto-vectorization - ✅ PASSED
- Test 4: Semantic search precision - ⚠️ PARTIAL

**Success Rate: 75% (3/4 critical tests passed)**

### Migration Notes

**From torch to OpenAI Embeddings:**

Before (torch-based):
- Memory: ~520MB
- Dependencies: torch + sentence-transformers
- Cost: Required $25/month Render plan
- Quality: all-MiniLM-L6-v2 embeddings

After (OpenAI-based):
- Memory: ~110MB
- Dependencies: openai SDK only
- Cost: $7/month Render + $0.01/month API
- Quality: text-embedding-3-small (better)

**Why This Migration:**
- Render's 512MB limit caused OOM crashes
- torch + sentence-transformers = restart loop
- Service completely unusable before migration
- OpenAI API more cost-effective than RAM upgrade

### Security

- All API keys stored as environment variables
- Sensitive files (data.db, vector_store.json) gitignored
- Telegram user ID validation for access control
- No credentials committed to repository

---

## [Unreleased]

### Planned for v1.1.0 (Phase 2B)

**Google Calendar Integration:**
- Natural language event creation
- "schedule dinner with mom next Friday at 7pm"
- Two-way sync with Google Calendar
- Calendar event search via RAG

### Planned for v1.2.0 (Phase 2C)

**Calendar + RAG Integration:**
- Combined task/note/event search
- Automatic calendar event vectorization
- "when am I seeing mom?" queries

### Planned for v2.0.0 (Phase 3B)

**Intelligent Import - Images/PDFs:**
- Claude Vision API for OCR
- Forward vendor contracts → extract event details
- Screenshot event flyers → create calendar events
- Confirmation flow for extracted data

---

## Version History

- **v1.0.0** (2025-10-21) - Initial production release
- Future releases planned in Phase 2B-4 roadmap

---

## Migration Guide

### Upgrading from Pre-v1.0

If you have a local installation from before v1.0:

1. **Backup your data:**
   ```bash
   cp data.db data.db.backup
   cp vector_store.json vector_store.json.backup
   ```

2. **Update dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

4. **Re-vectorize existing items:**
   ```bash
   python scripts/migrate_to_openai.py
   ```

5. **Test locally:**
   ```bash
   python scripts/telegram_bot.py
   ```

---

## Support

- **Repository:** https://github.com/parthakker/life-os
- **Issues:** https://github.com/parthakker/life-os/issues
- **Documentation:** See `VERSION_1.0_RELEASE.md` for complete release notes

---

**Life OS v1.0 - Your AI-powered personal assistant** 🤖
