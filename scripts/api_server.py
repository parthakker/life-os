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

def get_immediate_child_ids(category_id):
    """Get IDs of immediate children of a category"""
    children = execute_query(
        "SELECT id FROM categories WHERE parent_id = ?",
        (category_id,),
        fetch='all'
    )
    return [child['id'] for child in (children or [])]

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

@app.route('/api/categories/tree', methods=['GET'])
def get_categories_tree():
    """Get categories as hierarchical tree structure"""
    try:
        # Get all categories
        rows = execute_query(
            "SELECT id, name, description, parent_id, sort_order FROM categories ORDER BY sort_order, name",
            fetch='all'
        )
        categories = rows_to_list(rows)

        # Build tree structure
        category_map = {cat['id']: {**cat, 'children': []} for cat in categories}
        tree = []

        for cat in categories:
            if cat['parent_id'] is None:
                # Top-level category
                tree.append(category_map[cat['id']])
            else:
                # Child category - add to parent's children
                parent = category_map.get(cat['parent_id'])
                if parent:
                    parent['children'].append(category_map[cat['id']])

        return jsonify(tree), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/task-counts', methods=['GET'])
def get_category_task_counts():
    """Get active task counts for each category (including immediate children)"""
    try:
        # Get all categories
        categories = execute_query(
            "SELECT id FROM categories",
            fetch='all'
        )

        # Build counts dictionary
        counts = {}

        for cat in categories:
            cat_id = cat['id']

            # Get immediate child IDs
            child_ids = get_immediate_child_ids(cat_id)
            all_ids = [cat_id] + child_ids

            # Count active tasks (not completed) in this category and immediate children
            # Use %s for PostgreSQL compatibility (db_helper will handle conversion if SQLite)
            db_type = get_db_type()
            placeholder = '%s' if db_type == 'postgres' else '?'
            placeholders = ','.join([placeholder] * len(all_ids))
            # PostgreSQL uses FALSE for boolean, SQLite uses 0
            completed_value = 'FALSE' if db_type == 'postgres' else '0'
            result = execute_query(
                f"SELECT COUNT(*) as count FROM tasks WHERE category_id IN ({placeholders}) AND completed = {completed_value}",
                tuple(all_ids),
                fetch='one'
            )

            count = result['count'] if result else 0
            if count > 0:
                counts[cat_id] = count

        return jsonify(counts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/note-counts', methods=['GET'])
def get_category_note_counts():
    """Get note counts for each category (including immediate children)"""
    try:
        # Get all categories
        categories = execute_query(
            "SELECT id FROM categories",
            fetch='all'
        )

        # Build counts dictionary
        counts = {}

        for cat in categories:
            cat_id = cat['id']

            # Get immediate child IDs
            child_ids = get_immediate_child_ids(cat_id)
            all_ids = [cat_id] + child_ids

            # Count notes in this category and immediate children
            # Use %s for PostgreSQL compatibility (db_helper will handle conversion if SQLite)
            db_type = get_db_type()
            placeholder = '%s' if db_type == 'postgres' else '?'
            placeholders = ','.join([placeholder] * len(all_ids))
            result = execute_query(
                f"SELECT COUNT(*) as count FROM notes WHERE category_id IN ({placeholders})",
                tuple(all_ids),
                fetch='one'
            )

            count = result['count'] if result else 0
            if count > 0:
                counts[cat_id] = count

        return jsonify(counts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        parent_id = data.get('parent_id')
        sort_order = data.get('sort_order', 0)

        if not name:
            return jsonify({'error': 'Category name is required'}), 400

        # Insert category
        category_id = execute_insert(
            "INSERT INTO categories (name, description, parent_id, sort_order) VALUES (?, ?, ?, ?)",
            (name, description, parent_id, sort_order)
        )

        # Return created category
        category = execute_query(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,),
            fetch='one'
        )
        return jsonify(row_to_dict(category)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update/rename a category"""
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description')
        parent_id = data.get('parent_id')
        sort_order = data.get('sort_order')

        # Build update query dynamically
        updates = []
        params = []

        if name is not None:
            updates.append("name = ?")
            params.append(name)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if parent_id is not None:
            updates.append("parent_id = ?")
            params.append(parent_id)
        if sort_order is not None:
            updates.append("sort_order = ?")
            params.append(sort_order)

        if not updates:
            return jsonify({'error': 'No fields to update'}), 400

        params.append(category_id)
        query = f"UPDATE categories SET {', '.join(updates)} WHERE id = ?"

        execute_query(query, tuple(params))

        # Return updated category
        category = execute_query(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,),
            fetch='one'
        )
        return jsonify(row_to_dict(category)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category"""
    try:
        # Check if category has children
        children = execute_query(
            "SELECT COUNT(*) as count FROM categories WHERE parent_id = ?",
            (category_id,),
            fetch='one'
        )

        if children['count'] > 0:
            return jsonify({
                'error': 'Cannot delete category with subcategories',
                'has_children': True,
                'child_count': children['count']
            }), 400

        # Check if category has tasks
        tasks = execute_query(
            "SELECT COUNT(*) as count FROM tasks WHERE category_id = ?",
            (category_id,),
            fetch='one'
        )

        if tasks['count'] > 0:
            # Get reassignment target from request (optional)
            data = request.json or {}
            reassign_to = data.get('reassign_to')
            delete_tasks = data.get('delete_tasks', False)

            if delete_tasks:
                # Delete all tasks in this category
                execute_query("DELETE FROM tasks WHERE category_id = ?", (category_id,))
            elif reassign_to:
                # Reassign tasks to another category
                execute_query(
                    "UPDATE tasks SET category_id = ? WHERE category_id = ?",
                    (reassign_to, category_id)
                )
            else:
                # Return error with task count - user needs to decide
                return jsonify({
                    'error': 'Category has tasks that need to be reassigned or deleted',
                    'has_tasks': True,
                    'task_count': tasks['count']
                }), 400

        # Delete the category
        execute_query("DELETE FROM categories WHERE id = ?", (category_id,))

        return jsonify({'message': 'Category deleted successfully'}), 200
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
        include_children = request.args.get('include_children', 'false').lower() == 'true'

        # Build query
        query = """
            SELECT t.*, c.name as category_name
            FROM tasks t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        """
        params = []

        if category_id:
            # Get category IDs to filter by
            category_ids = [int(category_id)]

            # If include_children is true, add immediate children
            if include_children:
                child_ids = get_immediate_child_ids(int(category_id))
                category_ids.extend(child_ids)

            # Build IN clause for multiple category IDs
            placeholders = ','.join('?' * len(category_ids))
            query += f" AND t.category_id IN ({placeholders})"
            params.extend(category_ids)

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

# ==================== HEALTH TRACKING ====================

@app.route('/api/health/sleep', methods=['GET', 'POST'])
def health_sleep():
    """Get or log sleep data"""
    if request.method == 'GET':
        try:
            # Optional date range filter
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            query = "SELECT * FROM sleep_logs"
            params = []

            if start_date and end_date:
                query += " WHERE date BETWEEN ? AND ? ORDER BY date DESC"
                params = [start_date, end_date]
            elif start_date:
                query += " WHERE date >= ? ORDER BY date DESC"
                params = [start_date]
            else:
                query += " ORDER BY date DESC LIMIT 30"

            rows = execute_query(query, tuple(params) if params else None, fetch='all')
            return jsonify(rows_to_list(rows)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            date = data.get('date', datetime.now().date().isoformat())
            hours = data.get('hours')
            notes = data.get('notes')

            if not hours:
                return jsonify({'error': 'hours is required'}), 400

            # Insert sleep log (PostgreSQL compatible)
            execute_insert(
                "INSERT INTO sleep_logs (date, hours, notes) VALUES (?, ?, ?)",
                (date, hours, notes),
                return_id=False
            )

            return jsonify({'date': date, 'hours': hours}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/health/water', methods=['GET', 'POST'])
def health_water():
    """Get or log water intake"""
    if request.method == 'GET':
        try:
            date = request.args.get('date', datetime.now().date().isoformat())

            # Get water logs for specific date
            rows = execute_query(
                "SELECT * FROM water_logs WHERE date = ? ORDER BY timestamp",
                (date,),
                fetch='all'
            )

            # Calculate total cups for the day
            total_cups = len(rows) if rows else 0

            return jsonify({
                'date': date,
                'total_cups': total_cups,
                'logs': rows_to_list(rows)
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            date = data.get('date', datetime.now().date().isoformat())
            cups = data.get('cups', 1)
            timestamp = data.get('timestamp', datetime.now().isoformat())

            log_id = execute_insert(
                "INSERT INTO water_logs (date, cups, timestamp) VALUES (?, ?, ?)",
                (date, cups, timestamp),
                return_id=True
            )

            return jsonify({'id': log_id, 'date': date, 'cups': cups}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/health/exercise', methods=['GET', 'POST'])
def health_exercise():
    """Get or log exercise"""
    if request.method == 'GET':
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            query = "SELECT * FROM exercise_logs"
            params = []

            if start_date and end_date:
                query += " WHERE date BETWEEN ? AND ? ORDER BY date DESC"
                params = [start_date, end_date]
            elif start_date:
                query += " WHERE date >= ? ORDER BY date DESC"
                params = [start_date]
            else:
                query += " ORDER BY date DESC LIMIT 30"

            rows = execute_query(query, tuple(params) if params else None, fetch='all')
            return jsonify(rows_to_list(rows)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            date = data.get('date', datetime.now().date().isoformat())
            activity_type = data.get('activity_type')
            duration_minutes = data.get('duration_minutes')
            notes = data.get('notes')

            if not activity_type or not duration_minutes:
                return jsonify({'error': 'activity_type and duration_minutes are required'}), 400

            log_id = execute_insert(
                "INSERT INTO exercise_logs (date, activity_type, duration_minutes, notes) VALUES (?, ?, ?, ?)",
                (date, activity_type, duration_minutes, notes),
                return_id=True
            )

            return jsonify({'id': log_id, 'date': date, 'activity_type': activity_type, 'duration_minutes': duration_minutes}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/health/sauna', methods=['GET', 'POST'])
def health_sauna():
    """Get or log sauna sessions"""
    if request.method == 'GET':
        try:
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            query = "SELECT * FROM sauna_logs"
            params = []

            if start_date and end_date:
                query += " WHERE date BETWEEN ? AND ? ORDER BY date DESC"
                params = [start_date, end_date]
            elif start_date:
                query += " WHERE date >= ? ORDER BY date DESC"
                params = [start_date]
            else:
                query += " ORDER BY date DESC LIMIT 30"

            rows = execute_query(query, tuple(params) if params else None, fetch='all')
            return jsonify(rows_to_list(rows)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            date = data.get('date', datetime.now().date().isoformat())
            num_visits = data.get('num_visits', 1)
            duration_minutes = data.get('duration_minutes')

            if not duration_minutes:
                return jsonify({'error': 'duration_minutes is required'}), 400

            # Insert sauna log (PostgreSQL compatible)
            execute_insert(
                "INSERT INTO sauna_logs (date, num_visits, duration_minutes) VALUES (?, ?, ?)",
                (date, num_visits, duration_minutes),
                return_id=False
            )

            return jsonify({'date': date, 'num_visits': num_visits, 'duration_minutes': duration_minutes}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/health/inbody', methods=['GET', 'POST'])
def health_inbody():
    """Get or log InBody measurements"""
    if request.method == 'GET':
        try:
            # Get all InBody measurements, most recent first
            rows = execute_query(
                "SELECT * FROM inbody_measurements ORDER BY date DESC LIMIT 20",
                fetch='all'
            )
            return jsonify(rows_to_list(rows)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            date = data.get('date', datetime.now().date().isoformat())
            weight = data.get('weight')
            smm = data.get('smm')
            pbf = data.get('pbf')
            ecw_tbw_ratio = data.get('ecw_tbw_ratio')
            notes = data.get('notes')

            if not all([weight, smm, pbf, ecw_tbw_ratio]):
                return jsonify({'error': 'weight, smm, pbf, and ecw_tbw_ratio are required'}), 400

            # Insert InBody measurement (PostgreSQL compatible)
            execute_insert(
                "INSERT INTO inbody_measurements (date, weight, smm, pbf, ecw_tbw_ratio, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (date, weight, smm, pbf, ecw_tbw_ratio, notes),
                return_id=False
            )

            return jsonify({'date': date, 'weight': weight}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/health/summary', methods=['GET'])
def health_summary():
    """Get today's health summary"""
    try:
        today = datetime.now().date().isoformat()

        # Sleep
        sleep_row = execute_query(
            "SELECT hours FROM sleep_logs WHERE date = ?",
            (today,),
            fetch='one'
        )
        sleep_hours = sleep_row['hours'] if sleep_row else None

        # Water
        water_rows = execute_query(
            "SELECT COUNT(*) as total FROM water_logs WHERE date = ?",
            (today,),
            fetch='one'
        )
        water_cups = water_rows['total'] if water_rows else 0

        # Exercise
        exercise_rows = execute_query(
            "SELECT SUM(duration_minutes) as total FROM exercise_logs WHERE date = ?",
            (today,),
            fetch='one'
        )
        exercise_minutes = exercise_rows['total'] if exercise_rows and exercise_rows['total'] else 0

        # Sauna
        sauna_row = execute_query(
            "SELECT num_visits, duration_minutes FROM sauna_logs WHERE date = ?",
            (today,),
            fetch='one'
        )
        sauna_data = row_to_dict(sauna_row) if sauna_row else None

        # Latest InBody
        inbody_row = execute_query(
            "SELECT * FROM inbody_measurements ORDER BY date DESC LIMIT 1",
            fetch='one'
        )
        inbody_data = row_to_dict(inbody_row) if inbody_row else None

        return jsonify({
            'date': today,
            'sleep_hours': sleep_hours,
            'water_cups': water_cups,
            'exercise_minutes': exercise_minutes,
            'sauna': sauna_data,
            'latest_inbody': inbody_data
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
    print("Life OS API Server starting...")
    print(f"Database: {get_db_type()}")
    print("CORS enabled for frontend development")
    print("Server running on http://localhost:5000")
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
    print("  GET/POST /api/health/sleep")
    print("  GET/POST /api/health/water")
    print("  GET/POST /api/health/exercise")
    print("  GET/POST /api/health/sauna")
    print("  GET/POST /api/health/inbody")
    print("  GET    /api/health/summary")

    app.run(debug=True, host='0.0.0.0', port=5000)
