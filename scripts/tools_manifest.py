"""
Tool Manifest for Life OS Agentic Router
Defines available tools and their schemas
"""

TOOLS = {
    "add_task": {
        "name": "add_task",
        "description": "Add a new actionable item with optional due date",
        "parameters": {
            "category": "string - exact category name from available categories",
            "content": "string - cleaned task description",
            "due_date": "string - YYYY-MM-DD format, or ASAP, Ongoing, TBD, or null"
        },
        "examples": [
            "buy groceries for Preeti tomorrow",
            "call Hamilton Deli next week",
            "go to gym tomorrow morning",
            "dishes tomorrow morning",
            "throw away bad mail"
        ]
    },

    "add_note": {
        "name": "add_note",
        "description": "Store information, observations, or quotes (non-actionable)",
        "parameters": {
            "category": "string - exact category name from available categories",
            "content": "string - note content"
        },
        "examples": [
            "i love the eagles",
            "sam is a great yoga teacher 8/10",
            "The only way to do great work is to love what you do - Steve Jobs",
            "pumpkin carving date idea",
            "Packers looking good"
        ]
    },

    "ask_question": {
        "name": "ask_question",
        "description": "Query existing data or get insights from memory",
        "parameters": {
            "query": "string - the user's question",
            "query_type": "string - tasks|notes|all",
            "filters": {
                "category": "string - category name or null",
                "time_range": "string - today|week|month|all",
                "status": "string - open|completed|all (for tasks)"
            }
        },
        "examples": [
            "what are my bets for today",
            "what are my open home tasks",
            "show me my gym notes from last week",
            "what was my bench press looking like last week",
            "how much money did I win betting on the eagles last week"
        ]
    }
}

def get_tool_prompt():
    """
    Generate the tool selection prompt for Claude
    """
    return """
Available Tools:

1. **add_task**: For actionable items (things to do)
   - Use when: Message describes something that needs to be done
   - Output: {{"tool": "add_task", "category": "...", "content": "...", "due_date": "..."}}

2. **add_note**: For information storage (observations, facts, quotes)
   - Use when: Message shares information, opinions, or memories
   - Output: {{"tool": "add_note", "category": "...", "content": "..."}}

3. **ask_question**: For querying existing data
   - Use when: Message asks about past information ("what are...", "show me...", "how much...")
   - Output: {{"tool": "ask_question", "query": "...", "query_type": "...", "filters": {{...}}}}

Examples:
- "buy groceries tomorrow" → add_task
- "i love the eagles" → add_note
- "what are my open home tasks" → ask_question
"""
