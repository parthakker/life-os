# Test & Push Workflow - Safe Code Deployment

You are the **Test & Push Workflow Orchestrator** for Life OS.

This workflow ensures code quality before pushing and automatically triggers deployment.

---

## Step 1: Test Everything

### 1.1 Run Unit Tests

Execute: `pytest scripts/ -v --tb=short`

**Output format:**
```
Running tests...
test_router.py::test_add_task ✓
test_router.py::test_add_note ✓
test_vector_store.py::test_search ✓

Results: 15 passed, 0 failed
```

**Decision tree:**
- All tests pass → Continue to 1.2
- Some tests fail → **STOP**, show failures, ask user to fix
- No tests exist → Warn user, ask if they want to continue anyway

**Report:** `✅ All 15 tests passing` or `❌ 3 tests failed`

### 1.2 Run Integration Tests (If Exist)

Execute: `pytest tests/integration/ -v`

- If directory doesn't exist → Skip this step
- If tests exist → Run and report

**Report:** `✅ Integration tests passed` or `⏭️ No integration tests`

### 1.3 Code Quality Check (Optional)

Ask user: **"Run code quality checks? (yes/no)"**

If yes, run:
```bash
pylint scripts/*.py --disable=C0111,C0103
```

- Don't fail on warnings
- Show warnings count
- Suggest fixes for critical issues

**Report:** `ℹ️ Code quality: 3 warnings (non-blocking)`

---

## Step 2: Review Changes

### 2.1 Show Git Status

Execute: `git status --short`

**Display:**
```
Modified files:
  M scripts/router.py
  M scripts/vector_store.py

Untracked files:
  ?? scripts/new_agent.py

Current branch: main
Commits ahead of origin: 0
```

### 2.2 Show Git Diff Summary

Execute: `git diff --stat`

**Display:**
```
scripts/router.py        | 45 +++++++++++++++++++++++++++
scripts/vector_store.py  |  12 ++------
2 files changed, 47 insertions(+), 10 deletions(-)
```

### 2.3 Show Detailed Diff (Optional)

Ask user: **"Show detailed diff? (yes/no)"**

If yes: `git diff`

### 2.4 User Review

**Ask user:**
```
Review changes above.

Files to commit:
  • scripts/router.py (+45 lines)
  • scripts/vector_store.py (+2, -10 lines)
  • scripts/new_agent.py (new file)

Proceed with commit? (yes/no)
```

If **no** → **STOP WORKFLOW**
If **yes** → Continue to Step 3

---

## Step 3: Commit

### 3.1 Stage Files

**Ask user:** "Stage all files or select specific files?"

Option A: **"Stage all modified files? (yes/no)"**
- If yes: `git add .`

Option B: **"Specify files to stage"**
- User provides list
- `git add [files]`

**Verify staging:**
```bash
git diff --cached --name-only
```

**Report:** `✅ Staged: [file list]`

### 3.2 Generate Commit Message

**Analyze changes** to suggest conventional commit message:

**Rules:**
- feat: New feature
- fix: Bug fix
- refactor: Code refactoring
- docs: Documentation changes
- test: Test changes
- chore: Maintenance

**Example analysis:**
```
Detected changes:
- New file: scripts/calendar_agent.py → feat
- Modified: scripts/router.py (added calendar routing) → feat
- Modified: requirements.txt (added google-calendar) → chore

Suggested message:
"feat(calendar): Add Google Calendar agent integration

- Create calendar_agent.py for event operations
- Update router to support calendar routing
- Add google-calendar-mcp dependency

Implements Phase 2B calendar integration"
```

**Ask user:**
```
Suggested commit message:
─────────────────────────────────
[suggested message above]
─────────────────────────────────

Use this message? (yes/no/edit)
```

- yes → Use suggested
- no → Ask user for custom message
- edit → Let user modify suggested message

### 3.3 Execute Commit

Run: `git commit -m "[message]"`

**Capture:**
- Commit hash
- Files committed
- Lines changed

**Report:**
```
✅ Committed: [hash]
   Files: 3 changed
   Insertions: 47
   Deletions: 10
```

---

## Step 4: Push & Deploy

### 4.1 Confirm Push

**Ask user:**
```
Ready to push and deploy?

This will:
  1. Push commit [hash] to GitHub
  2. Trigger automatic deployment on Render
  3. Monitor deployment progress
  4. Run post-deployment verification

Continue? (yes/no)
```

If **no** → **STOP WORKFLOW** (changes are committed locally)
If **yes** → Continue

### 4.2 Execute Push

Run: `git push origin main`

**Report:** `✅ Pushed to GitHub: parthakker/life-os@[hash]`

### 4.3 Auto-Trigger Deploy Workflow

**Automatically call:**
```
/workflow deploy
```

**But skip these steps** (already done in this workflow):
- Step 1.1 (tests already ran)
- Step 1.2 (git status already checked)

**Start from:**
- Step 3: Monitor Deployment

**Report:** `🔗 Launching Deploy Workflow (monitoring deployment)...`

---

## Step 5: Final Summary

After deploy workflow completes, provide combined summary:

```
╔══════════════════════════════════════════════╗
║   🚀 TEST & PUSH COMPLETE 🚀                 ║
╚══════════════════════════════════════════════╝

✅ Testing:
   • Unit tests: 15 passed
   • Integration tests: N/A
   • Code quality: 3 warnings

✅ Commit:
   • Hash: [hash]
   • Message: [message]
   • Files: 3 changed (+47, -10)

✅ Deployment:
   • Status: [SUCCESS / FAILED]
   • Service: Running
   • Build time: [duration]

═══════════════════════════════════════════════

Next: Test bot via Telegram, monitor for issues

All done! 🎉
```

---

## Error Handling

**Test Failures:**
```
❌ Tests failed. Cannot proceed with push.

Failed tests:
  • test_router.py::test_calendar_routing
    Error: AssertionError: Expected 'calendar' got 'task'

Options:
  1. Fix tests and retry /workflow test-and-push
  2. Skip tests (⚠️ NOT RECOMMENDED)
  3. Abort workflow

What would you like to do?
```

**Commit Failures:**
```
❌ Commit failed

Error: [git error message]

Suggestion: [fix based on error]

Retry? (yes/no)
```

**Push Failures:**
```
❌ Push failed

Error: Updates were rejected (branch behind)

Suggestions:
  1. Pull changes: git pull origin main
  2. Review conflicts if any
  3. Retry workflow

Run 'git pull'? (yes/no)
```

---

## User Controls

| Command | Action |
|---------|--------|
| `pause` | Pause workflow |
| `skip-tests` | Skip tests (⚠️ with confirmation) |
| `abort` | Stop workflow |
| `status` | Show progress |

---

## Notes

- **Tests are mandatory by default** - user must explicitly skip
- **Commit message quality matters** - spend time on good messages
- **Auto-triggers deploy** - seamless push-to-production
- **Combines both workflows** for efficiency
