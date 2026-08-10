from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Email Configuration (Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Paatymurray@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'your-app-password-here'  # Gmail App Password (see instructions below)
app.config['MAIL_DEFAULT_SENDER'] = 'Paatymurray@gmail.com'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(20), nullable=False)  # excellent, good, fair
    fuel_type = db.Column(db.String(20), nullable=False)  # gasoline, diesel, electric, hybrid
    transmission = db.Column(db.String(20), nullable=False)  # automatic, manual
    body_type = db.Column(db.String(20), nullable=False)  # sedan, suv, truck, van, etc
    vin = db.Column(db.String(17), unique=True, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='available')  # available, reserved, sold
    featured = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    inquiries = db.relationship('Inquiry', backref='vehicle', lazy=True)
    reviews = db.relationship('Review', backref='vehicle', lazy=True)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    inquiry_type = db.Column(db.String(20), default='contact_form')  # whatsapp, contact_form, phone_call, test_drive, reservation
    message = db.Column(db.Text)
    is_contacted = db.Column(db.Boolean, default=False)
    contacted_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)  # Admin must approve
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Public Routes
@app.route('/')
def index():
    featured_vehicles = Vehicle.query.filter_by(status='available', featured=True).order_by(Vehicle.created_at.desc()).limit(6).all()
    
    # Calculate statistics
    total_vehicles = Vehicle.query.count()
    available_vehicles = Vehicle.query.filter_by(status='available').count()
    sold_vehicles = Vehicle.query.filter_by(status='sold').count()
    total_inquiries = Inquiry.query.count()
    
    # Calculate real customer satisfaction from reviews
    approved_reviews = Review.query.filter_by(is_approved=True).all()
    if approved_reviews:
        total_rating = sum(review.rating for review in approved_reviews)
        avg_rating = total_rating / len(approved_reviews)
        satisfaction_rate = (avg_rating / 5) * 100  # Convert to percentage
    else:
        satisfaction_rate = 0  # No reviews yet
    
    return render_template('index.html', 
                         vehicles=featured_vehicles,
                         total_vehicles=total_vehicles,
                         available_vehicles=available_vehicles,
                         sold_vehicles=sold_vehicles,
                         total_inquiries=total_inquiries,
                         satisfaction_rate=satisfaction_rate,
                         total_reviews=len(approved_reviews),
                         approved_reviews=approved_reviews)

@app.route('/inventory')
def inventory():
    # Get filters from query parameters
    make = request.args.get('make')
    condition = request.args.get('condition')
    fuel_type = request.args.get('fuel_type')
    transmission = request.args.get('transmission')
    
    query = Vehicle.query.filter_by(status='available')
    
    if make:
        query = query.filter_by(make=make)
    if condition:
        query = query.filter_by(condition=condition)
    if fuel_type:
        query = query.filter_by(fuel_type=fuel_type)
    if transmission:
        query = query.filter_by(transmission=transmission)
    
    vehicles = query.all()
    
    # Get unique makes for filter dropdown
    makes = db.session.query(Vehicle.make).distinct().all()
    makes = [m[0] for m in makes]
    
    return render_template('inventory.html', vehicles=vehicles, makes=makes)

@app.route('/vehicle/<int:id>')
def vehicle_detail(id):
    vehicle = Vehicle.query.get_or_404(id)
    return render_template('vehicle_detail.html', vehicle=vehicle)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        inquiry = Inquiry(
            name=request.form['name'],
            phone=request.form['phone'],
            email=request.form.get('email'),
            message=request.form.get('message'),
            inquiry_type='contact_form'
        )
        db.session.add(inquiry)
        db.session.commit()
        
        # Send email notification
        try:
            msg = Message(
                subject='New Contact Form Inquiry - Douala Vehicles',
                recipients=['Paatymurray@gmail.com'],  # Your email to receive notifications
                body=f"""
New inquiry from your website!

Name: {request.form['name']}
Phone: {request.form['phone']}
Email: {request.form.get('email', 'Not provided')}

Message:
{request.form.get('message', 'No message')}

---
This inquiry has been saved to your database.
Login to your admin panel to manage: http://127.0.0.1:5000/admin/login
                """
            )
            mail.send(msg)
            flash('Thank you! Your message has been sent. We will contact you soon.', 'success')
        except Exception as e:
            # Still save to database even if email fails
            flash('Thank you for your inquiry! We will contact you soon.', 'success')
            print(f"Email error: {e}")  # Log error for debugging
        
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit-review', methods=['GET', 'POST'])
def submit_review():
    if request.method == 'POST':
        # Create new review
        review = Review(
            vehicle_id=request.form.get('vehicle_id') if request.form.get('vehicle_id') else None,
            name=request.form['name'],
            email=request.form.get('email'),
            rating=int(request.form['rating']),
            comment=request.form['comment'],
            is_approved=False  # Reviews need admin approval
        )
        db.session.add(review)
        db.session.commit()
        
        # Send email notification to admin
        try:
            msg = Message(
                subject='New Customer Review Submitted - Miami Auto Sales',
                recipients=['Paatymurray@gmail.com'],
                body=f"""
A new customer review has been submitted and is pending approval.

Customer: {request.form['name']}
Email: {request.form.get('email', 'Not provided')}
Rating: {request.form['rating']}/5 stars

Review:
{request.form['comment']}

---
Login to your admin panel to approve or reject this review:
http://127.0.0.1:5000/admin/reviews
                """
            )
            mail.send(msg)
        except Exception as e:
            print(f"Email error: {e}")
        
        flash('Thank you for your review! It will be published after approval by our team.', 'success')
        return redirect(url_for('index'))
    
    # Get all vehicles for the dropdown
    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    return render_template('submit_review.html', vehicles=vehicles)

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    total_vehicles = Vehicle.query.count()
    available_vehicles = Vehicle.query.filter_by(status='available').count()
    sold_vehicles = Vehicle.query.filter_by(status='sold').count()
    total_inquiries = Inquiry.query.count()
    pending_inquiries = Inquiry.query.filter_by(is_contacted=False).count()
    
    recent_vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).limit(5).all()
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_vehicles=total_vehicles,
                         available_vehicles=available_vehicles,
                         sold_vehicles=sold_vehicles,
                         total_inquiries=total_inquiries,
                         pending_inquiries=pending_inquiries,
                         recent_vehicles=recent_vehicles,
                         recent_inquiries=recent_inquiries)

@app.route('/admin/vehicles')
def admin_vehicles():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    return render_template('admin/vehicles.html', vehicles=vehicles)

@app.route('/admin/vehicles/add', methods=['GET', 'POST'])
def admin_add_vehicle():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        # Handle image upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = filename
        
        vehicle = Vehicle(
            make=request.form['make'],
            model=request.form['model'],
            year=int(request.form['year']),
            price=float(request.form['price']),
            mileage=int(request.form['mileage']),
            condition=request.form['condition'],
            fuel_type=request.form['fuel_type'],
            transmission=request.form['transmission'],
            body_type=request.form['body_type'],
            vin=request.form['vin'],
            description=request.form.get('description'),
            status=request.form.get('status', 'available'),
            featured=request.form.get('featured') == 'on',
            image_url=image_url
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('admin_vehicles'))
    
    return render_template('admin/add_vehicle.html')

@app.route('/admin/vehicles/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit_vehicle(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    vehicle = Vehicle.query.get_or_404(id)
    
    if request.method == 'POST':
        vehicle.make = request.form['make']
        vehicle.model = request.form['model']
        vehicle.year = int(request.form['year'])
        vehicle.price = float(request.form['price'])
        vehicle.mileage = int(request.form['mileage'])
        vehicle.condition = request.form['condition']
        vehicle.fuel_type = request.form['fuel_type']
        vehicle.transmission = request.form['transmission']
        vehicle.body_type = request.form['body_type']
        vehicle.vin = request.form['vin']
        vehicle.description = request.form.get('description')
        vehicle.status = request.form.get('status', 'available')
        vehicle.featured = request.form.get('featured') == 'on'
        
        # Handle new image upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                vehicle.image_url = filename
        
        db.session.commit()
        flash('Vehicle updated successfully!', 'success')
        return redirect(url_for('admin_vehicles'))
    
    return render_template('admin/edit_vehicle.html', vehicle=vehicle)

@app.route('/admin/vehicles/delete/<int:id>')
def admin_delete_vehicle(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    
    flash('Vehicle deleted successfully!', 'success')
    return redirect(url_for('admin_vehicles'))

@app.route('/admin/inquiries')
def admin_inquiries():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries)

@app.route('/admin/inquiries/contact/<int:id>')
def admin_mark_contacted(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    inquiry = Inquiry.query.get_or_404(id)
    inquiry.is_contacted = True
    inquiry.contacted_at = datetime.utcnow()
    db.session.commit()
    
    flash('Inquiry marked as contacted!', 'success')
    return redirect(url_for('admin_inquiries'))

@app.route('/admin/reviews')
def admin_reviews():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    pending = Review.query.filter_by(is_approved=False).order_by(Review.created_at.desc()).all()
    approved = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    
    # Calculate statistics
    total_reviews = Review.query.count()
    pending_reviews = len(pending)
    approved_reviews = len(approved)
    
    # Calculate average rating from approved reviews
    if approved_reviews > 0:
        total_rating = sum(review.rating for review in approved)
        average_rating = total_rating / approved_reviews
        satisfaction_rate = (average_rating / 5) * 100
    else:
        average_rating = 0
        satisfaction_rate = 0
    
    return render_template('admin/reviews.html',
                         pending=pending,
                         approved=approved,
                         total_reviews=total_reviews,
                         pending_reviews=pending_reviews,
                         approved_reviews=approved_reviews,
                         average_rating=average_rating,
                         satisfaction_rate=satisfaction_rate)

@app.route('/admin/reviews/approve/<int:id>')
def admin_approve_review(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    review = Review.query.get_or_404(id)
    review.is_approved = True
    db.session.commit()
    
    flash('Review approved successfully!', 'success')
    return redirect(url_for('admin_reviews'))

@app.route('/admin/reviews/unapprove/<int:id>')
def admin_unapprove_review(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    review = Review.query.get_or_404(id)
    review.is_approved = False
    db.session.commit()
    
    flash('Review moved to pending!', 'success')
    return redirect(url_for('admin_reviews'))

@app.route('/admin/reviews/delete/<int:id>')
def admin_delete_review(id):
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('admin_reviews'))

def init_sample_reviews():
    """Initialize database with sample reviews if none exist"""
    try:
        existing_count = Review.query.count()
        
        if existing_count > 0:
            print(f"Database already has {existing_count} reviews. Skipping initialization.")
            return
        
        print("Initializing database with sample reviews...")
        
        sample_reviews = [
            {
                "name": "Michael Johnson",
                "email": "michael.j@email.com",
                "rating": 5,
                "comment": "Excellent service! Found exactly what I was looking for. The car was in great condition and the price was unbeatable. Highly recommend Miami Auto Sales!",
                "is_approved": True,
                "created_at": datetime(2017, 6, 15)
            },
            {
                "name": "Sarah Williams",
                "email": "sarah.w@email.com",
                "rating": 5,
                "comment": "Very professional and transparent process. No hidden fees, just honest pricing. Got a fantastic deal on my SUV. Will definitely recommend to friends!",
                "is_approved": True,
                "created_at": datetime(2017, 11, 22)
            },
            {
                "name": "David Martinez",
                "email": "david.m@email.com",
                "rating": 4,
                "comment": "Great experience overall. The team was helpful and patient with all my questions. Found a reliable vehicle at a fair price. Very satisfied!",
                "is_approved": True,
                "created_at": datetime(2019, 3, 10)
            },
            {
                "name": "Jennifer Brown",
                "email": "jennifer.b@email.com",
                "rating": 5,
                "comment": "Best car buying experience I've had! No pressure, just genuine help finding the right vehicle. The car runs perfectly and looks amazing. Thank you!",
                "is_approved": True,
                "created_at": datetime(2019, 8, 5)
            },
            {
                "name": "Robert Taylor",
                "email": "robert.t@email.com",
                "rating": 5,
                "comment": "Impressed with the quality and service. The vehicle was thoroughly inspected and everything was explained clearly. Got a great deal on a bank repo. Highly recommended!",
                "is_approved": True,
                "created_at": datetime(2021, 7, 18)
            },
            {
                "name": "Lisa Anderson",
                "email": "lisa.a@email.com",
                "rating": 4,
                "comment": "Very happy with my purchase! The staff was friendly and professional. Found exactly what I needed within my budget. Would definitely buy from them again.",
                "is_approved": True,
                "created_at": datetime(2022, 2, 28)
            },
            {
                "name": "James Wilson",
                "email": "james.w@email.com",
                "rating": 5,
                "comment": "Outstanding experience from start to finish! The team went above and beyond to help me find the perfect vehicle. Great prices and excellent customer service!",
                "is_approved": True,
                "created_at": datetime(2026, 5, 12)
            },
            {
                "name": "Patricia Davis",
                "email": "patricia.d@email.com",
                "rating": 5,
                "comment": "Couldn't be happier with my purchase! Professional service, fair pricing, and a quality vehicle. This is the place to go for bank repossessed cars!",
                "is_approved": True,
                "created_at": datetime(2026, 7, 20)
            }
        ]
        
        for review_data in sample_reviews:
            review = Review(**review_data)
            db.session.add(review)
        
        db.session.commit()
        print(f"✅ Successfully added {len(sample_reviews)} sample reviews!")
    except Exception as e:
        print(f"Error initializing reviews: {e}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: admin / admin123")
        
        # Initialize sample reviews
        init_sample_reviews()
    
    app.run(debug=True)
else:
    # When running on Render with gunicorn, create tables on import
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
        
        # Initialize sample reviews for Render
        init_sample_reviews()
