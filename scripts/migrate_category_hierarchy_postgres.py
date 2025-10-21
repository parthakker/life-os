"""
Migration Script: Add Category Hierarchy (PostgreSQL Compatible)
Adds parent_id column and parses existing category names to build parent-child relationships
"""

from db_helper import execute_query, execute_insert, get_db_connection

def migrate_category_hierarchy():
    """Add parent_id column and parse category hierarchy"""

    print("=" * 60)
    print("CATEGORY HIERARCHY MIGRATION (PostgreSQL)")
    print("=" * 60)

    conn, cursor, db_type = get_db_connection()

    if db_type != 'postgres':
        print(f"\n[WARNING] This script is for PostgreSQL, but detected: {db_type}")
        print("Use migrate_category_hierarchy.py for SQLite instead")
        conn.close()
        return

    # Step 1: Add parent_id column if it doesn't exist
    print("\n1. Adding parent_id column...")
    try:
        cursor.execute("""
            ALTER TABLE categories
            ADD COLUMN IF NOT EXISTS parent_id INTEGER REFERENCES categories(id)
        """)
        conn.commit()
        print("   [OK] parent_id column added")
    except Exception as e:
        if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
            print("   [OK] parent_id column already exists")
        else:
            raise

    # Step 2: Get all categories
    print("\n2. Fetching existing categories...")
    categories = execute_query("SELECT id, name FROM categories ORDER BY name", fetch='all')
    print(f"   [OK] Found {len(categories)} categories")

    # Step 3: Create parent categories and build hierarchy
    print("\n3. Creating parent categories...")

    # Find all unique parent names that need to be created
    parent_names_needed = set()
    for cat in categories:
        if " - " in cat['name']:
            parts = cat['name'].split(" - ")
            # Add all possible parent levels
            for i in range(1, len(parts)):
                parent_name = " - ".join(parts[:i])
                parent_names_needed.add(parent_name)

    # Create a mapping of category names to IDs
    name_to_id = {cat['name']: cat['id'] for cat in categories}

    # Create missing parent categories
    parents_created = 0
    for parent_name in sorted(parent_names_needed):
        if parent_name not in name_to_id:
            # Create the parent category
            cursor.execute(
                "INSERT INTO categories (name, description, sort_order) VALUES (%s, %s, %s) RETURNING id",
                (parent_name, f"Auto-created parent category", 0)
            )
            parent_id = cursor.fetchone()[0]
            conn.commit()
            name_to_id[parent_name] = parent_id
            parents_created += 1
            print(f"   [NEW] Created parent: {parent_name} (ID: {parent_id})")

    print(f"   [OK] Created {parents_created} parent categories")

    # Step 4: Build parent-child relationships
    print("\n4. Building parent-child relationships...")
    updates = []

    for category in categories:
        name = category['name']
        cat_id = category['id']

        # Check if category name contains " - " separator
        if " - " in name:
            # Split by " - " to find immediate parent
            parts = name.split(" - ")

            # Try to find parent by checking progressively longer prefixes
            parent_name = None
            for i in range(len(parts) - 1, 0, -1):
                potential_parent = " - ".join(parts[:i])
                if potential_parent in name_to_id and name_to_id[potential_parent] != cat_id:
                    parent_name = potential_parent
                    break

            if parent_name:
                parent_id = name_to_id[parent_name]
                updates.append((parent_id, cat_id, name, parent_name))
                print(f"   - {name}")
                print(f"     -> Parent: {parent_name} (ID: {parent_id})")

    # Step 5: Apply updates
    print(f"\n5. Applying {len(updates)} parent-child relationships...")
    for parent_id, cat_id, child_name, parent_name in updates:
        cursor.execute(
            "UPDATE categories SET parent_id = %s WHERE id = %s",
            (parent_id, cat_id)
        )
    conn.commit()
    print("   [OK] Relationships applied")

    # Step 6: Verify the migration
    print("\n6. Verification:")
    top_level = execute_query(
        "SELECT COUNT(*) as count FROM categories WHERE parent_id IS NULL",
        fetch='one'
    )
    with_parents = execute_query(
        "SELECT COUNT(*) as count FROM categories WHERE parent_id IS NOT NULL",
        fetch='one'
    )

    print(f"   - Top-level categories: {top_level['count']}")
    print(f"   - Subcategories: {with_parents['count']}")

    # Show the tree structure
    print("\n7. Category Tree Preview:")
    top_categories = execute_query(
        "SELECT id, name FROM categories WHERE parent_id IS NULL ORDER BY name LIMIT 10",
        fetch='all'
    )

    for top_cat in top_categories:
        print(f"\n   [Folder] {top_cat['name']}")
        children = execute_query(
            "SELECT name FROM categories WHERE parent_id = %s ORDER BY name",
            (top_cat['id'],),
            fetch='all'
        )
        for child in children[:5]:  # Show first 5 children
            print(f"      -> {child['name']}")
        if len(children) > 5:
            print(f"      -> ... and {len(children) - 5} more")

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    migrate_category_hierarchy()
