"""
RAG Query Execution for Life OS
Uses vector search + Claude AI to answer questions about your data

Phase 2 Integration - Ready for activation
"""

import os
from datetime import datetime
import anthropic
from vector_store import search_memory


def execute_rag_query(user_query, query_type='all', filters=None):
    """
    Answer user question using RAG pipeline
    Returns simple formatted list (Phase 2A)

    Args:
        user_query: Natural language question
        query_type: 'tasks', 'notes', or 'all'
        filters: Optional dict with category, time_range, status

    Returns:
        Formatted list of results
    """

    # 1. Search memory for relevant context
    print(f"[RAG] Searching for: {user_query}")

    # Apply filters
    search_filters = {}
    if filters:
        if filters.get('category'):
            search_filters['category'] = filters['category']
        if filters.get('status') == 'open':
            search_filters['completed'] = False
        elif filters.get('status') == 'completed':
            search_filters['completed'] = True
        if query_type != 'all':
            search_filters['type'] = query_type.rstrip('s')  # 'tasks' -> 'task'

    # Get relevant items from vector store
    results = search_memory(user_query, n_results=10, filters=search_filters)

    if not results:
        return "💭 No results found in your Life OS database."

    # 2. Format results as simple list
    formatted_lines = []
    task_count = 0
    note_count = 0

    for result in results:
        item = result['item']
        item_type = item['type']
        category = item['category']
        content = item['content']

        if item_type == 'task':
            task_count += 1
            due = item.get('due_date', 'No due date')
            status_icon = "✓" if item.get('completed') else "⏳"
            formatted_lines.append(f"{status_icon} [{category}] {content}")
            if due and due != 'No due date':
                formatted_lines.append(f"   Due: {due}")
            formatted_lines.append("")  # Empty line for spacing
        else:
            note_count += 1
            formatted_lines.append(f"📝 [{category}] {content}")
            formatted_lines.append("")  # Empty line for spacing

    # Build header
    result_type = []
    if task_count > 0:
        result_type.append(f"{task_count} task{'s' if task_count != 1 else ''}")
    if note_count > 0:
        result_type.append(f"{note_count} note{'s' if note_count != 1 else ''}")

    header = f"💭 Found {' and '.join(result_type)}:\n\n"

    return header + "\n".join(formatted_lines).strip()


def main():
    """Command-line interface for RAG queries"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python rag_query.py '<question>'")
        print('Example: python rag_query.py "what are my open home tasks"')
        sys.exit(1)

    query = ' '.join(sys.argv[1:])

    print(f"\nQuestion: {query}\n")
    answer = execute_rag_query(query)
    print(f"Answer: {answer}\n")


if __name__ == '__main__':
    main()
