"""
Migration Script: Populate Category Descriptions (PostgreSQL Compatible)
Migrates hardcoded category context from router.py to database descriptions field
"""

from db_helper import execute_query, get_db_connection

# Category descriptions from router.py (lines 104-150+)
CATEGORY_DESCRIPTIONS = {
    # Top-level categories
    "Buddy": "Dog care, health, vet appointments",
    "Home": "House maintenance, HOA, Brad rent, cleaning, furniture",
    "Bills": "Bill payments and tracking (reference only)",
    "Personal Projects": "Life OS, Personal Assistant, NFL for Indians, Podcast, Claude Code",
    "Betting": "Sports betting, Beat Writer Scraper, betting tracking, active bets",
    "Events": "Upcoming events, birthdays, important dates",
    "Social": "Friends visiting, social coordination",
    "Tasks": "Generic catch-all tasks",

    # Family subcategories
    "Family": "Family members, relationships, coordination",
    "Immediate Family": "Mom, Dad, Mansi (sister) - bank, passwords, insurance",
    "USA Family": "Jay, Aayushi, Surekha Aunty, Suraj - job help, design discussion",
    "India Family": "Dadi, Dada, Nani - weekly follow up",

    # Hobbies subcategories
    "Hobbies": "Personal hobbies, interests, and activities",
    "GYM": "Gym workouts, fitness",
    "BJJ": "Brazilian Jiu-Jitsu training and practice",
    "Video Games": "Gaming, Madden, esports",
    "Television/Movies": "TV shows, movies, entertainment",
    "FOOTBALL": "NFL, fantasy football, game analysis",
    "Photography": "Photos, camera equipment, shoots",
    "Guitar": "Music, guitar playing, practice",
    "Yoga": "Yoga practice and mindfulness",
    "Finance": "Financial topics, investing, markets",
    "Politics": "Political interests and discussions",
    "AI": "AI topics, learning, research",
    "Extra-Curricular": "Other hobbies and activities",
    "Cricket": "Cricket interests and matches",

    # Wedding subcategories
    "Wedding": "Wedding planning and coordination",
    "Vendors": "Grove, Pasha, photobooth, invitations",
    "Things Needed from Family": "Guest list, family coordination",
    "Bachelor Party": "Planning, Suns game, ATV, coordination",
    "Dances": "Dance planning and choreography",
    "Speeches": "Speech planning and preparation",
    "Décor": "Clothes, outfits, décor items",
    "Engagement Pooja": "Engagement event planning and coordination",

    # Princeton AI Partners subcategories
    "Princeton AI": "AI consulting business",
    "Princeton AI Partners": "Client projects and business operations",
    "Princeton-ai.com": "Website development and maintenance",
    "UpLevel Resume": "Client project - resume optimization",
    "Hamilton Deli": "Client project ($50/mo) - Akshay contact",
    "Overview": "General business, Jasjit, Liji, SELL strategy",
    "Generic Tasks": "N8N workflows, Mercury banking, Stripe monitoring",

    # Notes subcategories (if they exist)
    "Notes": "General notes and information storage",
    "Preeti": "Notes about Preeti (fiancée)",
    "Mom": "Notes about Mom",
    "Dad": "Notes about Dad",
    "Mansi": "Notes about Mansi (sister)",
    "General": "General notes not categorized",
}


def migrate_descriptions():
    """Populate category descriptions from hardcoded mapping"""

    print("=" * 60)
    print("CATEGORY DESCRIPTION MIGRATION (PostgreSQL)")
    print("=" * 60)

    conn, cursor, db_type = get_db_connection()

    if db_type != 'postgres':
        print(f"\n[WARNING] This script is for PostgreSQL, but detected: {db_type}")
        print("Use migrate_category_descriptions.py for SQLite instead")
        conn.close()
        return

    # First ensure description column exists
    print("\n0. Ensuring description column exists...")
    try:
        cursor.execute("""
            ALTER TABLE categories
            ADD COLUMN IF NOT EXISTS description TEXT
        """)
        conn.commit()
        print("   [OK] description column ready")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   [OK] description column already exists")
        else:
            raise

    # Get all categories
    categories = execute_query(
        "SELECT id, name, description FROM categories",
        fetch='all'
    )

    updated = 0
    skipped = 0
    not_found = 0

    print(f"\nProcessing {len(categories)} categories...")

    for cat in categories:
        cat_id = cat['id']
        cat_name = cat['name']
        current_desc = cat['description']

        # Check if description exists in our mapping
        if cat_name in CATEGORY_DESCRIPTIONS:
            new_desc = CATEGORY_DESCRIPTIONS[cat_name]

            # Only update if currently NULL or empty
            if not current_desc or current_desc.strip() == '':
                print(f"  [UPDATE] {cat_name} -> \"{new_desc}\"")
                cursor.execute(
                    "UPDATE categories SET description = %s WHERE id = %s",
                    (new_desc, cat_id)
                )
                updated += 1
            else:
                print(f"  [SKIP] {cat_name} (already has description: \"{current_desc}\")")
                skipped += 1
        else:
            print(f"  [NOT FOUND] {cat_name} (no description in mapping)")
            not_found += 1

    conn.commit()

    print(f"\n{'-' * 60}")
    print(f"SUMMARY:")
    print(f"  Updated: {updated}")
    print(f"  Skipped (already has description): {skipped}")
    print(f"  Not found in mapping: {not_found}")
    print(f"  Total: {len(categories)}")
    print("=" * 60)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    migrate_descriptions()
