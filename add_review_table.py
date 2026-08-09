"""
Add Review table to existing database without deleting data
"""
from app import app, db
from sqlalchemy import text

with app.app_context():
    # Check if review table exists
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("Current tables:", tables)
    
    if 'review' not in tables:
        print("\nReview table missing. Creating it now...")
        
        # Create review table directly with SQL
        db.engine.execute(text("""
            CREATE TABLE review (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                vehicle_id INTEGER,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(120),
                rating INTEGER NOT NULL,
                comment TEXT,
                is_approved BOOLEAN NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(vehicle_id) REFERENCES vehicle (id)
            )
        """))
        
        print("Review table created successfully!")
    else:
        print("\nReview table already exists!")
    
    print("\nAll tables now:", db.inspect(db.engine).get_table_names())
    print("\nYou can now run: python app.py")
