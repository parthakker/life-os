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
    },

    "log_sleep": {
        "name": "log_sleep",
        "description": "Log sleep hours for a specific date",
        "parameters": {
            "hours": "float - hours of sleep (e.g., 7.5)",
            "date": "string - YYYY-MM-DD format, defaults to last night if not specified",
            "notes": "string - optional notes about sleep quality"
        },
        "examples": [
            "I slept 8 hours last night",
            "slept 7.5 hours",
            "got 6 hours of sleep yesterday"
        ]
    },

    "log_water": {
        "name": "log_water",
        "description": "Log water intake in cups",
        "parameters": {
            "cups": "integer - number of cups (e.g., 1, 2)",
            "date": "string - YYYY-MM-DD format, defaults to today"
        },
        "examples": [
            "2 cups of water",
            "drank 1 cup",
            "had 3 cups of water today"
        ]
    },

    "log_exercise": {
        "name": "log_exercise",
        "description": "Log exercise activity with duration",
        "parameters": {
            "activity_type": "string - type of activity (e.g., Gym, Pickleball, BJJ, Yoga, Running)",
            "duration_minutes": "integer - duration in minutes",
            "date": "string - YYYY-MM-DD format, defaults to today",
            "notes": "string - optional notes"
        },
        "examples": [
            "1 hour of pickleball",
            "played pickleball for 60 minutes",
            "gym session 45 minutes",
            "30 min run this morning"
        ]
    },

    "log_sauna": {
        "name": "log_sauna",
        "description": "Log sauna session",
        "parameters": {
            "duration_minutes": "integer - duration in minutes",
            "num_visits": "integer - number of visits/sessions (default: 1)",
            "date": "string - YYYY-MM-DD format, defaults to today"
        },
        "examples": [
            "20 minutes in sauna",
            "sauna for 30 min",
            "did 2 sauna sessions 15 minutes each"
        ]
    },

    "log_inbody": {
        "name": "log_inbody",
        "description": "Log InBody scan measurements",
        "parameters": {
            "weight": "float - weight in lbs",
            "smm": "float - skeletal muscle mass in lbs",
            "pbf": "float - percent body fat",
            "ecw_tbw_ratio": "float - ECW/TBW ratio",
            "date": "string - YYYY-MM-DD format, defaults to today",
            "notes": "string - optional notes"
        },
        "examples": [
            "InBody: weight 174, SMM 84, PBF 15.2, ECW/TBW 0.385",
            "inbody scan results: 172 lbs, smm 83.5, pbf 14.8%, ecw 0.39"
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

4. **log_sleep**: Log sleep hours
   - Use when: Message mentions sleep duration
   - Output: {{"tool": "log_sleep", "hours": 8.0, "date": "...", "notes": "..."}}

5. **log_water**: Log water intake
   - Use when: Message mentions drinking water
   - Output: {{"tool": "log_water", "cups": 2, "date": "..."}}

6. **log_exercise**: Log exercise/workout
   - Use when: Message mentions physical activity
   - Output: {{"tool": "log_exercise", "activity_type": "...", "duration_minutes": 60, "date": "...", "notes": "..."}}

7. **log_sauna**: Log sauna session
   - Use when: Message mentions sauna
   - Output: {{"tool": "log_sauna", "duration_minutes": 20, "num_visits": 1, "date": "..."}}

8. **log_inbody**: Log InBody scan results
   - Use when: Message contains InBody measurements (weight, SMM, PBF, ECW/TBW)
   - Output: {{"tool": "log_inbody", "weight": 174.0, "smm": 84.0, "pbf": 15.2, "ecw_tbw_ratio": 0.385, "date": "...", "notes": "..."}}

Examples:
- "buy groceries tomorrow" → add_task
- "i love the eagles" → add_note
- "what are my open home tasks" → ask_question
- "I slept 8 hours last night" → log_sleep
- "2 cups of water" → log_water
- "played pickleball for 60 minutes" → log_exercise
- "20 minutes in sauna" → log_sauna
"""
