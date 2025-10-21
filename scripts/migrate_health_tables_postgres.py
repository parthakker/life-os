"""
Migration Script: Create Health Tracking Tables (PostgreSQL Compatible)
Creates tables for sleep, water, exercise, sauna, and InBody measurements
Does NOT populate dummy data (for production use)
"""

from db_helper import get_db_connection

def create_health_tables():
    """Create health tracking tables"""

    print("=" * 60)
    print("HEALTH TABLES MIGRATION (PostgreSQL)")
    print("=" * 60)

    conn, cursor, db_type = get_db_connection()

    if db_type != 'postgres':
        print(f"\n[WARNING] This script is for PostgreSQL, but detected: {db_type}")
        print("Use migrate_health_tables.py for SQLite instead")
        conn.close()
        return

    # Sleep logs table
    print("\n[1/5] Creating sleep_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleep_logs (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL UNIQUE,
            hours REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Water logs table
    print("[2/5] Creating water_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_logs (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL,
            cups INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Exercise logs table
    print("[3/5] Creating exercise_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sauna logs table
    print("[4/5] Creating sauna_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sauna_logs (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL UNIQUE,
            num_visits INTEGER NOT NULL DEFAULT 1,
            duration_minutes INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # InBody measurements table
    print("[5/5] Creating inbody_measurements table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inbody_measurements (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL UNIQUE,
            weight REAL NOT NULL,
            smm REAL NOT NULL,
            pbf REAL NOT NULL,
            ecw_tbw_ratio REAL NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("\n-> All tables created successfully!")
    print("=" * 60)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nNote: No dummy data generated for production.")
    print("Use Telegram bot or API to log health data.")

    conn.close()


if __name__ == "__main__":
    create_health_tables()
