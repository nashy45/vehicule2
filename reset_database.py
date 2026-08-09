"""
Database Reset Script
Run this to delete the old database and create a fresh one with all tables
"""
import os
from app import app, db

# Delete old database
db_path = 'instance/database.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted old database: {db_path}")

# Create fresh database with all tables
with app.app_context():
    db.create_all()
    print("Created fresh database with all tables!")
    print("Tables created: User, Vehicle, Inquiry, Review")
    
    # Create default admin user
    from werkzeug.security import generate_password_hash
    from app import User
    
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("\nDefault admin user created!")
        print("Username: admin")
        print("Password: admin123")
    
print("\nDatabase reset complete! You can now run: python app.py")
