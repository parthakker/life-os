# Transcript Processing Prompt
## Template for Claude Life Dumps

**Created:** October 18, 2024
**Purpose:** Standard prompt for processing voice transcripts
**Use:** Copy this prompt into temp Claude before pasting your transcript

---

## 📋 The Prompt

Copy everything below this line and paste into a new Claude conversation:

---

```
I'm building a Life Operating System to organize everything in my life. I'm about to give you a comprehensive brain dump transcript of everything going on - responsibilities, projects, tasks, ideas, important information, deadlines, etc.

Your job:

1. LISTEN & CATEGORIZE
   - Identify all distinct areas/categories of my life mentioned
   - Create subcategories where it makes sense
   - Organize EVERYTHING I mention into this structure

2. EXTRACT KEY DATA
   For each item, identify:
   - Category & subcategory it belongs to
   - Description
   - Any deadlines/dates mentioned
   - Any costs/amounts
   - Any actions needed (todos)
   - Priority level (if I indicate urgency)
   - Any important reference info (numbers, accounts, etc.)

3. OUTPUT FORMAT

   [SUGGESTED STRUCTURE]
   Show me a category tree with all the areas of my life you identified

   [ORGANIZED ITEMS]
   Everything I mentioned, organized into those categories with extracted data
   Format as:
   - Item | Due: [date] | Cost: [amount] | Action: [todo] | Priority: [level]

   [QUESTIONS/AMBIGUITIES]
   Anything you're unsure about or needs clarification

4. BE THOROUGH
   - Don't skip anything I mention
   - If something could go in multiple categories, note that
   - Capture ALL dates, amounts, names, important details
   - Flag items that seem time-sensitive

Ready? Here's my life dump:

---

[PASTE YOUR TRANSCRIPT BELOW THIS LINE]
```

---

## 🎯 How to Use

### Step 1: Record Your Dump
- Use voice recorder on phone
- Speak naturally about everything on your mind
- Don't worry about organization - just brain dump
- Include deadlines, tasks, ideas, worries, everything

### Step 2: Get Transcript
- Use transcription service (Otter.ai, phone built-in, etc.)
- Copy the full transcript

### Step 3: Process with Claude
- Open new Claude conversation (not this Life OS)
- Paste the prompt above
- Paste your transcript below the prompt
- Send

### Step 4: Review Output
- Claude will give you organized structure + items
- Review for accuracy
- Note any questions Claude asked

### Step 5: Transfer to Life OS
- Copy Claude's organized output
- Paste into `inbox/raw.md`
- Tell Life OS organization agent to process
- Answer any follow-up questions
- Everything gets filed!

---

## 💡 Tips for Better Transcripts

### Do's
✅ Mention deadlines explicitly ("due Oct 21st")
✅ Include amounts ("$5,000")
✅ Name names ("call mom", "meet with Soham")
✅ Specify priorities ("urgent", "important", "whenever")
✅ Mention all life areas
✅ Include ideas even if not actionable yet

### Don'ts
❌ Try to organize while speaking (just dump)
❌ Censor yourself (get it all out)
❌ Skip small things (capture everything)
❌ Worry about categories (Claude will organize)

---

## 📝 Example Transcript

```
Okay so there's a lot going on. First, work stuff - I have that ID&V Rules presentation to Sendos on Monday which is huge, can't forget that. Also Fridays for Fraud with Ariana on Thursday. The DASH Migration is coming up in November so I need to start prepping for that.

Wedding planning is getting intense. We need to pay the venue five thousand dollars by October 10th, that's coming up soon. The wedding is May 3rd, 2026. It's a five-day Indian wedding - Wednesday and Thursday are the haldis and pooja, Friday is sangeet at Rasoi in South Brunswick, Saturday is welcome dinner, and Sunday is the big day at The Grove in Cedar Grove.

Buddy has been having some issues. His vet appointment is October 15th at 3pm for a checkup. I need to ask about those fat growths. Also need to remember his insurance is $275 a month to Nationwide.

Oh and I have that Uplevel Resume contract that's due in two weeks which is critical. Need to really focus on that. Also need to follow up with Hamilton Deli and Jhopri clients.

Home stuff - I really need to automate the HOA payment, keep forgetting that. Brad's rent is due soon, $1,100. And I need to schedule that dryer vent cleaning ASAP.

For friends, I should catch up with Soham soon, haven't talked in a while. And Varun and I are working on that bot project together.

Fantasy football this week - Patriots defense looking good. Might put some bets on the game.

That's about it for now I think...
```

---

## 🔄 After Processing

### What You'll Get from Claude

**1. Suggested Structure**
All the life areas Claude identified in your dump

**2. Organized Items**
Everything you mentioned, categorized with extracted data

**3. Questions**
Anything ambiguous or needing clarification

### Next Steps

1. Review Claude's organization
2. Answer any questions
3. Paste into Life OS `inbox/raw.md`
4. Run organization agent
5. Answer Life OS's questions (if any)
6. Dashboard updates with everything!

---

## 🎤 Voice Dump Frequency

### Recommended Schedule

**Daily Micro-Dumps:**
- End of day brain dump (5-10 min)
- Capture what came up today
- Quick wins for staying current

**Weekly Macro-Dumps:**
- Weekend review (15-20 min)
- Everything on your mind
- Upcoming week planning
- Anything forgotten during week

**Monthly Mega-Dumps:**
- Full life review (30-45 min)
- All areas of life
- Long-term planning
- Refresh Life OS structure

---

## 🔗 Related Docs

- `core-principles.md` - Why we do brain dumps
- `organization-rules.md` - How items get categorized
- `../inbox-processor/instructions.md` - What happens after dump

---

**Last Updated:** October 18, 2024
**Version:** 1.0
**Use this every time you do a brain dump!**
