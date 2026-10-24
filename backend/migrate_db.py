import sqlite3
import os
import datetime

def migrate_database():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "database", "safebite.db")
    
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 1. Inspect existing columns in restaurants
    cur.execute("PRAGMA table_info(restaurants)")
    existing_cols = {col[1] for col in cur.fetchall()}
    print(f"Existing restaurant columns: {len(existing_cols)}")
    
    new_columns = [
        ("source_name", "VARCHAR DEFAULT 'SafeBite Synthetic Benchmark'"),
        ("source_url", "VARCHAR DEFAULT 'https://safebite.demo/datasets/benchmark-v1'"),
        ("source_record_id", "VARCHAR"),
        ("last_synced_at", "DATETIME"),
        ("verification_status", "VARCHAR DEFAULT 'Synthetic Demonstration'"),
        ("confidence_score", "FLOAT DEFAULT 0.75"),
        ("is_synthetic", "BOOLEAN DEFAULT 1"),
        ("data_freshness_status", "VARCHAR DEFAULT 'Current'"),
    ]
    
    for col_name, col_def in new_columns:
        if col_name not in existing_cols:
            print(f"Adding column '{col_name}' to restaurants...")
            cur.execute(f"ALTER TABLE restaurants ADD COLUMN {col_name} {col_def}")
        else:
            print(f"Column '{col_name}' already exists.")
            
    # Also for inspections: add provenance columns if not present
    cur.execute("PRAGMA table_info(inspections)")
    existing_insp_cols = {col[1] for col in cur.fetchall()}
    insp_new_cols = [
        ("source_name", "VARCHAR DEFAULT 'SafeBite Synthetic Benchmark'"),
        ("source_record_id", "VARCHAR"),
        ("verification_status", "VARCHAR DEFAULT 'Synthetic Demonstration'"),
        ("is_synthetic", "BOOLEAN DEFAULT 1")
    ]
    for col_name, col_def in insp_new_cols:
        if col_name not in existing_insp_cols:
            print(f"Adding column '{col_name}' to inspections...")
            cur.execute(f"ALTER TABLE inspections ADD COLUMN {col_name} {col_def}")
            
    # 2. Create correction_requests table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS correction_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id VARCHAR NOT NULL,
        inspection_id INTEGER,
        owner_id INTEGER NOT NULL,
        request_type VARCHAR NOT NULL,
        details TEXT NOT NULL,
        evidence_url VARCHAR,
        status VARCHAR DEFAULT 'Pending',
        admin_notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        reviewed_at DATETIME,
        FOREIGN KEY (restaurant_id) REFERENCES restaurants (id),
        FOREIGN KEY (inspection_id) REFERENCES inspections (id),
        FOREIGN KEY (owner_id) REFERENCES users (id)
    )
    """)
    print("Table 'correction_requests' created or confirmed.")
    
    # 3. Update existing synthetic restaurants explicitly so provenance is transparent
    cur.execute("""
    UPDATE restaurants 
    SET is_synthetic = 1,
        verification_status = 'Synthetic Demonstration',
        source_name = 'SafeBite Synthetic Benchmark',
        source_url = 'https://safebite.demo/datasets/benchmark-v1',
        source_record_id = id,
        confidence_score = 0.70,
        last_synced_at = CURRENT_TIMESTAMP
    WHERE is_synthetic IS NULL OR is_synthetic = 1
    """)
    
    cur.execute("""
    UPDATE inspections 
    SET is_synthetic = 1,
        verification_status = 'Synthetic Demonstration',
        source_name = 'SafeBite Synthetic Benchmark',
        source_record_id = CAST(id AS TEXT)
    WHERE is_synthetic IS NULL OR is_synthetic = 1
    """)
    
    conn.commit()
    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_database()
