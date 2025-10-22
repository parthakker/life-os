"""
Migrate Health Data from Local SQLite to Production PostgreSQL
Transfers 306 health records (sleep, water, exercise, sauna, InBody)
"""

import os
import sqlite3
from pathlib import Path

# Set production database URL
PROD_DB_URL = "postgresql://lifeos_user:nS2SUCw1PRQ4CZvzJELSuWGptCtbQMz7@dpg-d3r8oj6uk2gs73cbdlu0-a.ohio-postgres.render.com/lifeos"
os.environ['DATABASE_URL'] = PROD_DB_URL

# Import after setting DATABASE_URL
from db_helper import execute_insert, execute_query

# Local SQLite database
LOCAL_DB = Path(__file__).parent.parent / 'data.db'

def migrate_table(table_name, columns):
    """
    Migrate a single health table from SQLite to PostgreSQL

    Args:
        table_name: Name of the table (sleep_logs, water_logs, etc.)
        columns: List of column names to migrate
    """
    print(f"\n{'='*60}")
    print(f"Migrating {table_name}...")
    print(f"{'='*60}")

    # Connect to local SQLite
    local_conn = sqlite3.connect(LOCAL_DB)
    local_conn.row_factory = sqlite3.Row
    local_cursor = local_conn.cursor()

    try:
        # Get all records from local database
        local_cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
        local_records = local_cursor.fetchall()

        if not local_records:
            print(f"[INFO] No records found in local {table_name}")
            return 0

        print(f"[OK] Found {len(local_records)} records in local {table_name}")

        # Check if production already has data
        prod_count = execute_query(f"SELECT COUNT(*) as count FROM {table_name}", fetch='one')
        if prod_count and prod_count['count'] > 0:
            print(f"[WARNING] Production {table_name} already has {prod_count['count']} records")
            response = input(f"Continue and add {len(local_records)} more records? (y/n): ")
            if response.lower() != 'y':
                print(f"[SKIP] Skipping {table_name}")
                return 0

        # Migrate each record
        migrated = 0
        failed = 0

        for record in local_records:
            try:
                # Build parameterized query
                placeholders = ', '.join(['?' for _ in columns])
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

                # Get values from record
                values = tuple(record[col] for col in columns)

                # Insert into production
                new_id = execute_insert(query, values, return_id=True)

                if new_id:
                    migrated += 1
                else:
                    failed += 1
                    print(f"[ERROR] Failed to insert record: {dict(record)}")

            except Exception as e:
                failed += 1
                print(f"[ERROR] Exception migrating record: {e}")
                print(f"        Record: {dict(record)}")

        print(f"\n[SUMMARY] {table_name}:")
        print(f"  - Local records: {len(local_records)}")
        print(f"  - Migrated: {migrated}")
        print(f"  - Failed: {failed}")

        return migrated

    finally:
        local_conn.close()


def verify_migration():
    """Verify all health data migrated correctly"""
    print(f"\n{'='*60}")
    print("VERIFICATION: Checking Production Database")
    print(f"{'='*60}")

    tables = {
        'sleep_logs': 30,
        'water_logs': 248,
        'exercise_logs': 15,
        'sauna_logs': 8,
        'inbody_measurements': 5
    }

    total_expected = sum(tables.values())
    total_actual = 0
    all_match = True

    for table, expected in tables.items():
        result = execute_query(f"SELECT COUNT(*) as count FROM {table}", fetch='one')
        actual = result['count'] if result else 0
        total_actual += actual

        status = "[OK]" if actual == expected else "[MISMATCH]"
        print(f"{status} {table}: {actual}/{expected} records")

        if actual != expected:
            all_match = False

    print(f"\n{'='*60}")
    print(f"TOTAL: {total_actual}/{total_expected} records")

    if all_match:
        print("[SUCCESS] All health data migrated successfully!")
    else:
        print("[WARNING] Some discrepancies found. Review above.")

    return all_match


def main():
    """Main migration function"""
    print("\n" + "="*60)
    print("HEALTH DATA MIGRATION: Local SQLite -> Production PostgreSQL")
    print("="*60)
    print(f"\nLocal Database: {LOCAL_DB}")
    print(f"Production Database: Render PostgreSQL")
    print(f"\nExpected Records:")
    print("  - Sleep logs: 30")
    print("  - Water logs: 248")
    print("  - Exercise logs: 15")
    print("  - Sauna logs: 8")
    print("  - InBody measurements: 5")
    print("  - TOTAL: 306 health records")

    # Confirm before proceeding
    print(f"\n{'='*60}")
    response = input("Proceed with migration? (y/n): ")
    if response.lower() != 'y':
        print("[CANCELLED] Migration aborted")
        return

    # Migrate each table
    total_migrated = 0

    # Sleep logs
    total_migrated += migrate_table('sleep_logs', [
        'date', 'hours', 'notes'
    ])

    # Water logs
    total_migrated += migrate_table('water_logs', [
        'date', 'cups'
    ])

    # Exercise logs
    total_migrated += migrate_table('exercise_logs', [
        'date', 'activity_type', 'duration_minutes', 'notes'
    ])

    # Sauna logs
    total_migrated += migrate_table('sauna_logs', [
        'date', 'duration_minutes', 'num_visits'
    ])

    # InBody measurements
    total_migrated += migrate_table('inbody_measurements', [
        'date', 'weight', 'smm', 'pbf', 'ecw_tbw_ratio', 'notes'
    ])

    # Final verification
    print(f"\n{'='*60}")
    print(f"MIGRATION COMPLETE: {total_migrated} records migrated")
    print(f"{'='*60}")

    # Verify counts
    verify_migration()


if __name__ == '__main__':
    main()
