"""
One-time migration script: SQLite (data.db) → PostgreSQL
Run this after deploying to Render to migrate your existing data
"""

import os
import sqlite3
import psycopg2
from pathlib import Path

# Paths
DB_PATH = Path(__file__).parent.parent / 'data.db'
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL environment variable not set")
    print("This script should be run on Render after deployment")
    exit(1)

print("[Migration] Starting SQLite → PostgreSQL migration...")
print(f"[Migration] Source: {DB_PATH}")
print(f"[Migration] Target: PostgreSQL (DATABASE_URL)")

# Connect to SQLite
sqlite_conn = sqlite3.connect(DB_PATH)
sqlite_cursor = sqlite_conn.cursor()

# Connect to PostgreSQL
pg_conn = psycopg2.connect(DATABASE_URL)
pg_cursor = pg_conn.cursor()

# Create PostgreSQL schema
print("\n[1/4] Creating PostgreSQL tables...")

pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        parent_category TEXT,
        sort_order INTEGER DEFAULT 0
    )
""")

pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        category_id INTEGER REFERENCES categories(id),
        content TEXT NOT NULL,
        due_date TEXT,
        completed BOOLEAN DEFAULT FALSE,
        created_date TEXT NOT NULL
    )
""")

pg_cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id SERIAL PRIMARY KEY,
        category_id INTEGER REFERENCES categories(id),
        content TEXT NOT NULL,
        created_date TEXT NOT NULL
    )
""")

pg_conn.commit()
print("[✓] Tables created successfully")

# Migrate categories
print("\n[2/4] Migrating categories...")
sqlite_cursor.execute("SELECT id, name, parent_category, sort_order FROM categories ORDER BY id")
categories = sqlite_cursor.fetchall()

category_id_map = {}  # Old ID → New ID mapping

for old_id, name, parent_category, sort_order in categories:
    pg_cursor.execute(
        "INSERT INTO categories (name, parent_category, sort_order) VALUES (%s, %s, %s) RETURNING id",
        (name, parent_category, sort_order)
    )
    new_id = pg_cursor.fetchone()[0]
    category_id_map[old_id] = new_id

pg_conn.commit()
print(f"[✓] Migrated {len(categories)} categories")

# Migrate tasks
print("\n[3/4] Migrating tasks...")
sqlite_cursor.execute("SELECT category_id, content, due_date, completed, created_date FROM tasks")
tasks = sqlite_cursor.fetchall()

for category_id, content, due_date, completed, created_date in tasks:
    new_category_id = category_id_map.get(category_id)
    if new_category_id:
        pg_cursor.execute(
            "INSERT INTO tasks (category_id, content, due_date, completed, created_date) VALUES (%s, %s, %s, %s, %s)",
            (new_category_id, content, due_date, bool(completed), created_date)
        )

pg_conn.commit()
print(f"[✓] Migrated {len(tasks)} tasks")

# Migrate notes
print("\n[4/4] Migrating notes...")
sqlite_cursor.execute("SELECT category_id, content, created_date FROM notes")
notes = sqlite_cursor.fetchall()

for category_id, content, created_date in notes:
    new_category_id = category_id_map.get(category_id)
    if new_category_id:
        pg_cursor.execute(
            "INSERT INTO notes (category_id, content, created_date) VALUES (%s, %s, %s)",
            (new_category_id, content, created_date)
        )

pg_conn.commit()
print(f"[✓] Migrated {len(notes)} notes")

# Verify migration
print("\n[Verification]")
pg_cursor.execute("SELECT COUNT(*) FROM categories")
print(f"  Categories: {pg_cursor.fetchone()[0]}")

pg_cursor.execute("SELECT COUNT(*) FROM tasks")
print(f"  Tasks: {pg_cursor.fetchone()[0]}")

pg_cursor.execute("SELECT COUNT(*) FROM notes")
print(f"  Notes: {pg_cursor.fetchone()[0]}")

# Close connections
sqlite_conn.close()
pg_conn.close()

print("\n[✓] Migration completed successfully!")
print("\nNext steps:")
print("1. Test your bot via Telegram")
print("2. Verify data with /stats command")
print("3. If everything works, you can delete data.db from local and re-hide in .gitignore")
