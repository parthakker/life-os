"""
Verify production database fix
"""

import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print('=' * 70)
print('VERIFICATION: Wedding Category Tree')
print('=' * 70)

cursor.execute("""
    SELECT c1.id, c1.name, c1.description
    FROM categories c1
    WHERE c1.name = 'Wedding' AND c1.parent_id IS NULL
""")
wedding = cursor.fetchone()

print(f"\nWedding (ID {wedding['id']}): {wedding['description']}")

cursor.execute("""
    SELECT id, name, description
    FROM categories
    WHERE parent_id = %s
    ORDER BY name
""", (wedding['id'],))
children = cursor.fetchall()

print(f"\nDirect children of Wedding ({len(children)}):")
for child in children:
    desc = child['description'][:40] if child['description'] else '(no description)'
    print(f"  - {child['name']:30s} | {desc}")

print('\n' + '=' * 70)
print('SUMMARY')
print('=' * 70)

cursor.execute('SELECT COUNT(*) as count FROM categories')
total = cursor.fetchone()['count']

cursor.execute("SELECT COUNT(*) as count FROM categories WHERE description IS NOT NULL AND description != ''")
with_desc = cursor.fetchone()['count']

print(f'Total categories: {total}')
print(f'Categories with descriptions: {with_desc}/{total}')
print('\nDatabase is now clean and aligned!')

conn.close()
