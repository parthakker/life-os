# MCP Setup Guide for Life OS

This guide walks you through installing Model Context Protocol (MCP) servers for Claude Code.

## Prerequisites

- Claude Code installed
- Node.js and npm installed (for npx commands)
- GitHub account
- Google account (for Calendar MCP)

---

## 1. GitHub MCP Setup

**Purpose:** Enable Claude Code to push to GitHub, manage repositories, create PRs, and handle issues.

### Step 1: Create GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name: `Claude Code MCP`
4. Expiration: No expiration (or 1 year)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read org and team membership)
   - ✅ `workflow` (Update GitHub Action workflows)
6. Click **"Generate token"**
7. **Copy the token immediately** (you won't see it again)

### Step 2: Configure Claude Code

1. Open Claude Code settings file:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Add the GitHub MCP configuration:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE"
      }
    }
  }
}
```

3. Replace `YOUR_TOKEN_HERE` with your actual token

4. Restart Claude Code

### Step 3: Verify Installation

- Open Claude Code
- Try: "Can you see my GitHub repositories?"
- If MCP is working, I'll be able to list your repos

---

## 2. Filesystem MCP Setup

**Purpose:** Better file operations, backups, and database management for Life OS.

### Step 1: Configure Claude Code

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\parth\\OneDrive\\Desktop\\life-os"
      ]
    }
  }
}
```

**Note:** Update the path if your Life OS directory is different.

### Step 2: Restart Claude Code

### Step 3: Verify Installation

- Try: "Can you read the files in my Life OS directory?"
- I should be able to access files more efficiently

---

## 3. Google Calendar MCP Setup

**Purpose:** Enable calendar integration for Phase 2B (schedule events, list events, update/delete).

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Create new project: **"Life OS Calendar"**
3. Wait for project creation (30 seconds)

### Step 2: Enable Google Calendar API

1. Go to **APIs & Services** → **Library**
2. Search for **"Google Calendar API"**
3. Click **"Enable"**

### Step 3: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: **Life OS**
   - User support email: Your email
   - Developer contact: Your email
   - Click **Save and Continue**
   - Scopes: Skip for now
   - Test users: Add your email
   - Click **Save and Continue**

4. Back to **Create OAuth client ID**:
   - Application type: **Desktop app**
   - Name: **Life OS MCP**
   - Click **Create**

5. Download the JSON credentials file
   - Click **Download JSON**
   - Save as: `C:\Users\parth\OneDrive\Desktop\life-os\google-calendar-credentials.json`

### Step 4: Add to .gitignore

**IMPORTANT:** Add to `.gitignore` to prevent committing credentials:

```
# Google Calendar credentials
google-calendar-credentials.json
google-calendar-token.json
```

### Step 5: Configure Claude Code

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\parth\\OneDrive\\Desktop\\life-os"
      ]
    },
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "google-calendar-mcp"],
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "C:\\Users\\parth\\OneDrive\\Desktop\\life-os\\google-calendar-credentials.json"
      }
    }
  }
}
```

### Step 6: First-Time Authorization

1. Restart Claude Code
2. First time using calendar, you'll need to authorize
3. A browser window will open asking to authorize Life OS
4. Grant permissions
5. Token will be saved to `google-calendar-token.json`

### Step 7: Verify Installation

- Try: "What's on my calendar today?"
- I should be able to list your calendar events

---

## Troubleshooting

### GitHub MCP

**Error: "Repository not found"**
- Check token has `repo` scope
- Verify token is not expired
- Ensure token is correctly copied (no extra spaces)

**Error: "Authentication failed"**
- Regenerate token with correct scopes
- Update `claude_desktop_config.json` with new token
- Restart Claude Code

### Filesystem MCP

**Error: "Permission denied"**
- Check file path is correct
- Ensure Claude Code has read/write permissions
- On Windows, use double backslashes `\\` in paths

### Google Calendar MCP

**Error: "Credentials not found"**
- Check `google-calendar-credentials.json` exists
- Verify path in config is correct
- Use absolute path, not relative

**Error: "Authorization failed"**
- Delete `google-calendar-token.json`
- Restart Claude Code
- Re-authorize when prompted

**Error: "API not enabled"**
- Go to Google Cloud Console
- Verify Google Calendar API is enabled
- Wait 1-2 minutes for changes to propagate

---

## Security Best Practices

1. **Never commit tokens/credentials to git**
   - Always add to `.gitignore`
   - Tokens are in `claude_desktop_config.json` (not in Life OS repo)

2. **Use token expiration**
   - GitHub tokens: Set 1-year expiration
   - Rotate tokens annually

3. **Minimal scopes**
   - Only grant permissions needed
   - Review scopes before accepting

4. **Keep credentials local**
   - Don't share `claude_desktop_config.json`
   - Don't screenshot config with tokens visible

---

## Next Steps

Once all MCPs are installed:

1. ✅ Verify each MCP is working
2. ✅ Test GitHub push capability
3. ✅ Test calendar read/write
4. 📅 Proceed with deployment to Render
5. 📅 Start Phase 2B: Calendar integration

---

## Support

If you encounter issues:
- GitHub MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/github
- Filesystem MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- Google Calendar MCP: https://github.com/nspady/google-calendar-mcp
