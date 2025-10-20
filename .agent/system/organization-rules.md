# Organization Rules
## Keyword Detection & Category Mapping Logic

**Created:** October 18, 2024
**Purpose:** Define how items get categorized automatically
**Status:** Living document - updates as agent learns

---

## 🎯 How Categorization Works

### Process
1. Read item from inbox
2. Check for explicit category markers `[CATEGORY]`
3. If not explicit, scan for keywords
4. Match against rules below
5. If confident (>90%), auto-file
6. If ambiguous (<90%), ask user
7. Learn from user's answer
8. Update `keyword-mapping.md`

---

## 👨‍👩‍👦 FAMILY Category

### Keywords
- Family member names: mom, dad, mansi, aayushi, jay, suraj, surekha aunty
- Context: family, parents, sister, brother, cousin, aunt, uncle

### Subcategories
- **Name match** → `family/[person-name]/`
- **General family** → `family/`

### Examples
- "Call mom" → `family/mom/tasks.md`
- "Dad's birthday next month" → `family/dad/dates.md`
- "Family dinner this weekend" → `family/notes.md`

---

## 👥 FRIENDS Category

### Keywords
- Friend names: soham, veenay, jon, varun, akhil, vineeth, vijay, shiraz, viren, steven schilder, shivam
- Context: friend, hangout, catch up

### Subcategories
- **Name match** → `friends/[person-name]/`
- **Multiple friends** → Multiple folders

### Examples
- "Soham's birthday party" → `friends/soham/dates.md`
- "Catch up with Varun" → `friends/varun/tasks.md`
- "Weekend hangout with Jon and Akhil" → Both folders

---

## 💑 PREETI Category

### Keywords
- preeti, fiancé, fiancee, girlfriend, her
- Context: date, gift, relationship, together

### Subcategories
- **Tasks** → `preeti/tasks.md`
- **Date ideas** → `preeti/dates-ideas.md`
- **General** → `preeti/notes.md`

### Examples
- "Preeti wants to try Italian restaurant" → `preeti/dates-ideas.md`
- "Get anniversary gift for Preeti" → `preeti/tasks.md`

---

## 💍 WEDDING Category

### Keywords
- wedding, venue, ceremony, reception, marriage, married, marry
- Event names: haldi, pooja, sangeet, welcome dinner
- Vendor names: (will be added as learned)
- Locations: The Grove, Rasoi

### Subcategories

**By Content Type:**
- Contains $ amount → `wedding/finance.md`
- Contains vendor/venue name → `wedding/vendors/`
- Contains date/deadline → Check event or deadline
- Contains "my task", "I need to" → `wedding/my-todos.md`
- Contains "parents", "mom", "dad" + task → `wedding/parents-tasks.md`
- Contains "for parents" → `wedding/my-tasks-for-parents.md`

**By Event:**
- Keywords: haldi → `wedding/events/haldi-wednesday.md`
- Keywords: pooja → `wedding/events/pooja-thursday.md`
- Keywords: sangeet → `wedding/events/sangeet-friday.md`
- Keywords: welcome dinner → `wedding/events/welcome-dinner-saturday.md`
- Keywords: ceremony, reception → `wedding/events/ceremony-reception-sunday.md`

### Examples
- "Wedding venue payment $5k due 10/10" → `wedding/finance.md` + `wedding/vendors/`
- "Sangeet song list" → `wedding/events/sangeet-friday.md`
- "Parents need to finalize guest list" → `wedding/parents-tasks.md`
- "Pick up parents from airport" → `wedding/my-tasks-for-parents.md`

### Special Rule: Multiple Filing
Wedding items often belong in multiple places. Agent should ask:
"This wedding item could go in multiple places. Where should I file it?"

---

## 💼 WORK Category

### Keywords
- work, job, office, professional, career
- Project names: Not ATO Bot, DASH Migration, PII Tokenization, Notification Strategy
- Systems: ID&V, IDB, LexisNexis, TMX
- Team names: Sendos, Fridays for Fraud, Intelligence Team
- Colleague names: Nicole, Ariana, Elizabeth Scott, Rachel, Jay (context: work)

### Subcategories

**By Project Area:**
- Keywords: RCA, account, backlog, trends, digital compromise → `work/high-dollar-rcas/`
- Keywords: ID&V, IDB, rules, governance, controls → `work/governance-controls/`
- Keywords: Not ATO Bot, DASH, PII, tokenization, notification → `work/major-projects/`

**Within Major Projects:**
- "Not ATO Bot" → `work/major-projects/not-ato-bot.md`
- "DASH Migration" → `work/major-projects/dash-migration.md`
- "PII Tokenization" → `work/major-projects/pii-tokenization.md`

**General:**
- No specific project → `work/tasks.md`
- Deadline mentioned → Also add to `work/deadlines.md`
- Networking/people → `work/networking.md`

### Examples
- "ID&V Rules presentation to Sendos Monday" → `work/governance-controls/idv-rules-docs.md` + `work/deadlines.md`
- "DASH Migration heavy work in November" → `work/major-projects/dash-migration.md`
- "Coffee with Rachel" → `work/networking.md`
- "Pen report with Nicole next week" → `work/tasks.md` + `work/deadlines.md`

---

## 🏠 HOME Category

### Keywords
- home, house, property, maintenance
- Bills: mortgage, tax, taxes, HOA, electric, electricity, water, sewage, wifi, internet, xfinity
- Tenant: Brad, rent, rental
- Maintenance: repair, fix, broken, cleaning, service

### Subcategories

**Bills:**
- Keywords: mortgage, tax → `home/bills/mortgage.md`
- Keywords: HOA → `home/bills/hoa.md`
- Keywords: electric, water, sewage, wifi, xfinity → `home/bills/utilities.md`
- Keywords: property tax → `home/bills/taxes.md`

**Tenant:**
- Keywords: Brad, rent, tenant → `home/tenant/brad-rent.md`

**Maintenance:**
- Keywords: repair, fix, cleaning, service → `home/maintenance.md`

### Examples
- "HOA payment $X due Y" → `home/bills/hoa.md`
- "Collect rent from Brad" → `home/tenant/brad-rent.md`
- "Dryer vent cleaning" → `home/maintenance.md`

---

## 🐕 BUDDY Category

### Keywords
- Buddy, dog, puppy, vet, veterinarian
- Medical: health, sick, medication, medicine, prescription
- Insurance: Nationwide, pet insurance
- Care: bath, grooming, food, supplies

### Subcategories
- Keywords: vet, appointment, checkup, exam → `buddy/vet-appointments.md` OR `buddy/health.md`
- Keywords: health, sick, issue, problem, fat growths, teeth → `buddy/health-issues.md`
- Keywords: medical records, Blue Pearl, Princeton Animal Hospital → `buddy/medical-records.md`
- Keywords: insurance, Nationwide, payment → `buddy/insurance.md`
- Keywords: bath, grooming, food, prescription, supplies → `buddy/care-schedule.md` OR `buddy/supplies.md`

### Examples
- "Buddy vet appointment 10/15 for checkup" → `buddy/vet-appointments.md`
- "Buddy fat growths check" → `buddy/health-issues.md`
- "Insurance payment $275 monthly" → `buddy/insurance.md`
- "Buddy needs prescription food" → `buddy/supplies.md`

---

## 💪 FITNESS Category

### Keywords
- gym, workout, exercise, fitness, training
- jujitsu, bjj, martial arts, class

### Subcategories
- Keywords: gym, workout → `fitness/gym.md`
- Keywords: jujitsu, bjj, class → `fitness/jujitsu.md`

### Examples
- "Gym session Tuesday" → `fitness/gym.md`
- "Jujitsu class schedule" → `fitness/jujitsu.md`

---

## 🎮 HOBBIES Category

### Keywords
- hobby, fun, recreation, leisure
- NFL, football, fantasy, madden, patriots, betting (sports context)
- Video games, gaming, playstation, league of legends, LOL
- Guitar, music, practice
- Photography, photo, camera, shoot

### Subcategories

**NFL:**
- Keywords: NFL, fantasy football → `hobbies/nfl/fantasy-football.md`
- Keywords: madden → `hobbies/nfl/madden.md`

**Video Games:**
- Keywords: League of Legends, LOL → `hobbies/video-games/league-of-legends.md`
- Keywords: PlayStation, PS5, game → `hobbies/video-games/playstation.md`
- General gaming → `hobbies/video-games/games-list.md`

**Other:**
- Keywords: guitar, music, practice → `hobbies/guitar.md`
- Keywords: photography, photo, camera → `hobbies/photography.md`

### Examples
- "Patriots defense looks good for week 7" → `hobbies/nfl/fantasy-football.md`
- "New League of Legends patch" → `hobbies/video-games/league-of-legends.md`
- "Guitar practice schedule" → `hobbies/guitar.md`

### Special Note: Betting
See SIDE HUSTLES - Betting (business context) vs Hobbies (sports betting for fun)

---

## 💰 SIDE HUSTLES Category

### Keywords
- side hustle, business, client, contract, project, income, revenue
- Princeton AI, Princeton AI Partners, Uplevel, Hamilton Deli, Jhopri
- Betting (business context), bankroll, ROI, profit, strategy

### Subcategories

**Princeton AI Partners:**
- Keywords: Uplevel Resume, Uplevel → `side-hustles/princeton-ai/uplevel-resume.md`
- Keywords: Uplevel website → `side-hustles/princeton-ai/uplevel-website.md`
- Keywords: Hamilton Deli, deli client → `side-hustles/princeton-ai/hamilton-deli.md`
- Keywords: Jhopri → `side-hustles/princeton-ai/jhopri.md`
- Company website → `side-hustles/princeton-ai/company-website.md`

**Betting (Business):**
- Keywords: bet, betting, active bets → `side-hustles/betting/active-bets.md`
- Keywords: bet tracking, screenshot bets → `side-hustles/betting/bet-tracking.md`
- Keywords: bankroll, ROI, profit → `side-hustles/betting/bankroll.md`

### Examples
- "Uplevel Resume contract due in 2 weeks" → `side-hustles/princeton-ai/uplevel-resume.md`
- "Follow up with Hamilton Deli client" → `side-hustles/princeton-ai/hamilton-deli.md`
- "Active bet on Patriots -3.5" → `side-hustles/betting/active-bets.md`

---

## 🚀 PERSONAL PROJECTS Category

### Keywords
- personal project, idea, build, create
- Personal Assistant AI, NFL website, bot with Varun

### Subcategories
- Keywords: personal assistant, AI assistant → `personal-projects/personal-assistant-ai.md`
- Keywords: NFL website, South Asia, learning → `personal-projects/nfl-learning-website.md`
- Keywords: bot with Varun, Varun bot → `personal-projects/bot-with-varun.md`

### Examples
- "Personal Assistant AI with internet access" → `personal-projects/personal-assistant-ai.md`
- "NFL learning website for South Asia" → `personal-projects/nfl-learning-website.md`

---

## 🔍 Detection Patterns

### Date Detection
**Formats recognized:**
- MM/DD, MM/DD/YYYY
- "due [date]", "by [date]", "on [date]"
- "next week", "next month"
- Day names: "Monday", "Tuesday", etc.
- Months: "October", "November", etc.

**Action:**
- Extract date
- Add to appropriate file
- If deadline, flag for dashboard "Next 7 Days"

### Money Detection
**Patterns:**
- $XXX, $X,XXX, $XX.XX
- "cost", "payment", "bill", "price"

**Action:**
- Extract amount
- Format as: `$X,XXX`
- Flag for finance tracking

### Priority Detection
**Keywords:**
- **Critical/High:** urgent, ASAP, critical, important, deadline, due soon
- **Medium:** soon, upcoming, next week
- **Low:** eventually, someday, maybe, idea

**Action:**
- Tag with priority level
- Critical items → Dashboard "Today" section

### Action Detection
**Keywords:**
- "need to", "should", "must", "have to", "remember to", "don't forget"

**Action:**
- Mark as task with `- [ ]` checkbox
- Add to appropriate tasks file

---

## 🤔 Ambiguity Rules

### When to Ask Questions

**Multiple Categories Possible:**
- "Gym membership $50/month" → Could be: Hobbies > Fitness OR Home > Bills
- ASK: "Is this a hobby expense or a home bill?"

**New Item Type:**
- Never seen before
- No matching keywords
- ASK: "I haven't seen '[item]' before. Which category should this go in?"

**Unclear Context:**
- "Jay wants to talk about the project"
- Could be: Family (Jay the person) OR Work (project)
- ASK: "Is this about family member Jay or a work project?"

### When NOT to Ask

**High Confidence Match:**
- Clear keywords match exactly
- Pattern matches previous items
- Only one logical category

**Low Importance:**
- General notes without action items
- Can always be moved later

---

## 📚 Learning & Updates

### After User Answers Question

**Process:**
1. File item per user's answer
2. Update `keyword-mapping.md` with new pattern
3. Log to `organization-log.md`
4. Next time similar item appears → Auto-file

**Example:**
- Q: "Gym membership - hobby or bill?"
- A: "Bill"
- Update: Add to rules: "gym, fitness membership → home/bills/"
- Next: "Jujitsu membership $X" → Auto-files to home/bills/

### Continuous Improvement

**Track:**
- How often questions asked (should decrease)
- How often users correct auto-filing (should decrease)
- How accurate predictions are (should increase)

**Update this file when:**
- New categories added
- New patterns discovered
- Rules change based on usage

---

## 🔗 Related Docs

- `keyword-mapping.md` - Your specific learned keywords
- `category-tree.md` - Current folder structure
- `data-format-spec.md` - How to format filed items
- `../inbox-processor/instructions.md` - Step-by-step organization process

---

**Last Updated:** October 18, 2024
**Version:** 1.0
**Status:** Living document - updates as agent learns
**Next Update:** After processing first batch of data
