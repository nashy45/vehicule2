# Douala Vehicle Dealership 🚗

A complete vehicle dealership website built with Flask, Bootstrap, and SQLite. This application allows you to manage and display bank-repossessed vehicles for sale in Douala, Cameroon.

## ✨ Features

### Public Website
- **Homepage**: Eye-catching hero section with featured vehicles showcase
- **Inventory Page**: Browse all available vehicles with advanced filters (make, condition, fuel type, transmission)
- **Vehicle Detail Page**: Comprehensive vehicle information with inquiry options
- **Contact Page**: Multiple contact methods (WhatsApp, phone, contact form)
- **About Page**: Company story, values, and why choose us
- **Responsive Design**: Mobile-first design that works on all devices
- **XAF Currency**: Localized for Cameroon market

### Admin Panel
- **Dashboard**: Real-time stats (total vehicles, available, sold, inquiries)
- **Vehicle Management**: Full CRUD operations with image upload
- **Inquiry Management**: Track and manage customer inquiries
- **Secure Authentication**: Session-based login system
- **Image Upload**: Support for JPEG, PNG, GIF, WebP (max 16MB)
- **Clean Interface**: Bootstrap-powered responsive admin UI

## 🛠️ Tech Stack

- **Backend**: Python 3.x + Flask 3.x
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5.3
- **Database**: SQLite 3
- **Icons**: Font Awesome 6.4
- **Image Handling**: Werkzeug secure filename

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

## 🚀 Installation & Setup

### Quick Start (Windows)

**Option 1: Using start.bat (Recommended)**

1. Navigate to the project folder
2. Double-click `start.bat` or run in Command Prompt:
   ```cmd
   start.bat
   ```

The script automatically:
- ✅ Checks Python installation
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Starts the Flask server
- ✅ Creates default admin user

**Option 2: Manual Installation**

1. **Create a virtual environment**:
   ```cmd
   python -m venv venv
   ```

2. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```cmd
   python app.py
   ```

5. **Access the application**:
   - 🌐 Public website: `http://127.0.0.1:5000`
   - 🔐 Admin panel: `http://127.0.0.1:5000/admin/login`

## 🔐 Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

**⚠️ IMPORTANT**: Change these credentials in production!

## 📁 Project Structure

```
vehicules/
├── app.py                      # Main Flask application with routes and models
├── requirements.txt            # Python dependencies
├── start.bat                   # Windows quick start script
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── database.db                 # SQLite database (auto-created)
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Custom styles (admin + public)
│   ├── js/
│   │   ├── main.js            # Public site JavaScript
│   │   └── admin.js           # Admin panel JavaScript
│   └── images/
│       └── uploads/           # Vehicle image uploads (max 16MB)
│           └── .gitkeep       # Keeps folder in git
│
└── templates/                  # Jinja2 templates
    ├── base.html              # Public site base template
    ├── index.html             # Homepage with hero & featured vehicles
    ├── inventory.html         # Vehicle listing with filters
    ├── vehicle_detail.html    # Single vehicle details
    ├── contact.html           # Contact form page
    ├── about.html             # About us page
    │
    └── admin/                 # Admin panel templates
        ├── base.html          # Admin base with sidebar
        ├── login.html         # Admin login page
        ├── dashboard.html     # Admin dashboard with stats
        ├── vehicles.html      # Vehicle list management
        ├── add_vehicle.html   # Add new vehicle form
        ├── edit_vehicle.html  # Edit vehicle form
        └── inquiries.html     # Customer inquiry management
```

## 📊 Database Models

### User
- **Fields**: id, username, email, password (hashed), is_admin, created_at
- **Purpose**: Admin authentication

### Vehicle
- **Fields**: id, make, model, year, price, mileage, condition, fuel_type
- **Additional**: transmission, body_type, vin, description, status, featured, image_url
- **Timestamps**: created_at, updated_at
- **Status**: available, reserved, sold
- **Relations**: One-to-many with Inquiry

### Inquiry
- **Fields**: id, vehicle_id (FK), name, phone, email, inquiry_type, message
- **Tracking**: is_contacted, contacted_at, notes, created_at
- **Types**: whatsapp, contact_form, phone_call, test_drive

## 🎯 Key Features Explained

### Vehicle Management
- ➕ Add vehicles with 15+ fields (make, model, year, price, mileage, etc.)
- 📸 Image upload with validation (type, size, preview)
- ✏️ Edit all vehicle details including image replacement
- 🗑️ Delete vehicles with confirmation
- ⭐ Mark vehicles as "featured" for homepage display
- 📊 Status tracking: available, reserved, sold
- 🔍 VIN validation (17 characters)

### Inquiry System
- 📧 Contact form submissions with vehicle linking
- 📱 WhatsApp integration buttons
- ☎️ Phone call tracking
- ✅ Mark inquiries as contacted with timestamp
- 📝 View all customer details in admin panel

### Security Features
- 🔒 Password hashing with Werkzeug
- 🔑 Session-based authentication (no JWT complexity)
- 📁 Secure file uploads with sanitization
- 🛡️ CSRF protection (Flask built-in)
- ⚠️ File size limits (16MB max)
- ✔️ File type validation (images only)

### User Experience
- 📱 Fully responsive (mobile-first design)
- ⚡ Fast loading (no heavy frameworks)
- 🎨 Clean Bootstrap 5 UI
- 🔔 Flash messages with auto-dismiss
- 🖼️ Image preview before upload
- ✨ Smooth animations and transitions

## 🎨 Customization Guide

### 1. Update Contact Information

**Footer** (`templates/base.html`):
```html
<i class="fas fa-phone"></i> +237 6XX XXX XXX<br>
<i class="fas fa-envelope"></i> info@douala-vehicles.cm
```

**Contact Page** (`templates/contact.html`):
Update business hours, address, phone numbers

**Vehicle Detail** (`templates/vehicle_detail.html`):
```html
<a href="https://wa.me/237XXXXXXXXX?text=...">
```

### 2. Change Color Scheme

Edit `static/css/style.css`:
```css
:root {
    --primary-color: #6366f1;    /* Change this */
    --secondary-color: #06b6d4;  /* And this */
    --success-color: #10b981;
    --danger-color: #ef4444;
}
```

### 3. Modify Company Name

Update these files:
- `templates/base.html` - Navbar and footer
- `templates/index.html` - Hero section
- `templates/about.html` - Company information

### 4. Change Secret Key (Production)

In `app.py`, change:
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

## 📝 Usage Guide

### Adding Your First Vehicle

1. Go to `http://127.0.0.1:5000/admin/login`
2. Login with default credentials (admin/admin123)
3. Click "Add Vehicle" in the sidebar
4. Fill in all required fields:
   - Make, Model, Year
   - Price (in XAF)
   - Mileage (in kilometers)
   - VIN (17 characters)
   - Condition, Fuel Type, Transmission, Body Type
5. Upload an image (JPEG, PNG, GIF, or WebP)
6. Check "Featured" to display on homepage
7. Click "Add Vehicle"

### Managing Inquiries

1. Navigate to "Inquiries" in admin panel
2. View all customer inquiries sorted by date
3. See customer contact details (phone, email)
4. View which vehicle they inquired about
5. Click "Contact" to mark as contacted
6. System automatically records timestamp

### Filtering Inventory

Public users can filter vehicles by:
- **Make**: Select specific car manufacturer
- **Condition**: Excellent, Good, Fair
- **Fuel Type**: Gasoline, Diesel, Electric, Hybrid
- **Transmission**: Automatic, Manual

## 🚀 Deployment

### Deploy to PythonAnywhere (Free Option)

1. Create account at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your project files
3. Create a new web app (Flask)
4. Configure WSGI file
5. Set up static files mapping
6. Reload web app

### Deploy to Heroku

1. Create `Procfile`:
   ```
   web: python app.py
   ```

2. Update `app.py` for production:
   ```python
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port)
   ```

3. Deploy:
   ```cmd
   git init
   heroku create your-app-name
   git add .
   git commit -m "Initial commit"
   git push heroku master
   ```

## 🐛 Troubleshooting

### Port Already in Use
```cmd
# Find process using port 5000
netstat -ano | findstr :5000
# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Database Locked Error
- Close any SQLite browser/viewer
- Restart the Flask application
- Check file permissions

### Images Not Displaying
- Verify `static/images/uploads/` folder exists
- Check image file permissions
- Ensure image paths are correct in database
- Clear browser cache

### Module Not Found Error
```cmd
# Ensure virtual environment is activated
venv\Scripts\activate
# Reinstall dependencies
pip install -r requirements.txt
```

## 🔧 Development

### Adding New Features

1. **Add New Route**: Edit `app.py`
   ```python
   @app.route('/new-page')
   def new_page():
       return render_template('new_page.html')
   ```

2. **Create Template**: Add to `templates/`
   ```html
   {% extends 'base.html' %}
   {% block content %}
   <!-- Your content -->
   {% endblock %}
   ```

3. **Add Styling**: Edit `static/css/style.css`

4. **Add JavaScript**: Edit `static/js/main.js` or `admin.js`

### Database Migrations

To reset database (⚠️ deletes all data):
```cmd
del database.db
python app.py
```

To backup database:
```cmd
copy database.db database_backup.db
```

## 📚 Technologies Used

- **Flask 3.0.0**: Web framework
- **Flask-SQLAlchemy 3.1.1**: Database ORM
- **Werkzeug 3.0.1**: Security utilities
- **Bootstrap 5.3**: CSS framework
- **Font Awesome 6.4**: Icons
- **SQLite**: Database

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements!

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact: info@douala-vehicles.cm

## 🎉 Acknowledgments

- Built for the Douala, Cameroon market
- Designed for bank-repossessed vehicle sales
- Optimized for ease of use and fast performance

---

**Made with ❤️ for Douala Vehicle Dealers**
