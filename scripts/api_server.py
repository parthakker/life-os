"""
Flask REST API Server for Life OS Dashboard
Provides CRUD endpoints for tasks, notes, categories, and semantic search
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent))

from db_helper import execute_query, execute_insert, get_db_type
from vector_store import add_to_vector_store, search_memory
from rag_query import execute_rag_query

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend development

# ==================== UTILITY FUNCTIONS ====================

def row_to_dict(row):
    """Convert database row to dictionary"""
    if row is None:
        return None
    return dict(row)

def rows_to_list(rows):
    """Convert list of database rows to list of dictionaries"""
    if rows is None:
        return []
    return [dict(row) for row in rows]

# ==================== CATEGORIES ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        rows = execute_query(
            "SELECT * FROM categories ORDER BY sort_order, name",
            fetch='all'
        )
        categories = rows_to_list(rows)
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== TASKS ====================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filters"""
    try:
        # Get query parameters
        category_id = request.args.get('category_id')
        completed = request.args.get('completed')

        # Build query
        query = """
            SELECT t.*, c.name as category_name
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        """
        params = []

        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)

        if completed is not None:
            query += " AND t.completed = ?"
            params.append(completed == 'true')

        query += " ORDER BY t.completed ASC, t.due_date ASC, t.created_date DESC"

        rows = execute_query(query, tuple(params) if params else None, fetch='all')
        tasks = rows_to_list(rows)
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID"""
    try:
        row = execute_query(
            """
            SELECT t.*, c.name as category_name
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.id = ?
            """,
            (task_id,),
            fetch='one'
        )
        task = row_to_dict(row)
        if task:
            return jsonify(task), 200
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400

        # Insert task
        task_id = execute_insert(
            """
            INSERT INTO tasks (category_id, content, due_date, completed)
            VALUES (?, ?, ?, ?)
            """,
            (
                data.get('category_id'),
                data['content'],
                data.get('due_date'),
                data.get('completed', False)
            ),
            return_id=True
        )

        # Get category name for vectorization
        category_row = execute_query(
            "SELECT name FROM categories WHERE id = ?",
            (data.get('category_id'),),
            fetch='one'
        ) if data.get('category_id') else None

        category_name = category_row['name'] if category_row else 'Uncategorized'

        # Add to vector store
        add_to_vector_store(
            item_id=task_id,
            item_type='task',
            category=category_name,
            content=data['content'],
            due_date=data.get('due_date')
        )

        # Return created task
        row = execute_query(
            """
            SELECT t.*, c.name as category_name
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.id = ?
            """,
            (task_id,),
            fetch='one'
        )
        task = row_to_dict(row)
        return jsonify(task), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    try:
        data = request.get_json()

        # Build update query dynamically
        updates = []
        params = []

        if 'content' in data:
            updates.append("content = ?")
            params.append(data['content'])

        if 'category_id' in data:
            updates.append("category_id = ?")
            params.append(data['category_id'])

        if 'due_date' in data:
            updates.append("due_date = ?")
            params.append(data['due_date'])

        if 'completed' in data:
            updates.append("completed = ?")
            params.append(data['completed'])

        if not updates:
            return jsonify({'error': 'No fields to update'}), 400

        params.append(task_id)

        execute_query(
            f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
            tuple(params)
        )

        # Update vector store if content or category changed
        if 'content' in data or 'category_id' in data:
            # Get full task data for vectorization
            row = execute_query(
                """
                SELECT t.*, c.name as category_name
                FROM tasks t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.id = ?
                """,
                (task_id,),
                fetch='one'
            )
            task = row_to_dict(row)

            if task:
                add_to_vector_store(
                    item_id=task_id,
                    item_type='task',
                    category=task['category_name'] or 'Uncategorized',
                    content=task['content'],
                    due_date=task.get('due_date')
                )

        # Return updated task
        row = execute_query(
            """
            SELECT t.*, c.name as category_name
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.id = ?
            """,
            (task_id,),
            fetch='one'
        )
        task = row_to_dict(row)
        return jsonify(task), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>/complete', methods=['PATCH'])
def toggle_task_completion(task_id):
    """Toggle task completion status"""
    try:
        # Get current status
        row = execute_query(
            "SELECT completed FROM tasks WHERE id = ?",
            (task_id,),
            fetch='one'
        )

        if not row:
            return jsonify({'error': 'Task not found'}), 404

        # Toggle status
        new_status = not row['completed']

        execute_query(
            "UPDATE tasks SET completed = ? WHERE id = ?",
            (new_status, task_id)
        )

        # Return updated task
        row = execute_query(
            """
            SELECT t.*, c.name as category_name
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.id = ?
            """,
            (task_id,),
            fetch='one'
        )
        task = row_to_dict(row)
        return jsonify(task), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        # Check if task exists
        row = execute_query(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,),
            fetch='one'
        )

        if not row:
            return jsonify({'error': 'Task not found'}), 404

        # Delete from database
        execute_query(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        # Note: We don't remove from vector store as it's rebuilt periodically
        # Future enhancement: Add remove_from_vector_store function

        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== NOTES ====================

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes with optional filters"""
    try:
        category_id = request.args.get('category_id')

        query = """
            SELECT n.*, c.name as category_name
            FROM notes n
            LEFT JOIN categories c ON n.category_id = c.id
            WHERE 1=1
        """
        params = []

        if category_id:
            query += " AND n.category_id = ?"
            params.append(category_id)

        query += " ORDER BY n.created_date DESC"

        rows = execute_query(query, tuple(params) if params else None, fetch='all')
        notes = rows_to_list(rows)
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a single note by ID"""
    try:
        row = execute_query(
            """
            SELECT n.*, c.name as category_name
            FROM notes n
            LEFT JOIN categories c ON n.category_id = c.id
            WHERE n.id = ?
            """,
            (note_id,),
            fetch='one'
        )
        note = row_to_dict(row)
        if note:
            return jsonify(note), 200
        else:
            return jsonify({'error': 'Note not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.get_json()

        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400

        # Insert note
        note_id = execute_insert(
            """
            INSERT INTO notes (category_id, content)
            VALUES (?, ?)
            """,
            (data.get('category_id'), data['content']),
            return_id=True
        )

        # Get category name for vectorization
        category_row = execute_query(
            "SELECT name FROM categories WHERE id = ?",
            (data.get('category_id'),),
            fetch='one'
        ) if data.get('category_id') else None

        category_name = category_row['name'] if category_row else 'Uncategorized'

        # Add to vector store
        add_to_vector_store(
            item_id=note_id,
            item_type='note',
            category=category_name,
            content=data['content']
        )

        # Return created note
        row = execute_query(
            """
            SELECT n.*, c.name as category_name
            FROM notes n
            LEFT JOIN categories c ON n.category_id = c.id
            WHERE n.id = ?
            """,
            (note_id,),
            fetch='one'
        )
        note = row_to_dict(row)
        return jsonify(note), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update an existing note"""
    try:
        data = request.get_json()

        updates = []
        params = []

        if 'content' in data:
            updates.append("content = ?")
            params.append(data['content'])

        if 'category_id' in data:
            updates.append("category_id = ?")
            params.append(data['category_id'])

        if not updates:
            return jsonify({'error': 'No fields to update'}), 400

        params.append(note_id)

        execute_query(
            f"UPDATE notes SET {', '.join(updates)} WHERE id = ?",
            tuple(params)
        )

        # Update vector store if content or category changed
        if 'content' in data or 'category_id' in data:
            row = execute_query(
                """
                SELECT n.*, c.name as category_name
                FROM notes n
                LEFT JOIN categories c ON n.category_id = c.id
                WHERE n.id = ?
                """,
                (note_id,),
                fetch='one'
            )
            note = row_to_dict(row)

            if note:
                add_to_vector_store(
                    item_id=note_id,
                    item_type='note',
                    category=note['category_name'] or 'Uncategorized',
                    content=note['content']
                )

        # Return updated note
        row = execute_query(
            """
            SELECT n.*, c.name as category_name
            FROM notes n
            LEFT JOIN categories c ON n.category_id = c.id
            WHERE n.id = ?
            """,
            (note_id,),
            fetch='one'
        )
        note = row_to_dict(row)
        return jsonify(note), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    try:
        row = execute_query(
            "SELECT id FROM notes WHERE id = ?",
            (note_id,),
            fetch='one'
        )

        if not row:
            return jsonify({'error': 'Note not found'}), 404

        execute_query(
            "DELETE FROM notes WHERE id = ?",
            (note_id,)
        )

        return jsonify({'message': 'Note deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SEARCH ====================

@app.route('/api/search', methods=['GET'])
def semantic_search():
    """Perform semantic search using RAG"""
    try:
        query = request.args.get('q')

        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400

        # Use existing RAG query function
        result = execute_rag_query(query)

        return jsonify({
            'query': query,
            'answer': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': get_db_type(),
        'timestamp': datetime.now().isoformat()
    }), 200

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("🚀 Life OS API Server starting...")
    print(f"📊 Database: {get_db_type()}")
    print("🌐 CORS enabled for frontend development")
    print("📡 Server running on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET    /api/health")
    print("  GET    /api/categories")
    print("  GET    /api/tasks")
    print("  GET    /api/tasks/<id>")
    print("  POST   /api/tasks")
    print("  PUT    /api/tasks/<id>")
    print("  PATCH  /api/tasks/<id>/complete")
    print("  DELETE /api/tasks/<id>")
    print("  GET    /api/notes")
    print("  GET    /api/notes/<id>")
    print("  POST   /api/notes")
    print("  PUT    /api/notes/<id>")
    print("  DELETE /api/notes/<id>")
    print("  GET    /api/search?q=<query>")

    app.run(debug=True, host='0.0.0.0', port=5000)
