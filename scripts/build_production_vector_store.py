"""
Build vector store from production PostgreSQL database
Run this once to enable RAG search on production
"""

import os
import json
from datetime import datetime
from pathlib import Path
import psycopg2
import psycopg2.extras
from openai import OpenAI

DATABASE_URL = os.getenv('DATABASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VECTOR_STORE_PATH = Path(__file__).parent.parent / 'vector_store.json'

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL not set")
    exit(1)

if not OPENAI_API_KEY:
    print("[ERROR] OPENAI_API_KEY not set")
    exit(1)

print("=" * 70)
print("BUILDING PRODUCTION VECTOR STORE")
print("=" * 70)

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Get all tasks with full category hierarchy
print("\n[1/4] Fetching tasks from PostgreSQL...")
cursor.execute('''
    SELECT
        t.id,
        c.name as category_name,
        p.name as parent_name,
        t.content,
        t.due_date,
        t.created_date,
        t.completed
    FROM tasks t
    JOIN categories c ON t.category_id = c.id
    LEFT JOIN categories p ON c.parent_id = p.id
    ORDER BY t.created_date DESC
''')
tasks = cursor.fetchall()
print(f"  Found {len(tasks)} tasks")

# Get all notes with full category hierarchy
print("\n[2/4] Fetching notes from PostgreSQL...")
cursor.execute('''
    SELECT
        n.id,
        c.name as category_name,
        p.name as parent_name,
        n.content,
        n.created_date
    FROM notes n
    JOIN categories c ON n.category_id = c.id
    LEFT JOIN categories p ON c.parent_id = p.id
    ORDER BY n.created_date DESC
''')
notes = cursor.fetchall()
print(f"  Found {len(notes)} notes")

conn.close()

# Build vector store
print("\n[3/4] Vectorizing with OpenAI embeddings...")
client = OpenAI(api_key=OPENAI_API_KEY)

vector_store = {
    'metadata': {
        'created_at': datetime.now().isoformat(),
        'model': 'text-embedding-3-small',
        'provider': 'openai',
        'dimensions': 384,
        'total_items': len(tasks) + len(notes),
        'database': 'PostgreSQL (production)'
    },
    'items': []
}

# Vectorize tasks
vectorized = 0
for task in tasks:
    task_id = task['id']
    category_name = task['category_name']
    parent_name = task['parent_name']
    content = task['content']
    due_date = task['due_date']
    created = task['created_date']
    completed = task['completed']

    # Build full category path (e.g., "Wedding - Vendors")
    if parent_name:
        full_category = f"{parent_name} - {category_name}"
    else:
        full_category = category_name

    # Create rich text for better embeddings
    embedding_text = f"{full_category}: {content}"
    if due_date:
        embedding_text += f" (due: {due_date})"

    try:
        # Get embedding from OpenAI
        response = client.embeddings.create(
            input=embedding_text,
            model="text-embedding-3-small",
            dimensions=384
        )

        embedding = response.data[0].embedding

        # Store in vector store
        vector_store['items'].append({
            'id': task_id,
            'type': 'task',
            'category': full_category,
            'content': content,
            'due_date': due_date,
            'completed': completed,
            'created_date': created,
            'embedding_text': embedding_text,
            'embedding': embedding
        })

        vectorized += 1
        if vectorized % 10 == 0:
            print(f"  Vectorized {vectorized}/{len(tasks)} tasks...")

    except Exception as e:
        print(f"  [WARNING] Failed to vectorize task {task_id}: {str(e)}")

print(f"  [OK] Vectorized {vectorized} tasks")

# Vectorize notes
note_vectorized = 0
for note in notes:
    note_id = note['id']
    category_name = note['category_name']
    parent_name = note['parent_name']
    content = note['content']
    created = note['created_date']

    # Build full category path (e.g., "Notes - General")
    if parent_name:
        full_category = f"{parent_name} - {category_name}"
    else:
        full_category = category_name

    # Create rich text for better embeddings
    embedding_text = f"{full_category}: {content}"

    try:
        # Get embedding from OpenAI
        response = client.embeddings.create(
            input=embedding_text,
            model="text-embedding-3-small",
            dimensions=384
        )

        embedding = response.data[0].embedding

        # Store in vector store
        vector_store['items'].append({
            'id': note_id,
            'type': 'note',
            'category': full_category,
            'content': content,
            'created_date': created,
            'embedding_text': embedding_text,
            'embedding': embedding
        })

        note_vectorized += 1
        if note_vectorized % 10 == 0:
            print(f"  Vectorized {note_vectorized}/{len(notes)} notes...")

    except Exception as e:
        print(f"  [WARNING] Failed to vectorize note {note_id}: {str(e)}")

print(f"  [OK] Vectorized {note_vectorized} notes")

# Save vector store
print("\n[4/4] Saving vector store...")
with open(VECTOR_STORE_PATH, 'w', encoding='utf-8') as f:
    json.dump(vector_store, f, indent=2)

print(f"  [OK] Saved to {VECTOR_STORE_PATH}")
print(f"  [OK] Size: {VECTOR_STORE_PATH.stat().st_size // 1024} KB")

print("\n" + "=" * 70)
print("VECTOR STORE BUILD COMPLETE!")
print("=" * 70)
print(f"\nTotal items: {vectorized + note_vectorized}")
print(f"  Tasks: {vectorized}")
print(f"  Notes: {note_vectorized}")
print("\nThe bot can now perform RAG searches on production data!")
print("\nNOTE: Upload this file to production via:")
print("  1. Commit vector_store.json to git (if small enough)")
print("  2. Or run this script directly on Render")
