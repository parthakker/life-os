"""
Agentic Router for Life OS
Routes messages to appropriate tools using Claude AI
"""

import os
import json
import sys
from datetime import datetime, timedelta
import anthropic
from .tools_manifest import get_tool_prompt
from .vector_store import add_to_vector_store
from .rag_query import execute_rag_query
from .db_helper import execute_query, execute_insert


def get_category_id(category_name):
    """Get category ID from database by name (case-insensitive, hierarchical match)"""
    # Try exact match first
    result = execute_query(
        'SELECT id FROM categories WHERE LOWER(name) = LOWER(?)',
        (category_name,),
        fetch='one'
    )

    if result:
        return result['id']

    # If no exact match, try hierarchical lookup
    # E.g., "Wedding - Vendors" should find category "Vendors" with parent "Wedding"
    if ' - ' in category_name:
        parts = category_name.split(' - ')

        # Try to find the child category with the correct parent chain
        # Start from the end (most specific category)
        child_name = parts[-1]

        # If there's a parent specified
        if len(parts) > 1:
            parent_name = parts[-2]  # Immediate parent

            # Find child category with matching parent
            result = execute_query('''
                SELECT c.id
                FROM categories c
                JOIN categories p ON c.parent_id = p.id
                WHERE LOWER(c.name) = LOWER(?)
                AND LOWER(p.name) = LOWER(?)
            ''', (child_name, parent_name), fetch='one')

            if result:
                return result['id']

        # Try just the child name (last part) as fallback
        result = execute_query(
            'SELECT id FROM categories WHERE LOWER(name) = LOWER(?)',
            (child_name,),
            fetch='one'
        )

        if result:
            return result['id']

    # Last resort: partial match (e.g., "Wedding" matches "Wedding - Vendors")
    result = execute_query(
        'SELECT id FROM categories WHERE LOWER(name) LIKE LOWER(?)',
        (f'%{category_name}%',),
        fetch='one'
    )

    return result['id'] if result else None


def get_category_name(category_id):
    """Get category name from database by ID"""
    result = execute_query(
        'SELECT name FROM categories WHERE id = ?',
        (category_id,),
        fetch='one'
    )

    return result['name'] if result else None


def build_category_context():
    """Build category list with descriptions from database"""
    # Query all categories with their hierarchy info
    categories = execute_query(
        'SELECT id, name, description, parent_id FROM categories ORDER BY sort_order, name',
        fetch='all'
    )

    if not categories:
        return "- Tasks: Generic catch-all tasks"

    # Build hierarchical structure
    # Group by parent_id
    top_level = []
    children_map = {}

    for cat in categories:
        if cat['parent_id'] is None:
            top_level.append(cat)
        else:
            parent_id = cat['parent_id']
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(cat)

    # Build the prompt text
    lines = []

    for parent in top_level:
        parent_name = parent['name']
        parent_desc = parent['description'] or ""
        parent_id = parent['id']

        # Check if this category has children
        if parent_id in children_map:
            # Parent with children
            lines.append(f"\n**{parent_name}** (has subcategories - choose specific one):")
            if parent_desc:
                lines.append(f"  ({parent_desc})")
            for child in children_map[parent_id]:
                child_name = child['name']
                child_desc = child['description'] or ""
                lines.append(f"  - {parent_name} - {child_name}: {child_desc}")
        else:
            # Top-level category without children
            lines.append(f"- {parent_name}: {parent_desc}")

    return '\n'.join(lines)


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

    # Build dynamic category context from database
    category_context = build_category_context()

    prompt = f"""You are an intelligent routing assistant for Life OS.

TODAY'S DATE: {today.isoformat()} ({today.strftime('%A, %B %d, %Y')})

User Message: "{message}"

{get_tool_prompt()}

Available categories (with subcategories):
{category_context}

Instructions:
1. Analyze the message and determine which tool to use
2. If add_task or add_note: Extract category and content
   - For categories with subcategories (marked with **), MUST choose a specific subcategory like "Wedding - Vendors"
   - For leaf categories, use the name directly
3. If add_task: Also parse due date if mentioned
4. If ask_question: Extract query details and filters
   - For category filter, you CAN use parent categories like "Wedding" to search all subcategories
   - OR use specific subcategories like "Wedding - Vendors" for narrower searches

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
    "category": "category name or null (can be parent like 'Wedding' or specific like 'Wedding - Vendors')",
    "time_range": "today or week or all",
    "status": "open or completed or all"
  }}
}}

Examples of category usage in ask_question:
- "what are my wedding tasks" → filters: {{"category": "Wedding"}} (searches ALL wedding subcategories)
- "what are my vendor tasks" → filters: {{"category": "Wedding - Vendors"}} (searches only vendors)
- "show me home tasks" → filters: {{"category": "Home"}} (leaf category)

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
    task_id = execute_insert(
        'INSERT INTO tasks (category_id, content, due_date, created_date) VALUES (?, ?, ?, ?)',
        (category_id, content, parsed_due_date, datetime.now().isoformat()),
        return_id=True
    )

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
    note_id = execute_insert(
        'INSERT INTO notes (category_id, content, created_date) VALUES (?, ?, ?)',
        (category_id, content, datetime.now().isoformat()),
        return_id=True
    )

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


def execute_log_sleep(hours, date=None, notes=None):
    """Log sleep hours"""
    # Default to last night if no date specified
    if not date:
        date = (datetime.now() - timedelta(days=1)).date().isoformat()

    # Insert sleep log (PostgreSQL compatible)
    execute_insert(
        'INSERT INTO sleep_logs (date, hours, notes) VALUES (?, ?, ?)',
        (date, hours, notes),
        return_id=False
    )

    return {
        'message': f"💤 Logged {hours} hours of sleep for {date}"
    }


def execute_log_water(cups, date=None):
    """Log water intake"""
    if not date:
        date = datetime.now().date().isoformat()

    timestamp = datetime.now().isoformat()

    # Insert water log entry
    execute_insert(
        'INSERT INTO water_logs (date, cups, timestamp) VALUES (?, ?, ?)',
        (date, cups, timestamp)
    )

    return {
        'message': f"💧 Logged {cups} cup(s) of water for {date}"
    }


def execute_log_exercise(activity_type, duration_minutes, date=None, notes=None):
    """Log exercise activity"""
    if not date:
        date = datetime.now().date().isoformat()

    execute_insert(
        'INSERT INTO exercise_logs (date, activity_type, duration_minutes, notes) VALUES (?, ?, ?, ?)',
        (date, activity_type, duration_minutes, notes)
    )

    return {
        'message': f"🏃 Logged {duration_minutes} min of {activity_type} for {date}"
    }


def execute_log_sauna(duration_minutes, num_visits=1, date=None):
    """Log sauna session"""
    if not date:
        date = datetime.now().date().isoformat()

    execute_insert(
        'INSERT INTO sauna_logs (date, num_visits, duration_minutes) VALUES (?, ?, ?)',
        (date, num_visits, duration_minutes),
        return_id=False
    )

    return {
        'message': f"🧖 Logged sauna session: {duration_minutes} min for {date}"
    }


def execute_log_inbody(weight, smm, pbf, ecw_tbw_ratio, date=None, notes=None):
    """Log InBody measurements"""
    if not date:
        date = datetime.now().date().isoformat()

    execute_insert(
        'INSERT INTO inbody_measurements (date, weight, smm, pbf, ecw_tbw_ratio, notes) VALUES (?, ?, ?, ?, ?, ?)',
        (date, weight, smm, pbf, ecw_tbw_ratio, notes),
        return_id=False
    )

    return {
        'message': f"📊 InBody logged for {date}:\n  Weight: {weight} lbs\n  SMM: {smm} lbs\n  PBF: {pbf}%\n  ECW/TBW: {ecw_tbw_ratio}"
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

        elif result['tool'] == 'log_sleep':
            response = execute_log_sleep(
                result['hours'],
                result.get('date'),
                result.get('notes')
            )
            print(f"\n{response['message']}")

        elif result['tool'] == 'log_water':
            response = execute_log_water(
                result['cups'],
                result.get('date')
            )
            print(f"\n{response['message']}")

        elif result['tool'] == 'log_exercise':
            response = execute_log_exercise(
                result['activity_type'],
                result['duration_minutes'],
                result.get('date'),
                result.get('notes')
            )
            print(f"\n{response['message']}")

        elif result['tool'] == 'log_sauna':
            response = execute_log_sauna(
                result['duration_minutes'],
                result.get('num_visits', 1),
                result.get('date')
            )
            print(f"\n{response['message']}")

        elif result['tool'] == 'log_inbody':
            response = execute_log_inbody(
                result['weight'],
                result['smm'],
                result['pbf'],
                result['ecw_tbw_ratio'],
                result.get('date'),
                result.get('notes')
            )
            print(f"\n{response['message']}")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
