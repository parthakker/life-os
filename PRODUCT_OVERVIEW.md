# Life OS - Product Overview

**Your External Brain: Capture Everything, Search Anything**

---

## 🎯 What Is Life OS?

Life OS is an **AI-powered personal organization system** that acts as your external memory. Brain-dump anything via Telegram—tasks, notes, workout logs, screenshots, documents—and ask questions later to instantly retrieve organized information.

**Core Philosophy**: Pure organization and retrieval. No recommendations, no insights, no "what should I do today"—just **flawless memory** and **instant recall**.

---

## ⚡ The Problem Life OS Solves

**Before Life OS:**
- Information scattered across apps (Notes, Notion, Calendar, spreadsheets)
- Manual categorization and tagging
- Difficult to remember where you saved something
- "Did I bench press twice last week or three times?"
- "What was my weight from my last InBody scan?"
- "What bets did I place on FanDuel last Sunday?"

**With Life OS:**
- Text/voice message anything to Telegram
- AI automatically organizes it
- Ask questions in natural language
- Get instant, relevant answers

---

## 🚀 How It Works

### 1. **Capture** (Brain Dump Anywhere)
Send messages to your Telegram bot in plain English:

```
"workout 10/20 was bench press 3 sets 10 reps at 135 lbs for all reps"
"buy groceries tomorrow"
"florist 1 and 2 were great options for the wedding"
"schedule venue walkthrough next Tuesday at 2pm"
```

**Or** forward images/documents:
- InBody fitness scan → Auto-extract weight, BMI, muscle mass
- FanDuel betting screenshot → Log bets with stakes and odds
- Vendor contract PDF → Extract meeting dates and details
- Receipt photo → Save for expense tracking
- Any screenshot, photo, or document with information to remember

### 2. **Organize** (AI Handles It Automatically)
Claude AI instantly:
- Categorizes into 41 life areas (Wedding, Gym, Betting, Home, etc.)
- Identifies tasks vs notes vs events
- Extracts dates, numbers, and key details
- Converts everything to searchable embeddings

**You don't think about organization—it just happens.**

### 3. **Retrieve** (Ask Questions Naturally)
Ask questions like you'd ask a friend:

```
"what was my bench press info from last week"
"how many times did I do arms last week"
"what are my wedding tasks"
"what was my weight from my last InBody scan"
"show me my FanDuel bets from Sunday"
```

Life OS searches semantically and returns ranked results instantly.

---

## 💎 Key Features

### **Current (Phase 2A - Production)**
✅ **Semantic Search** - RAG-powered natural language queries
✅ **Instant Capture** - Telegram bot available 24/7
✅ **Auto-Categorization** - 41 categories across all life areas
✅ **Smart Date Parsing** - "tomorrow", "next week", "March 15"
✅ **Auto-Vectorization** - New items instantly searchable
✅ **Cloud Deployed** - Render (always-on, $7/month)
✅ **PostgreSQL Database** - Production-grade data persistence

### **Coming Soon (Phase 2B-3)**
🔜 **Google Calendar Integration** - Read/write/edit events
🔜 **Image Intelligence** - Upload photos, extract structured data
🔜 **PDF Import** - Forward contracts/documents, auto-extract info
🔜 **Multi-Modal Search** - Search across text, images, events

### **Future Vision (Phase 4+)**
🔮 **Voice Messages** - Transcribe and organize automatically
🔮 **Web Dashboard** - View and manage everything visually
🔮 **Advanced Querying** - "Did I improve my bench press since last month?"
🔮 **Multi-Calendar Support** - Work, Personal, Wedding calendars

---

## 📖 Real-World Use Cases

### **Fitness Tracking**
**Capture:**
```
You: "workout 10/20 was bench press 3 sets 10 reps at 135 lbs"
You: *uploads InBody scan photo*
```

**Retrieve:**
```
You: "what was my bench press info from last week"
Bot: 💭 Found 2 workout logs:
     📝 [Gym] 10/20 - Bench press 3x10 at 135 lbs
     📝 [Gym] 10/17 - Bench press 3x8 at 130 lbs

You: "how many times did I bench press last week"
Bot: 💭 Found 2 bench press sessions last week (Oct 14-20)

You: "what was my weight from my last InBody scan"
Bot: 💭 [Gym] InBody Scan 10/15/2025
     Weight: 185 lbs, BMI: 24.2, Muscle Mass: 142 lbs
```

### **Sports Betting Logs**
**Capture:**
```
You: *screenshots FanDuel bet*
Bot: 📸 Bet logged:
     Eagles vs Cowboys, Eagles -3.5, $50 at -110
```

**Retrieve:**
```
You: "show me my FanDuel bets from last Sunday"
Bot: 💭 Found 3 bets from Sunday, Oct 13:
     🎰 Eagles -3.5, $50 at -110
     🎰 Over 47.5, $25 at -105
     🎰 Parlay: Eagles + Over, $20 at +260
```

### **Wedding Planning**
**Capture:**
```
You: "florist 1 and 2 were great, florist 3 was too expensive"
You: "schedule final venue walkthrough March 15 at 2pm"
You: *forwards vendor contract PDF*
```

**Retrieve:**
```
You: "what are my wedding tasks"
Bot: 💭 Found 8 wedding tasks:
     ⏳ [Wedding] Book photographer
     ⏳ [Wedding] Send invitations
     ⏳ [Wedding] Choose menu
     ...

You: "which florists did we like"
Bot: 💭 [Wedding] Florist 1 and 2 were great, florist 3 was too expensive
```

### **General Life Organization**
**Capture:**
```
You: "buy milk tomorrow"
You: "call mom next week"
You: "i really enjoyed The Last of Us episode 3"
```

**Retrieve:**
```
You: "what do i need to buy"
You: "who do i need to call"
You: "what shows have i been watching"
```

---

## 🧠 What Makes Life OS Different

### **1. Organization Tool, Not Recommendation Engine**
Life OS **remembers and retrieves**—it doesn't tell you what to do.

❌ "You should work out today"
✅ "How many times did I work out last week?"

❌ "Based on your patterns, bet on the Eagles"
✅ "Show me my betting history for Eagles games"

### **2. Universal Input, Semantic Output**
- **Input**: Natural language, images, PDFs, voice (future)
- **Processing**: AI extracts structure automatically
- **Output**: Instant semantic search across everything

### **3. Zero Manual Organization**
No folders. No tags. No rigid structure.
Just text the bot like a friend.

### **4. Calendar as First-Class Citizen**
Full Google Calendar integration:
- Create events: "schedule dinner with mom next Friday at 7pm"
- Query calendar: "what's on my calendar tomorrow"
- Edit events: "move dentist appointment to 3pm"
- Search calendar: "when is my venue walkthrough"

---

## 🏗️ System Architecture (High-Level)

```
You (Telegram)
      ↓
Telegram Bot (24/7 on Render)
      ↓
AI Router (Claude 3.5 Haiku)
      ↓
  ┌───┴───────┬──────────────┐
  ↓           ↓              ↓
add_task   add_note    ask_question
  ↓           ↓              ↓
PostgreSQL  PostgreSQL   RAG Search
  ↓           ↓              ↓
Auto-Vectorize (instant searchability)
```

**Key Technology:**
- **RAG (Retrieval-Augmented Generation)**: Semantic search using vector embeddings
- **Auto-Vectorization**: New items immediately searchable
- **PostgreSQL**: Production database for tasks/notes
- **JSON Vector Store**: 384-dimensional embeddings for semantic search
- **Claude 3.5 Haiku**: Fast, cost-effective agentic routing

*For technical deep-dive, see `TECHNICAL_ARCHITECTURE.md`*

---

## 📊 Current Status

**Phase:** 2A Production (RAG System Complete)
**Deployment:** Render (srv-d3r6u5ogjchc73bsiibg)
**Database:** PostgreSQL (lifeos)
**Cost:** ~$7.36/month ($7 Render + $0.36 Claude API)
**Uptime:** 24/7

**Statistics:**
- 41 categories across all life areas
- 95+ items vectorized and searchable
- <1 second search latency
- 100% uptime on Render

---

## 🛣️ Roadmap

### **Phase 2B: Calendar Integration** (Week 2)
- Google Calendar read/write/edit
- Natural language event creation
- "schedule dinner next Friday at 7pm"
- Calendar-aware RAG search

### **Phase 2C: Calendar + RAG** (Week 2)
- Vectorize calendar events
- Unified search across tasks/notes/events
- "what are my wedding events this week"

### **Phase 3B: Intelligent Import - Images/PDFs** (Week 3-4) **[HIGH PRIORITY]**
- Upload any image → Extract structured data
- Current use cases: InBody scans, betting screenshots
- Future: Receipts, contracts, business cards, event flyers
- Confirmation flow before saving
- Multi-modal search

### **Phase 3C: Web Link Import** (Week 4)
- Share Eventbrite links → Auto-create events
- Facebook events → Import automatically
- Parse structured data from web pages

### **Phase 4: Advanced Features** (Future)
- Voice message transcription
- Web dashboard for visual management
- Multi-calendar support (Work, Personal, Wedding)
- Conflict detection for events
- Advanced analytics (trends over time)

---

## 🎯 Success Metrics

**Phase 2A (Current):**
- ✅ 95+ items vectorized
- ✅ <1 second search latency
- ✅ Auto-vectorization working
- ✅ Cost: ~$7.36/month

**Phase 3B Target (Intelligent Import):**
- >90% data extraction accuracy
- <10 second processing time
- User confirms without edits 80%+ of time

---

## 💰 Cost Analysis

**Current (Phase 2A):**
- Render Background Worker: $7.00/month (always-on)
- PostgreSQL: $0.00/month (free tier)
- Claude Haiku API: ~$0.36/month (20 msgs/day)
- **Total: ~$7.36/month**

**Phase 3 Estimate (with Image/PDF Processing):**
- Render: $7.00/month
- PostgreSQL: $0.00/month (still within free tier)
- Claude API: ~$1-2/month (vision API for images)
- **Total: ~$8-9/month**

**ROI:**
- Replaces: Notion ($10/mo), Todoist ($5/mo), scattered notes apps
- Saves: Hours per week in manual organization
- Value: Never forget anything again

---

## 🔐 Privacy & Security

**Your Data Is Yours:**
- Single-user system (Telegram user ID whitelist)
- No third-party data sharing
- Full control over your information
- Self-hosted option available

**Security:**
- All credentials in environment variables
- PostgreSQL connection encrypted
- Render-managed infrastructure
- Regular backups recommended

---

## 🚀 Getting Started

### **For Users:**
1. Message the Telegram bot (provided separately)
2. Start brain-dumping: tasks, notes, thoughts
3. Ask questions to retrieve information
4. That's it—AI handles the rest

### **For Developers:**
See `TECHNICAL_ARCHITECTURE.md` for:
- Setup instructions
- Database schema
- RAG implementation details
- Deployment guide
- Code structure

---

## 🎉 The Vision

Life OS is your **external brain**—a system that:
- **Remembers everything** you tell it
- **Organizes automatically** without your input
- **Retrieves instantly** with natural language
- **Evolves with you** as your needs change

From fitness tracking to wedding planning, from betting logs to daily tasks, Life OS is the **universal memory system** for modern life.

**No recommendations. No judgments. Just perfect recall.**

---

**Version:** 2.0 (Phase 2A Production)
**Last Updated:** October 20, 2025
**Status:** Deployed and operational
**Repository:** https://github.com/parthakker/life-os

---

*Built with Claude Code*
