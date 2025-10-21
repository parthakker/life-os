"""
Diagnostic Script: Check Production PostgreSQL Database
Queries production to see actual schema and data state
"""

import os
import psycopg2
import psycopg2.extras

# Production database URL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL not set")
    print("Run this script with: export DATABASE_URL='your-postgres-url'")
    exit(1)

print("=" * 70)
print("PRODUCTION DATABASE DIAGNOSTIC")
print("=" * 70)

# Connect
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print("\n[1/6] Checking tables...")
cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    ORDER BY table_name
""")
tables = cursor.fetchall()
print(f"Tables found: {len(tables)}")
for table in tables:
    print(f"  - {table['table_name']}")

print("\n[2/6] Checking categories table schema...")
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_schema = 'public'
    AND table_name = 'categories'
    ORDER BY ordinal_position
""")
columns = cursor.fetchall()
print(f"Categories table columns:")
for col in columns:
    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
    print(f"  - {col['column_name']:15s} {col['data_type']:15s} {nullable}")

print("\n[3/6] Checking category data...")
cursor.execute("SELECT COUNT(*) as count FROM categories")
total = cursor.fetchone()['count']
print(f"Total categories: {total}")

cursor.execute("SELECT COUNT(*) as count FROM categories WHERE parent_id IS NULL")
top_level = cursor.fetchone()['count']
print(f"Top-level categories: {top_level}")

cursor.execute("SELECT COUNT(*) as count FROM categories WHERE parent_id IS NOT NULL")
children = cursor.fetchone()['count']
print(f"Child categories: {children}")

cursor.execute("SELECT COUNT(*) as count FROM categories WHERE description IS NOT NULL AND description != ''")
with_desc = cursor.fetchone()['count']
print(f"Categories with descriptions: {with_desc}")

print("\n[4/6] Checking for duplicate/malformed category names...")
cursor.execute("""
    SELECT name, COUNT(*) as count
    FROM categories
    GROUP BY name
    HAVING COUNT(*) > 1
""")
duplicates = cursor.fetchall()
if duplicates:
    print(f"DUPLICATES FOUND: {len(duplicates)}")
    for dup in duplicates:
        print(f"  - '{dup['name']}' appears {dup['count']} times")
else:
    print("No duplicate category names found")

print("\n[5/6] Sample category data (first 15)...")
cursor.execute("""
    SELECT id, name, description, parent_id, sort_order
    FROM categories
    ORDER BY id
    LIMIT 15
""")
samples = cursor.fetchall()
print(f"\n{'ID':<5} {'Name':<30} {'Parent':<7} {'Desc?':<6}")
print("-" * 70)
for cat in samples:
    has_desc = "Yes" if cat['description'] else "No"
    parent = str(cat['parent_id']) if cat['parent_id'] else "NULL"
    name = cat['name'][:28] if len(cat['name']) <= 28 else cat['name'][:25] + "..."
    print(f"{cat['id']:<5} {name:<30} {parent:<7} {has_desc:<6}")

# Look for problematic patterns
print("\n[6/6] Looking for problematic category names...")
cursor.execute("""
    SELECT id, name
    FROM categories
    WHERE name LIKE '%Wedding - Wedding%'
       OR name LIKE '%Tasks - Tasks%'
       OR name LIKE '%- - %'
    ORDER BY name
""")
problematic = cursor.fetchall()
if problematic:
    print(f"PROBLEMATIC NAMES FOUND: {len(problematic)}")
    for cat in problematic:
        print(f"  ID {cat['id']}: '{cat['name']}'")
else:
    print("No obviously problematic category names found")

print("\n" + "=" * 70)
print("TASKS & NOTES CHECK")
print("=" * 70)

cursor.execute("SELECT COUNT(*) as count FROM tasks")
task_count = cursor.fetchone()['count']
print(f"Total tasks: {task_count}")

cursor.execute("SELECT COUNT(*) as count FROM notes")
note_count = cursor.fetchone()['count']
print(f"Total notes: {note_count}")

print("\n" + "=" * 70)
print("HEALTH TABLES CHECK")
print("=" * 70)

health_tables = ['sleep_logs', 'water_logs', 'exercise_logs', 'sauna_logs', 'inbody_measurements']
for table in health_tables:
    try:
        cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
        count = cursor.fetchone()['count']
        print(f"{table:25s}: {count} entries")
    except Exception as e:
        print(f"{table:25s}: TABLE DOES NOT EXIST")

conn.close()

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
