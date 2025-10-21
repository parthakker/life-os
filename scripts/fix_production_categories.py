"""
Fix Production Database Issues:
1. Remove "Wedding - Wedding" duplicate category
2. Re-parent wedding subcategories to "Wedding"
3. Add missing descriptions to auto-created categories
"""

import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("[ERROR] DATABASE_URL not set")
    exit(1)

print("=" * 70)
print("PRODUCTION DATABASE FIX")
print("=" * 70)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Step 1: Identify the problematic category
print("\n[1/5] Identifying 'Wedding - Wedding' category...")
cursor.execute("SELECT id, name, parent_id FROM categories WHERE name = 'Wedding - Wedding'")
bad_category = cursor.fetchone()

if not bad_category:
    print("  Category 'Wedding - Wedding' not found. Database may already be fixed.")
    conn.close()
    exit(0)

print(f"  Found: ID {bad_category['id']} - '{bad_category['name']}' (parent: {bad_category['parent_id']})")

# Step 2: Find the correct Wedding parent category
print("\n[2/5] Finding correct 'Wedding' parent category...")
cursor.execute("SELECT id, name FROM categories WHERE name = 'Wedding' AND parent_id IS NULL")
wedding_parent = cursor.fetchone()

if not wedding_parent:
    print("  ERROR: Could not find top-level 'Wedding' category!")
    conn.close()
    exit(1)

print(f"  Found: ID {wedding_parent['id']} - '{wedding_parent['name']}'")

# Step 3: Find all children of "Wedding - Wedding"
print("\n[3/5] Finding children of 'Wedding - Wedding'...")
cursor.execute("""
    SELECT id, name
    FROM categories
    WHERE parent_id = %s
    ORDER BY name
""", (bad_category['id'],))
children = cursor.fetchall()

print(f"  Found {len(children)} children:")
for child in children:
    print(f"    - ID {child['id']}: {child['name']}")

# Step 4: Re-parent children to correct Wedding category
print("\n[4/5] Re-parenting children to 'Wedding' (ID {wedding_parent['id']})...")
for child in children:
    cursor.execute("""
        UPDATE categories
        SET parent_id = %s
        WHERE id = %s
    """, (wedding_parent['id'], child['id']))
    print(f"  [OK] Updated ID {child['id']}: {child['name']}")

conn.commit()
print(f"  [OK] Re-parented {len(children)} categories")

# Step 5: Delete the "Wedding - Wedding" category
print("\n[5/5] Deleting 'Wedding - Wedding' category...")
cursor.execute("DELETE FROM categories WHERE id = %s", (bad_category['id'],))
conn.commit()
print(f"  [OK] Deleted category ID {bad_category['id']}")

# Step 6: Add missing descriptions
print("\n[6/7] Adding missing descriptions...")

DESCRIPTIONS = {
    "Family": "Family members, relationships, coordination",
    "Hobbies": "Personal hobbies, interests, and activities",
    "Notes": "General notes and information storage",
    "Preeti": "Notes about Preeti (fiancée)",
    "Princeton AI": "AI consulting business",
    "Princeton AI Partners": "Client projects and business operations",
    "Tasks": "Generic catch-all tasks",
    "Tasks - General": "Miscellaneous tasks not fitting other categories",
    "Wedding": "Wedding planning and coordination",
    "Upcoming Events + Birthdays": "Upcoming events, birthdays, important dates",
    "Quotes": "Inspirational quotes and sayings",
    "Important Events": "Important events related to Preeti",
    "Preeti - Notes": "Notes about Preeti",
    "Preeti - Tasks": "Tasks related to Preeti"
}

updated_desc = 0
for name, desc in DESCRIPTIONS.items():
    cursor.execute("""
        UPDATE categories
        SET description = %s
        WHERE name = %s AND (description IS NULL OR description = '' OR description = 'Auto-created parent category')
    """, (desc, name))
    if cursor.rowcount > 0:
        print(f"  [OK] Added description to '{name}'")
        updated_desc += 1

conn.commit()
print(f"  [OK] Updated {updated_desc} category descriptions")

# Step 7: Verification
print("\n[7/7] Verifying fixes...")

cursor.execute("SELECT COUNT(*) as count FROM categories WHERE name = 'Wedding - Wedding'")
should_be_zero = cursor.fetchone()['count']
print(f"  'Wedding - Wedding' categories: {should_be_zero} (should be 0)")

cursor.execute("SELECT COUNT(*) as count FROM categories WHERE parent_id = %s", (wedding_parent['id'],))
wedding_children = cursor.fetchone()['count']
print(f"  'Wedding' has {wedding_children} direct children (should be 7)")

cursor.execute("SELECT COUNT(*) as count FROM categories WHERE description IS NOT NULL AND description != ''")
with_desc = cursor.fetchone()['count']
print(f"  Categories with descriptions: {with_desc}/49")

conn.close()

print("\n" + "=" * 70)
print("FIX COMPLETED SUCCESSFULLY!")
print("=" * 70)
print("\nChanges made:")
print(f"  - Deleted 'Wedding - Wedding' category")
print(f"  - Re-parented {len(children)} wedding subcategories to 'Wedding'")
print(f"  - Added {updated_desc} missing descriptions")
print("\nNext: Test the bot via Telegram")
