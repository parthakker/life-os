"""
Database Helper - Auto-detects PostgreSQL vs SQLite
Uses DATABASE_URL env var to determine which database to use
"""

import os
import sqlite3
from pathlib import Path

DATABASE_URL = os.getenv('DATABASE_URL')
DB_PATH = Path(__file__).parent.parent / 'data.db'

# If DATABASE_URL is set, we MUST use PostgreSQL
if DATABASE_URL:
    try:
        import psycopg2
        import psycopg2.extras
        PSYCOPG2_AVAILABLE = True
    except ImportError as e:
        print(f"[CRITICAL ERROR] DATABASE_URL is set but psycopg2 is not available!")
        print(f"Import error: {e}")
        print("Install with: pip install psycopg2-binary")
        raise RuntimeError("Cannot use PostgreSQL without psycopg2-binary")
else:
    # Local development - try to import but don't require it
    try:
        import psycopg2
        import psycopg2.extras
        PSYCOPG2_AVAILABLE = True
    except ImportError:
        PSYCOPG2_AVAILABLE = False

def get_db_connection():
    """
    Get database connection - auto-detects PostgreSQL vs SQLite
    Returns: (connection, cursor, db_type)
    """
    if DATABASE_URL and PSYCOPG2_AVAILABLE:
        # Production: Use PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return conn, cursor, 'postgres'
    else:
        # Local development: Use SQLite
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        return conn, cursor, 'sqlite'

def execute_query(query, params=None, fetch=None):
    """
    Execute a database query with automatic connection handling

    Args:
        query: SQL query string (use %s for PostgreSQL, ? for SQLite)
        params: Query parameters (tuple or list)
        fetch: 'one', 'all', or None

    Returns:
        Query results or None
    """
    conn, cursor, db_type = get_db_connection()

    # Convert query placeholders if needed
    if db_type == 'postgres' and '?' in query:
        query = query.replace('?', '%s')

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if fetch == 'one':
            result = cursor.fetchone()
        elif fetch == 'all':
            result = cursor.fetchall()
        else:
            result = None

        conn.commit()
        return result

    finally:
        conn.close()

def execute_insert(query, params, return_id=True):
    """
    Execute an INSERT query and optionally return the new row ID

    Args:
        query: SQL INSERT statement
        params: Query parameters
        return_id: Whether to return the new row ID

    Returns:
        New row ID or None
    """
    conn, cursor, db_type = get_db_connection()

    # Convert query placeholders if needed
    if db_type == 'postgres':
        query = query.replace('?', '%s')
        if return_id and 'RETURNING id' not in query:
            query += ' RETURNING id'

    try:
        cursor.execute(query, params)

        if return_id:
            if db_type == 'postgres':
                result = cursor.fetchone()
                new_id = result[0] if result else None
            else:
                new_id = cursor.lastrowid
        else:
            new_id = None

        conn.commit()
        return new_id

    finally:
        conn.close()

def get_db_type():
    """Return current database type: 'postgres' or 'sqlite'"""
    if DATABASE_URL and PSYCOPG2_AVAILABLE:
        return 'postgres'
    return 'sqlite'
