# Quick Start Guide 🚀

Welcome to Douala Vehicle Dealership! Follow these simple steps to get started.

## Step 1: Install Python

If you don't have Python installed:
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. During installation, CHECK "Add Python to PATH"
4. Complete installation

## Step 2: Setup Database (First Time Only)

### Option A: Automatic Setup (Recommended)
The database will be created automatically when you run `start.bat` for the first time. It includes:
- ✅ Admin user (admin/admin123)
- ✅ 10 sample vehicles
- ✅ 5 sample inquiries

### Option B: Manual Database Setup
If you want to setup the database separately:
1. Double-click `setup_db.bat`
2. Or run in Command Prompt:
   ```cmd
   setup_db.bat
   ```

## Step 3: Start the Application

### Option A: Double-Click Method (Easiest)
1. Find `start.bat` in the project folder
2. Double-click it
3. Wait for it to install dependencies (first time only)
4. Database will be created automatically if it doesn't exist
5. The application will start automatically

### Option B: Command Line Method
1. Open Command Prompt
2. Navigate to the project folder:
   ```cmd
   cd C:\Users\fombu\OneDrive\Desktop\vehicules
   ```
3. Run the start script:
   ```cmd
   start.bat
   ```

## Step 4: Access the Website

Once the server is running, open your web browser and go to:

- **Public Website**: http://127.0.0.1:5000
- **Admin Panel**: http://127.0.0.1:5000/admin/login

## Step 5: Login to Admin Panel

Use these default credentials:
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change these credentials after your first login!

## Step 6: Explore Sample Data

When you first login, you'll see:
- 📊 10 sample vehicles already in the system
- 📧 5 sample customer inquiries
- 📈 Statistics on the dashboard

This sample data helps you understand how the system works. You can:
- Edit the sample vehicles
- Delete them and add your own
- Practice with the inquiry management

## Step 7: Add Your Own Vehicles

1. After logging in, you'll be on the Dashboard
2. Click "Add Vehicle" in the sidebar
3. Fill in all the vehicle information:
   - Make (e.g., Toyota)
   - Model (e.g., Camry)
   - Year (e.g., 2020)
   - Price in XAF (e.g., 5000000)
   - Mileage in km (e.g., 50000)
   - VIN (17 characters)
   - Select Condition, Fuel Type, Transmission, Body Type
4. Upload a vehicle image (JPEG, PNG, GIF, WebP)
5. Optionally check "Featured" to show on homepage
6. Click "Add Vehicle"

## Step 8: View Your Website

1. Click "View Website" in the admin sidebar
2. Or go directly to http://127.0.0.1:5000
3. Your vehicle should appear on the homepage (if featured) or in Inventory

## Database Information

### What's in the Database?

When you run the setup, the database (`database.db`) is created with:

**Tables**:
- `user` - Admin accounts
- `vehicle` - Vehicle inventory
- `inquiry` - Customer inquiries

**Sample Data**:
- 1 admin user (username: admin, password: admin123)
- 10 sample vehicles (various makes and models)
- 5 sample inquiries (some contacted, some pending)

### Reset Database

If you want to start fresh and delete all data:

1. **Stop the application** (Close the command prompt or press Ctrl+C)
2. **Delete the database file**: `database.db`
3. **Run setup again**: Double-click `setup_db.bat`
4. **Or let start.bat create it**: Just run `start.bat` and it will recreate the database

### Backup Database

To backup your data:
1. **Copy `database.db`** to a safe location
2. **Name it** something like `database_backup_2024-01-15.db`
3. **Store it** on a USB drive or cloud storage

To restore from backup:
1. **Stop the application**
2. **Replace `database.db`** with your backup file
3. **Restart the application**

## Common Tasks

### Stopping the Server
- Press `Ctrl + C` in the Command Prompt window
- Or simply close the Command Prompt window

### Restarting the Server
- Just run `start.bat` again
- All your data is saved in `database.db`

### Viewing All Vehicles
- Admin: Click "Vehicles" in sidebar
- Public: Go to "Inventory" page

### Managing Inquiries
- Admin: Click "Inquiries" in sidebar
- See all customer contact requests
- Mark inquiries as contacted

## Troubleshooting

### Python Not Found
- Make sure Python is installed
- Verify Python is in your PATH (reinstall and check "Add to PATH")
- Open a new Command Prompt after installing Python

### Port 5000 Already in Use
- Another application is using port 5000
- Close other applications or restart your computer

### Can't Access Website
- Make sure the server is running (Command Prompt window is open)
- Check for error messages in the Command Prompt
- Try using `http://localhost:5000` instead of `http://127.0.0.1:5000`

### Images Not Uploading
- Check file size (max 16MB)
- Only JPEG, PNG, GIF, WebP formats supported
- Make sure `static/images/uploads/` folder exists

## Next Steps

### Customize Your Website
1. Update contact information in templates
2. Change company name and branding
3. Update colors in `static/css/style.css`
4. Add your logo

### Add More Content
1. Add all your vehicles
2. Update the About page with your story
3. Add proper contact details (phone, email, address)
4. Update WhatsApp numbers in contact buttons

### Security (Important!)
1. Change admin password immediately
2. Change SECRET_KEY in `app.py` before going live
3. Use HTTPS when deploying to production

## Need Help?

- Read the full `README.md` for detailed documentation
- Check error messages in the Command Prompt
- Ensure all requirements are installed properly

## File Structure

```
vehicules/
├── app.py              - Main application (Don't modify unless you know Python/Flask)
├── database.db         - Your data (backup regularly!)
├── start.bat           - Quick start script
├── requirements.txt    - Python dependencies
├── README.md           - Full documentation
├── QUICKSTART.md       - This file
│
├── static/             - CSS, JS, Images
│   ├── css/style.css  - Customize colors here
│   ├── js/            - JavaScript files
│   └── images/uploads/ - Vehicle images go here
│
└── templates/          - HTML pages
    ├── *.html         - Public pages (customize these)
    └── admin/*.html   - Admin pages
```

## Support

For help, contact: admin@douala-vehicles.cm

---

**You're all set! Start adding vehicles and customizing your website!** 🎉
