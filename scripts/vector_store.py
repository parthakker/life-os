"""
Custom Vector Store for Life OS RAG
Lightweight implementation using OpenAI Embeddings API + JSON storage
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import numpy as np
from openai import OpenAI

DB_PATH = Path(__file__).parent.parent / 'data.db'
VECTOR_STORE_PATH = Path(__file__).parent.parent / 'vector_store.json'

# OpenAI API configuration
# text-embedding-3-small: High quality, low cost ($0.02/1M tokens)
# Using 384 dimensions to match previous all-MiniLM-L6-v2 model

def get_embedding(text):
    """
    Get embedding from OpenAI API
    Uses text-embedding-3-small with 384 dimensions

    Args:
        text: Text to embed

    Returns:
        List of floats (384 dimensions)
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable not set")

    client = OpenAI(api_key=api_key)

    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
            dimensions=384  # Match old model dimensions for compatibility
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"[Vector Store] Error getting embedding from OpenAI: {e}")
        raise


def vectorize_all_data(force=False):
    """
    Vectorize all tasks and notes in the database
    Args:
        force: If True, re-vectorize even if vector store exists
    """

    if VECTOR_STORE_PATH.exists() and not force:
        print(f"[OK] Vector store already exists at {VECTOR_STORE_PATH}")
        print("[OK] Use force=True to re-vectorize")
        return

    print("[Vector Store] Starting vectorization...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all tasks
    cursor.execute('''
        SELECT t.id, c.name, t.content, t.due_date, t.created_date, t.completed
        FROM tasks t
        JOIN categories c ON t.category_id = c.id
    ''')
    tasks = cursor.fetchall()

    # Get all notes
    cursor.execute('''
        SELECT n.id, c.name, n.content, n.created_date
        FROM notes n
        JOIN categories c ON n.category_id = c.id
    ''')
    notes = cursor.fetchall()

    conn.close()

    # Build vector store
    vector_store = {
        'metadata': {
            'created_at': datetime.now().isoformat(),
            'model': 'text-embedding-3-small',
            'provider': 'openai',
            'dimensions': 384,
            'total_items': len(tasks) + len(notes)
        },
        'items': []
    }

    # Vectorize tasks
    for task_id, category, content, due_date, created, completed in tasks:
        # Create rich text for better embeddings
        embedding_text = f"{category}: {content}"
        if due_date:
            embedding_text += f" (due: {due_date})"

        # Generate embedding via OpenAI API
        embedding = get_embedding(embedding_text)

        vector_store['items'].append({
            'id': f"task_{task_id}",
            'type': 'task',
            'category': category,
            'content': content,
            'due_date': due_date,
            'created_date': created,
            'completed': bool(completed),
            'embedding': embedding
        })

    print(f"[OK] Vectorized {len(tasks)} tasks")

    # Vectorize notes
    for note_id, category, content, created in notes:
        # Create rich text for better embeddings
        embedding_text = f"{category}: {content}"

        # Generate embedding via OpenAI API
        embedding = get_embedding(embedding_text)

        vector_store['items'].append({
            'id': f"note_{note_id}",
            'type': 'note',
            'category': category,
            'content': content,
            'created_date': created,
            'embedding': embedding
        })

    print(f"[OK] Vectorized {len(notes)} notes")

    # Save to JSON file
    with open(VECTOR_STORE_PATH, 'w', encoding='utf-8') as f:
        json.dump(vector_store, f, indent=2)

    print(f"[OK] Vector store saved to {VECTOR_STORE_PATH}")
    print(f"[OK] Total items: {len(vector_store['items'])}")

    # Print file size
    file_size_mb = VECTOR_STORE_PATH.stat().st_size / (1024 * 1024)
    print(f"[OK] File size: {file_size_mb:.2f} MB")


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def search_memory(query, n_results=5, filters=None):
    """
    Search vector store for similar items

    Args:
        query: Natural language query
        n_results: Number of results to return
        filters: Optional dict like {"category": "Betting", "type": "task"}

    Returns:
        List of matching items with similarity scores
    """

    if not VECTOR_STORE_PATH.exists():
        raise Exception("Vector store not found. Run vectorize_all_data() first.")

    # Load vector store
    with open(VECTOR_STORE_PATH, 'r', encoding='utf-8') as f:
        vector_store = json.load(f)

    # Vectorize query via OpenAI API
    print(f"[Search] Vectorizing query: '{query}'")
    query_embedding = get_embedding(query)

    # Calculate similarities for all items
    results = []
    for item in vector_store['items']:
        # Apply filters if provided
        if filters:
            if 'category' in filters and filters['category']:
                if filters['category'].lower() not in item['category'].lower():
                    continue
            if 'type' in filters and filters['type']:
                if item['type'] != filters['type']:
                    continue
            if 'completed' in filters and filters['completed'] is not None:
                if item['type'] == 'task' and item.get('completed') != filters['completed']:
                    continue

        # Calculate similarity
        similarity = cosine_similarity(query_embedding, item['embedding'])

        results.append({
            'item': item,
            'similarity': similarity
        })

    # Sort by similarity (highest first)
    results.sort(key=lambda x: x['similarity'], reverse=True)

    # Return top N results
    top_results = results[:n_results]

    print(f"[Search] Found {len(top_results)} results")
    for i, result in enumerate(top_results):
        print(f"  {i+1}. [{result['item']['category']}] {result['item']['content'][:50]}... (similarity: {result['similarity']:.3f})")

    return top_results


def add_to_vector_store(item_id, item_type, category, content, **kwargs):
    """
    Add a new item to vector store
    Called when new tasks/notes are added to database
    """

    if not VECTOR_STORE_PATH.exists():
        print("[Warning] Vector store not found. Run vectorize_all_data() first.")
        return

    # Load vector store
    with open(VECTOR_STORE_PATH, 'r', encoding='utf-8') as f:
        vector_store = json.load(f)

    # Create embedding text
    embedding_text = f"{category}: {content}"
    if item_type == 'task' and kwargs.get('due_date'):
        embedding_text += f" (due: {kwargs['due_date']})"

    # Generate embedding via OpenAI API
    embedding = get_embedding(embedding_text)

    # Create item
    new_item = {
        'id': f"{item_type}_{item_id}",
        'type': item_type,
        'category': category,
        'content': content,
        'created_date': datetime.now().isoformat(),
        'embedding': embedding
    }

    # Add task-specific fields
    if item_type == 'task':
        new_item['due_date'] = kwargs.get('due_date')
        new_item['completed'] = kwargs.get('completed', False)

    # Add to vector store
    vector_store['items'].append(new_item)
    vector_store['metadata']['total_items'] = len(vector_store['items'])

    # Save
    with open(VECTOR_STORE_PATH, 'w', encoding='utf-8') as f:
        json.dump(vector_store, f, indent=2)

    print(f"[Vector Store] Added {item_type}_{item_id} to vector store")


def main():
    """Command-line interface for vector store"""
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python vector_store.py vectorize         - Vectorize all data")
        print("  python vector_store.py search '<query>'  - Search vector store")
        print('Example: python vector_store.py search "what are my bets"')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'vectorize':
        force = '--force' in sys.argv
        vectorize_all_data(force=force)

    elif command == 'search':
        if len(sys.argv) < 3:
            print("Error: Please provide a search query")
            sys.exit(1)

        query = ' '.join(sys.argv[2:])
        results = search_memory(query, n_results=10)

        print(f"\n{'='*60}")
        print(f"Search Results for: '{query}'")
        print(f"{'='*60}\n")

        for i, result in enumerate(results):
            item = result['item']
            print(f"{i+1}. [{item['category']}] ({item['type'].upper()})")
            print(f"   Content: {item['content']}")
            if item['type'] == 'task' and item.get('due_date'):
                print(f"   Due: {item['due_date']}")
            print(f"   Similarity: {result['similarity']:.3f}")
            print()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
