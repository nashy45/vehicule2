"""
Check what's actually in the database
"""
import sqlite3

db_path = 'instance/database.db'
print(f"Checking database: {db_path}\n")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in database:")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Get column info for each table
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print(f"    Columns: {[col[1] for col in columns]}\n")
    
    conn.close()
    
    if not tables:
        print("ERROR: Database is empty! No tables found.")
        print("\nRun: python fix_database.py")
    else:
        print("Database structure looks good!")
        
except Exception as e:
    print(f"ERROR: {e}")
    print("\nDatabase file might be corrupted or locked.")
