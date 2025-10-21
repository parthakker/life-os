"""
Migration Script: Create Health Tracking Tables
Creates tables for sleep, water, exercise, sauna, and InBody measurements
Populates with 30 days of dummy data
"""

from db_helper import execute_query, get_db_connection
from datetime import datetime, timedelta
import random

def create_health_tables():
    """Create health tracking tables"""

    print("=" * 60)
    print("HEALTH TABLES MIGRATION")
    print("=" * 60)

    conn, cursor, db_type = get_db_connection()

    # Sleep logs table
    print("\n[1/5] Creating sleep_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sleep_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            hours REAL NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Water logs table
    print("[2/5] Creating water_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            cups INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Exercise logs table
    print("[3/5] Creating exercise_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercise_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sauna logs table
    print("[4/5] Creating sauna_logs table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sauna_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            num_visits INTEGER NOT NULL DEFAULT 1,
            duration_minutes INTEGER NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # InBody measurements table
    print("[5/5] Creating inbody_measurements table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inbody_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            weight REAL NOT NULL,
            smm REAL NOT NULL,
            pbf REAL NOT NULL,
            ecw_tbw_ratio REAL NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    print("\n-> All tables created successfully!")

    return conn, cursor


def generate_dummy_data(conn, cursor):
    """Generate 30 days of realistic dummy data"""

    print("\n" + "=" * 60)
    print("GENERATING DUMMY DATA (30 DAYS)")
    print("=" * 60)

    today = datetime.now().date()

    # Sleep data: 7-8.5 hours per night
    print("\n[1/5] Generating sleep data...")
    for i in range(30):
        date = (today - timedelta(days=i)).isoformat()
        hours = round(random.uniform(6.5, 8.5), 1)
        cursor.execute(
            "INSERT OR REPLACE INTO sleep_logs (date, hours) VALUES (?, ?)",
            (date, hours)
        )
    print(f"  -> Added 30 days of sleep logs (6.5-8.5 hrs/night)")

    # Water data: 6-10 cups per day (multiple entries throughout day)
    print("[2/5] Generating water data...")
    water_count = 0
    for i in range(30):
        date = (today - timedelta(days=i)).isoformat()
        daily_cups = random.randint(6, 10)
        # Spread throughout the day
        for cup in range(daily_cups):
            hour = random.randint(7, 22)
            minute = random.randint(0, 59)
            timestamp = f"{date}T{hour:02d}:{minute:02d}:00"
            cursor.execute(
                "INSERT INTO water_logs (date, cups, timestamp) VALUES (?, 1, ?)",
                (date, timestamp)
            )
            water_count += 1
    print(f"  -> Added {water_count} water log entries (6-10 cups/day)")

    # Exercise data: 3-4x per week, various activities
    print("[3/5] Generating exercise data...")
    activities = ["Pickleball", "Gym", "BJJ", "Yoga", "Running"]
    exercise_count = 0
    for i in range(30):
        date = (today - timedelta(days=i)).isoformat()
        # 50% chance of exercise (3-4x/week)
        if random.random() < 0.5:
            activity = random.choice(activities)
            duration = random.randint(30, 90)
            cursor.execute(
                "INSERT INTO exercise_logs (date, activity_type, duration_minutes) VALUES (?, ?, ?)",
                (date, activity, duration)
            )
            exercise_count += 1
    print(f"  -> Added {exercise_count} exercise logs (3-4x/week)")

    # Sauna data: 2x per week
    print("[4/5] Generating sauna data...")
    sauna_count = 0
    for i in range(30):
        date = (today - timedelta(days=i)).isoformat()
        # 28% chance of sauna (~2x/week)
        if random.random() < 0.28:
            duration = random.randint(15, 30)
            cursor.execute(
                "INSERT OR REPLACE INTO sauna_logs (date, num_visits, duration_minutes) VALUES (?, 1, ?)",
                (date, duration)
            )
            sauna_count += 1
    print(f"  -> Added {sauna_count} sauna sessions (2x/week)")

    # InBody data: Weekly measurements showing weight gain 170 -> 174 lbs
    print("[5/5] Generating InBody measurements...")
    inbody_count = 0
    for week in range(5):  # 5 weekly measurements
        days_ago = week * 7
        date = (today - timedelta(days=days_ago)).isoformat()

        # Weight trend: 170 -> 174 (gradual increase)
        weight = 170 + (week * 1.0)  # +1 lb per week

        # SMM trend: slight increase with weight gain
        smm = 82 + (week * 0.3)

        # PBF trend: slight increase (gaining some fat)
        pbf = 14.5 + (week * 0.2)

        # ECW/TBW ratio: relatively stable
        ecw_tbw = round(random.uniform(0.38, 0.40), 3)

        cursor.execute(
            """INSERT OR REPLACE INTO inbody_measurements
               (date, weight, smm, pbf, ecw_tbw_ratio)
               VALUES (?, ?, ?, ?, ?)""",
            (date, round(weight, 1), round(smm, 1), round(pbf, 1), ecw_tbw)
        )
        inbody_count += 1

    print(f"  -> Added {inbody_count} InBody measurements (weekly)")
    print(f"  -> Weight trend: 170.0 lbs -> 174.0 lbs (gained weight)")

    conn.commit()


def verify_data(conn):
    """Verify data was inserted correctly"""

    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    cursor = conn.cursor()

    tables = [
        ('sleep_logs', 'Sleep'),
        ('water_logs', 'Water'),
        ('exercise_logs', 'Exercise'),
        ('sauna_logs', 'Sauna'),
        ('inbody_measurements', 'InBody')
    ]

    for table, name in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {name:12s}: {count:3d} entries")

    # Show latest InBody measurement
    cursor.execute("""
        SELECT date, weight, smm, pbf, ecw_tbw_ratio
        FROM inbody_measurements
        ORDER BY date DESC LIMIT 1
    """)
    latest = cursor.fetchone()
    if latest:
        print(f"\n  Latest InBody ({latest[0]}):")
        print(f"    Weight:    {latest[1]} lbs")
        print(f"    SMM:       {latest[2]} lbs")
        print(f"    PBF:       {latest[3]}%")
        print(f"    ECW/TBW:   {latest[4]}")

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)


def main():
    """Main migration function"""
    conn, cursor = create_health_tables()
    generate_dummy_data(conn, cursor)
    verify_data(conn)
    conn.close()


if __name__ == "__main__":
    main()
