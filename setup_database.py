"""
Database Setup Script
This script creates the database, tables, and adds sample data
Run this before starting the application for the first time
"""

from app import app, db, User, Vehicle, Inquiry
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def setup_database():
    """Create database, tables, and sample data"""
    
    with app.app_context():
        print("Creating database and tables...")
        
        # Drop all tables (if they exist) and recreate them
        db.drop_all()
        db.create_all()
        
        print("✅ Database and tables created!")
        
        # Create admin user
        print("\nCreating admin user...")
        admin = User(
            username='admin',
            email='admin@douala-vehicles.cm',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        print("✅ Admin user created (username: admin, password: admin123)")
        
        # Create sample vehicles
        print("\nAdding sample vehicles...")
        
        vehicles_data = [
            {
                'make': 'Toyota',
                'model': 'Camry',
                'year': 2020,
                'price': 8500000,
                'mileage': 45000,
                'condition': 'excellent',
                'fuel_type': 'gasoline',
                'transmission': 'automatic',
                'body_type': 'sedan',
                'vin': '4T1BF1FK5CU123456',
                'description': 'Well-maintained Toyota Camry with full service history. Bank repossessed vehicle in excellent condition. Features include automatic transmission, air conditioning, power windows, and more.',
                'status': 'available',
                'featured': True,
                'image_url': None
            },
            {
                'make': 'Honda',
                'model': 'CR-V',
                'year': 2019,
                'price': 12000000,
                'mileage': 60000,
                'condition': 'good',
                'fuel_type': 'gasoline',
                'transmission': 'automatic',
                'body_type': 'suv',
                'vin': '2HKRM4H76HH123789',
                'description': 'Spacious Honda CR-V SUV perfect for families. Bank repossessed with clean interior and exterior. Includes backup camera, cruise control, and alloy wheels.',
                'status': 'available',
                'featured': True,
                'image_url': None
            },
            {
                'make': 'Mercedes-Benz',
                'model': 'C-Class',
                'year': 2018,
                'price': 15000000,
                'mileage': 75000,
                'condition': 'excellent',
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'body_type': 'sedan',
                'vin': 'WDDWF8EB8JR123456',
                'description': 'Luxury Mercedes-Benz C-Class in pristine condition. Bank repossessed from corporate lease. Loaded with premium features including leather seats, navigation, and sunroof.',
                'status': 'available',
                'featured': True,
                'image_url': None
            },
            {
                'make': 'Nissan',
                'model': 'Patrol',
                'year': 2017,
                'price': 18000000,
                'mileage': 90000,
                'condition': 'good',
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'body_type': 'suv',
                'vin': '5N1AR2MM4EC123456',
                'description': 'Powerful Nissan Patrol 4x4 SUV. Bank repossessed, perfect for rough terrain. Features 7 seats, 4WD, and heavy-duty suspension.',
                'status': 'available',
                'featured': True,
                'image_url': None
            },
            {
                'make': 'Toyota',
                'model': 'Hilux',
                'year': 2021,
                'price': 16500000,
                'mileage': 30000,
                'condition': 'excellent',
                'fuel_type': 'diesel',
                'transmission': 'manual',
                'body_type': 'truck',
                'vin': '5TFDZ5BN0MX123456',
                'description': 'Nearly new Toyota Hilux pickup truck. Bank repossessed from business. Diesel engine, manual transmission, perfect for work or personal use.',
                'status': 'available',
                'featured': True,
                'image_url': None
            },
            {
                'make': 'Hyundai',
                'model': 'Elantra',
                'year': 2019,
                'price': 6500000,
                'mileage': 55000,
                'condition': 'good',
                'fuel_type': 'gasoline',
                'transmission': 'automatic',
                'body_type': 'sedan',
                'vin': 'KMHD84LF5KU123456',
                'description': 'Affordable Hyundai Elantra sedan with low mileage. Bank repossessed, great fuel economy. Perfect first car or city driving.',
                'status': 'available',
                'featured': True,
                'image_url': None
            },
            {
                'make': 'Ford',
                'model': 'Explorer',
                'year': 2018,
                'price': 13500000,
                'mileage': 70000,
                'condition': 'good',
                'fuel_type': 'gasoline',
                'transmission': 'automatic',
                'body_type': 'suv',
                'vin': '1FM5K8D88JG123456',
                'description': 'Spacious Ford Explorer with 3 rows of seating. Bank repossessed family SUV with great features and reliability.',
                'status': 'available',
                'featured': False,
                'image_url': None
            },
            {
                'make': 'Volkswagen',
                'model': 'Golf',
                'year': 2020,
                'price': 7500000,
                'mileage': 40000,
                'condition': 'excellent',
                'fuel_type': 'gasoline',
                'transmission': 'automatic',
                'body_type': 'hatchback',
                'vin': '3VWC57BU2LM123456',
                'description': 'Compact and efficient VW Golf hatchback. Bank repossessed, perfect condition. Great handling and fuel economy.',
                'status': 'available',
                'featured': False,
                'image_url': None
            },
            {
                'make': 'Mitsubishi',
                'model': 'Pajero',
                'year': 2016,
                'price': 11000000,
                'mileage': 95000,
                'condition': 'good',
                'fuel_type': 'diesel',
                'transmission': 'automatic',
                'body_type': 'suv',
                'vin': 'JA4MT31R46J123456',
                'description': 'Rugged Mitsubishi Pajero SUV with 4WD capability. Bank repossessed, mechanically sound. Perfect for adventure seekers.',
                'status': 'available',
                'featured': False,
                'image_url': None
            },
            {
                'make': 'Kia',
                'model': 'Sportage',
                'year': 2019,
                'price': 9500000,
                'mileage': 50000,
                'condition': 'excellent',
                'fuel_type': 'gasoline',
                'transmission': 'automatic',
                'body_type': 'suv',
                'vin': 'KNDPM3AC8K7123456',
                'description': 'Modern Kia Sportage crossover SUV. Bank repossessed with warranty remaining. Stylish design with advanced safety features.',
                'status': 'reserved',
                'featured': False,
                'image_url': None
            }
        ]
        
        for vehicle_data in vehicles_data:
            vehicle = Vehicle(**vehicle_data)
            db.session.add(vehicle)
        
        print(f"✅ Added {len(vehicles_data)} sample vehicles")
        
        # Create sample inquiries
        print("\nAdding sample inquiries...")
        
        inquiries_data = [
            {
                'vehicle_id': 1,
                'name': 'Jean Dupont',
                'phone': '+237 650 123 456',
                'email': 'jean.dupont@email.cm',
                'inquiry_type': 'contact_form',
                'message': 'I am interested in the Toyota Camry. Is it still available? Can I schedule a test drive?',
                'is_contacted': False,
                'created_at': datetime.now() - timedelta(hours=2)
            },
            {
                'vehicle_id': 2,
                'name': 'Marie Nkoa',
                'phone': '+237 677 234 567',
                'email': 'marie.nkoa@email.cm',
                'inquiry_type': 'whatsapp',
                'message': 'Hello, I would like more information about the Honda CR-V. What is the financing option?',
                'is_contacted': True,
                'contacted_at': datetime.now() - timedelta(hours=1),
                'created_at': datetime.now() - timedelta(days=1)
            },
            {
                'vehicle_id': 3,
                'name': 'Paul Kamga',
                'phone': '+237 699 345 678',
                'email': None,
                'inquiry_type': 'phone_call',
                'message': None,
                'is_contacted': False,
                'created_at': datetime.now() - timedelta(hours=5)
            },
            {
                'vehicle_id': None,
                'name': 'Sophie Mbarga',
                'phone': '+237 655 456 789',
                'email': 'sophie.m@email.cm',
                'inquiry_type': 'contact_form',
                'message': 'Do you have any SUVs under 10 million XAF? I am looking for a family vehicle.',
                'is_contacted': False,
                'created_at': datetime.now() - timedelta(days=2)
            },
            {
                'vehicle_id': 5,
                'name': 'Alain Fotso',
                'phone': '+237 670 567 890',
                'email': 'alain.fotso@email.cm',
                'inquiry_type': 'test_drive',
                'message': 'I want to schedule a test drive for the Toyota Hilux this weekend. Saturday morning would be perfect.',
                'is_contacted': True,
                'contacted_at': datetime.now() - timedelta(hours=12),
                'created_at': datetime.now() - timedelta(days=3)
            }
        ]
        
        for inquiry_data in inquiries_data:
            inquiry = Inquiry(**inquiry_data)
            db.session.add(inquiry)
        
        print(f"✅ Added {len(inquiries_data)} sample inquiries")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "="*50)
        print("✅ DATABASE SETUP COMPLETE!")
        print("="*50)
        print("\nDatabase file: database.db")
        print("\nAdmin Credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nSample Data Added:")
        print(f"  - {len(vehicles_data)} vehicles")
        print(f"  - {len(inquiries_data)} inquiries")
        print("\nYou can now run: python app.py")
        print("Or simply run: start.bat")
        print("\nAccess the website at: http://127.0.0.1:5000")
        print("Access admin panel at: http://127.0.0.1:5000/admin/login")
        print("="*50)

if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"\n❌ Error setting up database: {str(e)}")
        print("\nMake sure you have installed all requirements:")
        print("  pip install -r requirements.txt")
