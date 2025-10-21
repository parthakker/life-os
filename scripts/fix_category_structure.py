"""
Migration Script: Fix Category Structure
1. Fix parent_id for Princeton AI and Wedding hierarchies
2. Clean up redundant parent names from child categories
"""

from db_helper import execute_query, get_db_connection
import sqlite3

def fix_category_structure():
    """Fix category hierarchy and clean up names"""

    print("=" * 60)
    print("CATEGORY STRUCTURE FIX")
    print("=" * 60)

    conn, cursor, db_type = get_db_connection()

    # Step 1: Fix Princeton AI hierarchy
    print("\n1. Fixing Princeton AI hierarchy...")
    print("   Setting 'Princeton AI - Princeton AI Partners' (113) as child of 'Princeton AI' (112)")
    cursor.execute("UPDATE categories SET parent_id = 112 WHERE id = 113")
    conn.commit()
    print("   [OK] Princeton AI hierarchy fixed")

    # Step 2: Fix Wedding hierarchy
    print("\n2. Fixing Wedding hierarchy...")
    print("   Setting 'Wedding - Wedding' (116) as child of 'Wedding' (115)")
    cursor.execute("UPDATE categories SET parent_id = 115 WHERE id = 116")
    conn.commit()
    print("   [OK] Wedding hierarchy fixed")

    # Step 3: Get all categories with parent_id set
    print("\n3. Cleaning up redundant parent names from child categories...")
    children = execute_query(
        """
        SELECT c.id, c.name, c.parent_id, p.name as parent_name
        FROM categories c
        JOIN categories p ON c.parent_id = p.id
        ORDER BY c.name
        """,
        fetch='all'
    )

    cleaned = 0
    skipped = 0
    used_names = set()

    # First, get all existing category names
    all_names = execute_query("SELECT name FROM categories", fetch='all')
    for name_row in all_names:
        used_names.add(name_row['name'])

    for child in children:
        child_name = child['name']
        parent_name = child['parent_name']

        # Check if child name starts with parent name followed by " - "
        if child_name.startswith(parent_name + " - "):
            # Remove the parent prefix
            new_name = child_name[len(parent_name) + 3:]  # +3 for " - "

            # Check if this new name would conflict
            if new_name in used_names and new_name != child_name:
                print(f"   [SKIP] '{child_name}' (would create duplicate '{new_name}')")
                skipped += 1
            else:
                print(f"   Renaming: '{child_name}' -> '{new_name}'")
                cursor.execute(
                    "UPDATE categories SET name = ? WHERE id = ?",
                    (new_name, child['id'])
                )
                # Update tracking
                used_names.remove(child_name)
                used_names.add(new_name)
                cleaned += 1

    conn.commit()
    print(f"   [OK] Cleaned {cleaned} category names ({skipped} skipped due to conflicts)")

    # Step 4: Verify the structure
    print("\n4. Verification:")

    # Check top-level categories
    top_level = execute_query(
        "SELECT COUNT(*) as count FROM categories WHERE parent_id IS NULL",
        fetch='one'
    )
    print(f"   - Top-level categories: {top_level['count']}")

    # Check children
    with_parents = execute_query(
        "SELECT COUNT(*) as count FROM categories WHERE parent_id IS NOT NULL",
        fetch='one'
    )
    print(f"   - Child categories: {with_parents['count']}")

    # Show Princeton AI structure
    print("\n5. Sample Structure - Princeton AI:")
    princeton = execute_query(
        """
        SELECT id, name, parent_id FROM categories
        WHERE id = 112 OR parent_id = 112 OR parent_id = 113 OR id = 113
        ORDER BY parent_id, name
        """,
        fetch='all'
    )
    for cat in princeton:
        if cat['parent_id'] is None:
            print(f"   [Folder] {cat['name']} (ID: {cat['id']})")
        elif cat['parent_id'] == 112:
            print(f"      -> {cat['name']} (ID: {cat['id']})")
        elif cat['parent_id'] == 113:
            print(f"         -> {cat['name']} (ID: {cat['id']})")

    # Show Wedding structure
    print("\n6. Sample Structure - Wedding:")
    wedding = execute_query(
        """
        SELECT id, name, parent_id FROM categories
        WHERE id = 115 OR parent_id = 115 OR parent_id = 116 OR id = 116
        ORDER BY parent_id, name
        """,
        fetch='all'
    )
    for cat in wedding:
        if cat['parent_id'] is None:
            print(f"   [Folder] {cat['name']} (ID: {cat['id']})")
        elif cat['parent_id'] == 115:
            print(f"      -> {cat['name']} (ID: {cat['id']})")
        elif cat['parent_id'] == 116:
            print(f"         -> {cat['name']} (ID: {cat['id']})")

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    fix_category_structure()
