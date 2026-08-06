# Database Information 🗄️

## Overview

This application uses **SQLite**, a lightweight database that stores everything in a single file called `database.db`. No separate database server is required!

## Database File

**Location**: `c:\Users\fombu\OneDrive\Desktop\vehicules\database.db`

**Size**: ~50 KB (empty) to several MB (with many vehicles)

**Format**: SQLite 3

## Setup Options

### Option 1: Automatic Setup (Recommended)
Just run `start.bat` and the database will be created automatically on first run with sample data.

### Option 2: Manual Setup
Run `setup_db.bat` to create the database separately before starting the application.

### Option 3: Custom Setup
```cmd
python setup_database.py
```

## Database Schema

### 1. User Table
Stores admin accounts for the management panel.

**Columns**:
- `id` - Primary key (auto-increment)
- `username` - Unique username for login
- `email` - User email address
- `password` - Hashed password (PBKDF2)
- `is_admin` - Boolean (always True for now)
- `created_at` - Account creation timestamp

**Default Data**:
```
Username: admin
Email: admin@douala-vehicles.cm
Password: admin123 (hashed)
```

### 2. Vehicle Table
Stores all vehicle inventory information.

**Columns**:
- `id` - Primary key (auto-increment)
- `make` - Vehicle manufacturer (e.g., Toyota)
- `model` - Vehicle model (e.g., Camry)
- `year` - Manufacturing year (1990-2026)
- `price` - Price in XAF (float)
- `mileage` - Kilometers driven (integer)
- `condition` - excellent, good, or fair
- `fuel_type` - gasoline, diesel, electric, or hybrid
- `transmission` - automatic or manual
- `body_type` - sedan, suv, truck, van, coupe, hatchback, or wagon
- `vin` - Vehicle Identification Number (17 chars, unique)
- `description` - Text description of the vehicle
- `status` - available, reserved, or sold
- `featured` - Boolean (show on homepage?)
- `image_url` - Filename of uploaded image
- `created_at` - Record creation timestamp
- `updated_at` - Last update timestamp

**Sample Data**: 10 vehicles including:
- Toyota Camry 2020 (8.5M XAF)
- Honda CR-V 2019 (12M XAF)
- Mercedes-Benz C-Class 2018 (15M XAF)
- Nissan Patrol 2017 (18M XAF)
- Toyota Hilux 2021 (16.5M XAF)
- Hyundai Elantra 2019 (6.5M XAF)
- And 4 more...

### 3. Inquiry Table
Stores customer contact requests and inquiries.

**Columns**:
- `id` - Primary key (auto-increment)
- `vehicle_id` - Foreign key to vehicle table (optional)
- `name` - Customer name
- `phone` - Customer phone number (+237 format)
- `email` - Customer email (optional)
- `inquiry_type` - whatsapp, contact_form, phone_call, or test_drive
- `message` - Customer message text (optional)
- `is_contacted` - Boolean (has admin contacted them?)
- `contacted_at` - Timestamp when marked as contacted
- `notes` - Admin notes (for future use)
- `created_at` - Inquiry creation timestamp

**Sample Data**: 5 inquiries with various types and statuses

## Sample Data Details

### 10 Sample Vehicles

1. **Toyota Camry 2020** - 8,500,000 XAF (Featured, Excellent)
2. **Honda CR-V 2019** - 12,000,000 XAF (Featured, Good)
3. **Mercedes-Benz C-Class 2018** - 15,000,000 XAF (Featured, Excellent)
4. **Nissan Patrol 2017** - 18,000,000 XAF (Featured, Good)
5. **Toyota Hilux 2021** - 16,500,000 XAF (Featured, Excellent)
6. **Hyundai Elantra 2019** - 6,500,000 XAF (Featured, Good)
7. **Ford Explorer 2018** - 13,500,000 XAF (Good)
8. **Volkswagen Golf 2020** - 7,500,000 XAF (Excellent)
9. **Mitsubishi Pajero 2016** - 11,000,000 XAF (Good)
10. **Kia Sportage 2019** - 9,500,000 XAF (Reserved, Excellent)

### 5 Sample Inquiries

1. Jean Dupont - Interested in Toyota Camry (Pending)
2. Marie Nkoa - Question about Honda CR-V (Contacted)
3. Paul Kamga - Phone call about Mercedes (Pending)
4. Sophie Mbarga - General inquiry about SUVs (Pending)
5. Alain Fotso - Test drive request for Hilux (Contacted)

## Database Operations

### View Database
You can view and edit the database using:
- **DB Browser for SQLite** (Free): https://sqlitebrowser.org/
- **SQLite Studio** (Free): https://sqlitestudio.pl/
- Or any SQLite-compatible tool

### Backup Database

**Manual Backup**:
```cmd
copy database.db database_backup.db
```

**Scheduled Backup** (Windows Task Scheduler):
1. Create a .bat file:
   ```batch
   copy "C:\Users\fombu\OneDrive\Desktop\vehicules\database.db" "C:\Backups\vehicules_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db"
   ```
2. Schedule it to run daily

### Restore Database

1. Stop the application (Ctrl+C or close terminal)
2. Replace `database.db` with your backup:
   ```cmd
   copy database_backup.db database.db
   ```
3. Restart the application

### Reset Database

**Warning**: This deletes ALL data!

```cmd
del database.db
python setup_database.py
```

Or simply:
```cmd
setup_db.bat
```

### Export Data

**To CSV** (using DB Browser):
1. Open `database.db` in DB Browser
2. File → Export → Table to CSV
3. Select table and export

**To SQL**:
```cmd
sqlite3 database.db .dump > backup.sql
```

### Import Data

**From SQL file**:
```cmd
sqlite3 database.db < backup.sql
```

## Database Maintenance

### Check Database Size
```cmd
dir database.db
```

### Optimize Database
```python
import sqlite3
conn = sqlite3.connect('database.db')
conn.execute('VACUUM')
conn.close()
```

### Check Integrity
```cmd
sqlite3 database.db "PRAGMA integrity_check;"
```

## Common Queries

### Count Vehicles
```sql
SELECT COUNT(*) FROM vehicle;
```

### Count Available Vehicles
```sql
SELECT COUNT(*) FROM vehicle WHERE status = 'available';
```

### Total Inventory Value
```sql
SELECT SUM(price) FROM vehicle WHERE status = 'available';
```

### Pending Inquiries
```sql
SELECT COUNT(*) FROM inquiry WHERE is_contacted = 0;
```

### Featured Vehicles
```sql
SELECT make, model, year, price FROM vehicle WHERE featured = 1;
```

## Database Security

### Change Admin Password

**Method 1**: Through admin panel (after we add this feature)

**Method 2**: Using Python:
```python
from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.password = generate_password_hash('new_password_here')
    db.session.commit()
    print("Password changed!")
```

**Method 3**: Using SQLite directly (advanced):
```python
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('new_password'))"
# Copy the hash, then:
sqlite3 database.db "UPDATE user SET password = 'PASTE_HASH_HERE' WHERE username = 'admin';"
```

### Backup Recommendations

- **Daily**: Automatic backup before making changes
- **Weekly**: Full backup to external drive
- **Monthly**: Cloud backup (Google Drive, Dropbox, etc.)

### Database Permissions

On Windows, set file permissions:
1. Right-click `database.db`
2. Properties → Security
3. Restrict access to admin users only

## Migration to Production Database

If you want to move to PostgreSQL or MySQL later:

### Using Flask-Migrate
```cmd
pip install Flask-Migrate
```

Then create migration scripts to transfer data.

### Manual Export/Import
1. Export data from SQLite to CSV
2. Import CSV into PostgreSQL/MySQL
3. Update `app.py` connection string

## Troubleshooting

### "Database is locked"
- Close any SQLite browser/editor
- Restart the Flask application
- Check for multiple running instances

### "No such table"
- Database not created properly
- Run `setup_database.py` again
- Check for errors during creation

### "Disk I/O error"
- Check disk space
- Check file permissions
- Run disk check (chkdsk)

### Lost Admin Password
```python
python setup_database.py
# This recreates the default admin user
```

## Performance Tips

- SQLite handles 100s of vehicles easily
- For 1000s of vehicles, consider PostgreSQL
- Index important columns (already done)
- Regular VACUUM for optimization
- Backup before bulk operations

## Support

For database issues:
- Check error messages in terminal
- Verify file permissions
- Ensure disk space available
- Review DATABASE_INFO.md (this file)

---

**Your data is safe in database.db - just remember to back it up regularly!** 📦
