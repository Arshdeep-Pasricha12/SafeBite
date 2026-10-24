import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'safebite.db')
print(f"DB Path: {db_path}")
print(f"DB Exists: {os.path.exists(db_path)}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cursor.fetchall()]
print(f"\nTables found: {tables}")

# Count rows in each table
for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM [{t}]")
    count = cursor.fetchone()[0]
    print(f"  {t}: {count} rows")

# Sample data from key tables
print("\n--- Sample Users ---")
cursor.execute("SELECT id, email, role, full_name FROM users LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n--- Sample Restaurants (first 5) ---")
cursor.execute("SELECT id, name, city, cuisine, safety_score, safety_rating, approval_status, license_number FROM restaurants LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n--- Sample Inspections (first 5) ---")
cursor.execute("SELECT id, restaurant_id, inspection_date, total_score, pass_fail_status, risk_level FROM inspections LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n--- Sample Violations (first 5) ---")
cursor.execute("SELECT id, inspection_id, severity_level, description FROM violations LIMIT 5")
for row in cursor.fetchall():
    print(f"  id={row[0]}, inspection_id={row[1]}, severity={row[2]}, desc={row[3][:80]}")

print("\n--- Sample Violation Codes (first 5) ---")
cursor.execute("SELECT id, code, category, severity, description FROM violation_codes LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n--- Sample Inspectors (first 5) ---")
cursor.execute("SELECT id, name, badge_number, certification_level FROM inspectors LIMIT 5")
for row in cursor.fetchall():
    print(f"  {row}")

print("\n--- Distinct Cities ---")
cursor.execute("SELECT DISTINCT city FROM restaurants ORDER BY city LIMIT 20")
for row in cursor.fetchall():
    print(f"  {row[0]}")

print("\n--- Distinct Cuisines ---")
cursor.execute("SELECT DISTINCT cuisine FROM restaurants ORDER BY cuisine LIMIT 20")
for row in cursor.fetchall():
    print(f"  {row[0]}")

print("\n--- Approval Status Distribution ---")
cursor.execute("SELECT approval_status, COUNT(*) FROM restaurants GROUP BY approval_status")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
