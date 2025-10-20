"""
Agentic Router for Life OS
Routes messages to appropriate tools using Claude AI
"""

import os
import json
import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import anthropic
from tools_manifest import get_tool_prompt
from vector_store import add_to_vector_store
from rag_query import execute_rag_query

DB_PATH = Path(__file__).parent.parent / 'data.db'


def get_category_id(category_name):
    """Get category ID from database by name (case-insensitive, partial match)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Try exact match first
    cursor.execute('SELECT id FROM categories WHERE LOWER(name) = LOWER(?)', (category_name,))
    result = cursor.fetchone()

    if not result:
        # Try partial match (e.g., "Wedding" matches "Wedding - Vendors")
        cursor.execute('SELECT id FROM categories WHERE LOWER(name) LIKE LOWER(?)', (f'%{category_name}%',))
        result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def get_category_name(category_id):
    """Get category name from database by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM categories WHERE id = ?', (category_id,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def parse_due_date(date_str):
    """Parse natural language due dates to ISO format"""
    if not date_str or date_str.lower() in ['none', 'n/a', 'tbd', 'null']:
        return None

    date_str_lower = date_str.lower().strip()
    today = datetime.now().date()

    # Common patterns
    if date_str_lower == 'today':
        return today.isoformat()
    elif date_str_lower == 'tomorrow':
        return (today + timedelta(days=1)).isoformat()
    elif 'next week' in date_str_lower or 'end of week' in date_str_lower:
        # Next Friday
        days_ahead = 4 - today.weekday()  # Friday is 4
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days=days_ahead)).isoformat()
    elif 'next month' in date_str_lower:
        next_month = today.replace(day=1) + timedelta(days=32)
        return next_month.replace(day=1).isoformat()
    elif date_str_lower == 'asap':
        return 'ASAP'
    elif date_str_lower == 'ongoing':
        return 'Ongoing'
    else:
        # Return as-is if it's a specific date
        return date_str


def route_message(message):
    """
    Route message to appropriate tool using Claude AI
    Returns: {
        'tool': 'add_task' | 'add_note' | 'ask_question',
        'parameters': {...}
    }
    """

    # Get API key from environment
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise Exception("ANTHROPIC_API_KEY environment variable not set")

    # Build routing prompt
    today = datetime.now().date()

    prompt = f"""You are an intelligent routing assistant for Life OS.

TODAY'S DATE: {today.isoformat()} ({today.strftime('%A, %B %d, %Y')})

User Message: "{message}"

{get_tool_prompt()}

Available categories (with subcategories):
- Buddy: Dog care, health, vet appointments
- Home: House maintenance, HOA, Brad rent, cleaning, furniture
- Bills: Bill payments and tracking (reference only)
- Personal Projects: Life OS, Personal Assistant, NFL for Indians, Podcast, Claude Code
- Betting: Sports betting, Beat Writer Scraper, betting tracking, active bets
- Events: Upcoming events, birthdays, important dates
- Social: Friends visiting, social coordination
- Tasks: Generic catch-all tasks

**Family** (has subcategories - choose specific group):
  - Family - Immediate Family: Mom, Dad, Mansi (sister) - bank, passwords, insurance
  - Family - USA Family: Jay, Aayushi, Surekha Aunty, Suraj - job help, design discussion
  - Family - India Family: Dadi, Dada, Nani - weekly follow up

**Hobbies** (has subcategories - choose specific hobby):
  - Hobbies - GYM: Gym workouts, fitness
  - Hobbies - BJJ: Brazilian Jiu-Jitsu
  - Hobbies - Video Games: Gaming, Madden, etc.
  - Hobbies - Television/Movies: TV shows, movies
  - Hobbies - FOOTBALL: NFL, fantasy football
  - Hobbies - Photography: Photos, camera
  - Hobbies - Guitar: Music, guitar playing
  - Hobbies - Yoga: Yoga practice
  - Hobbies - Finance: Financial topics, investing
  - Hobbies - Politics: Political interests
  - Hobbies - AI: AI topics, learning
  - Hobbies - Extra-Curricular: Other hobbies
  - Hobbies - Cricket: Cricket interests

**Wedding** (has subcategories - choose specific area):
  - Wedding - Vendors: Grove, Pasha, photobooth, invitations
  - Wedding - Things Needed from Family: Guest list, family coordination
  - Wedding - Bachelor Party: Planning, Suns game, ATV, coordination
  - Wedding - Dances: Dance planning
  - Wedding - Speeches: Speech planning
  - Wedding - Décor: Clothes, outfits, décor
  - Wedding - Engagement Pooja: Engagement event planning

**Princeton AI Partners** (has subcategories - choose specific project/client):
  - Princeton AI - Princeton AI Partners - Princeton-ai.com: Website tasks
  - Princeton AI - Princeton AI Partners - UpLevel Resume: Client project
  - Princeton AI - Princeton AI Partners - Hamilton Deli: Client ($50/mo), Akshay
  - Princeton AI - Princeton AI Partners - Overview: General business, Jasjit, Liji, SELL
  - Princeton AI - Princeton AI Partners - Generic Tasks: N8N, Mercury, Stripe monitoring

**Notes** (has subcategories):
  - Notes - General: General notes, reminders
  - Notes - Quotes: Memorable quotes

**Preeti** (has subcategories - fiancée related):
  - Preeti - Tasks: Things to do with/for Preeti
  - Preeti - Notes: Date ideas, thoughts about Preeti
  - Preeti - Important Events: Events related to Preeti

Instructions:
1. Analyze the message and determine which tool to use
2. If add_task or add_note: Extract category and content
3. If add_task: Also parse due date if mentioned
4. If ask_question: Extract query details and filters

Output Format Examples:

For add_task:
{{
  "tool": "add_task",
  "category": "exact category name",
  "content": "cleaned task description",
  "due_date": "YYYY-MM-DD or ASAP or null"
}}

For add_note:
{{
  "tool": "add_note",
  "category": "exact category name",
  "content": "note content"
}}

For ask_question:
{{
  "tool": "ask_question",
  "query": "user's question",
  "query_type": "tasks or notes or all",
  "filters": {{
    "category": "category name or null",
    "time_range": "today or week or all",
    "status": "open or completed or all"
  }}
}}

Return ONLY valid JSON, nothing else:
"""

    try:
        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=api_key)

        # Call Claude AI API using Haiku (cheap and fast)
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",  # Claude 3.5 Haiku - fastest and cheapest
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Get response text
        response_text = response.content[0].text.strip()

        # Extract JSON from response (in case there's extra text)
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1

        if json_start == -1 or json_end == 0:
            raise Exception(f"No JSON found in response: {response_text}")

        json_str = response_text[json_start:json_end]
        data = json.loads(json_str)

        return data

    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON from Claude AI: {e}")
    except Exception as e:
        raise Exception(f"Routing error: {e}")


def execute_add_task(category_name, content, due_date=None):
    """
    Execute add_task tool
    Returns: task_id and confirmation message
    """
    # Get category ID
    category_id = get_category_id(category_name)
    if not category_id:
        raise Exception(f"Unknown category: {category_name}")

    # Parse due date
    parsed_due_date = parse_due_date(due_date)

    # Add to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tasks (category_id, content, due_date, created_date)
        VALUES (?, ?, ?, ?)
    ''', (category_id, content, parsed_due_date, datetime.now().isoformat()))

    task_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Get actual category name from DB
    actual_category = get_category_name(category_id)

    # Auto-vectorize for RAG (Phase 2)
    try:
        add_to_vector_store(
            item_id=task_id,
            item_type='task',
            category=actual_category,
            content=content,
            due_date=parsed_due_date,
            completed=False
        )
    except Exception as e:
        print(f"[Warning] Failed to vectorize task {task_id}: {e}")

    return {
        'id': task_id,
        'category': actual_category,
        'content': content,
        'due_date': parsed_due_date,
        'message': f"✓ Task added to {actual_category}\nContent: {content}\nDue: {parsed_due_date or 'No due date'}\nID: {task_id}"
    }


def execute_add_note(category_name, content):
    """
    Execute add_note tool
    Returns: note_id and confirmation message
    """
    # Get category ID
    category_id = get_category_id(category_name)
    if not category_id:
        raise Exception(f"Unknown category: {category_name}")

    # Add to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO notes (category_id, content, created_date)
        VALUES (?, ?, ?)
    ''', (category_id, content, datetime.now().isoformat()))

    note_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Get actual category name from DB
    actual_category = get_category_name(category_id)

    # Auto-vectorize for RAG (Phase 2)
    try:
        add_to_vector_store(
            item_id=note_id,
            item_type='note',
            category=actual_category,
            content=content
        )
    except Exception as e:
        print(f"[Warning] Failed to vectorize note {note_id}: {e}")

    return {
        'id': note_id,
        'category': actual_category,
        'content': content,
        'message': f"✓ Note saved to {actual_category}\nContent: {content}\nID: {note_id}"
    }


def execute_ask_question(query, query_type='all', filters=None):
    """
    Execute ask_question tool using RAG (Phase 2)
    Returns simple formatted list results
    """
    try:
        # Use RAG to answer the question
        answer = execute_rag_query(query, query_type, filters)

        return {
            'query': query,
            'message': answer
        }
    except Exception as e:
        return {
            'query': query,
            'message': f"💭 Error answering question: {str(e)}\n\nPlease try rephrasing your question."
        }


def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python router.py <message>")
        print('Example: python router.py "buy groceries tomorrow"')
        sys.exit(1)

    message = ' '.join(sys.argv[1:])

    try:
        print(f"Routing: {message}")

        # Route to appropriate tool
        result = route_message(message)

        print(f"\n[OK] Tool selected: {result['tool']}")
        print(f"[OK] Parameters: {json.dumps(result, indent=2)}")

        # Execute tool
        if result['tool'] == 'add_task':
            response = execute_add_task(
                result['category'],
                result['content'],
                result.get('due_date')
            )
            print(f"\n{response['message']}")

        elif result['tool'] == 'add_note':
            response = execute_add_note(
                result['category'],
                result['content']
            )
            print(f"\n{response['message']}")

        elif result['tool'] == 'ask_question':
            response = execute_ask_question(
                result['query'],
                result.get('query_type', 'all'),
                result.get('filters')
            )
            print(f"\n{response['message']}")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
