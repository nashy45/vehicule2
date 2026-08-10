"""
Complete Database Fix - Recreates database from scratch
"""
import os
import shutil

print("=== Database Fix Script ===\n")

# Step 1: Backup old database
if os.path.exists('instance/database.db'):
    print("1. Backing up old database...")
    if not os.path.exists('backups'):
        os.makedirs('backups')
    import datetime
    backup_name = f"backups/database_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2('instance/database.db', backup_name)
    print(f"   Backup created: {backup_name}")
    
    # Delete old database
    os.remove('instance/database.db')
    print("   Old database deleted\n")

# Step 2: Create fresh database
print("2. Creating fresh database...")
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print("   All tables created successfully!")
    
    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("   Admin user created (username: admin, password: admin123)\n")

# Step 3: Verify tables
print("3. Verifying database structure...")
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"   Tables: {', '.join(tables)}")
    
    # Check each table structure
    for table in tables:
        columns = [col['name'] for col in inspector.get_columns(table)]
        print(f"   - {table}: {len(columns)} columns")

print("\n=== Fix Complete! ===")
print("You can now run: python app.py")
