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
            # 2017 Reviews (10 reviews - first year)
            {"name": "Michael Johnson", "email": "michael.j@email.com", "rating": 5, "comment": "Excellent service! Found exactly what I was looking for. The car was in great condition and the price was unbeatable.", "is_approved": True, "created_at": datetime(2017, 6, 15)},
            {"name": "Sarah Williams", "email": "sarah.w@email.com", "rating": 5, "comment": "Very professional and transparent process. No hidden fees, just honest pricing. Got a fantastic deal on my SUV!", "is_approved": True, "created_at": datetime(2017, 7, 22)},
            {"name": "Robert Martinez", "email": "robert.m@email.com", "rating": 4, "comment": "Great experience. The staff took time to explain everything about the vehicle. Fair pricing on a quality car.", "is_approved": True, "created_at": datetime(2017, 8, 10)},
            {"name": "Jennifer Garcia", "email": "jennifer.g@email.com", "rating": 5, "comment": "Best car buying experience! No pressure sales, just genuine help. Found my perfect vehicle within budget.", "is_approved": True, "created_at": datetime(2017, 9, 5)},
            {"name": "David Lee", "email": "david.l@email.com", "rating": 5, "comment": "Highly recommend Miami Auto Sales! Got a reliable truck at an amazing price. Professional team!", "is_approved": True, "created_at": datetime(2017, 10, 12)},
            {"name": "Maria Rodriguez", "email": "maria.r@email.com", "rating": 4, "comment": "Happy with my purchase. The car runs great and the price was very reasonable. Good service overall.", "is_approved": True, "created_at": datetime(2017, 11, 3)},
            {"name": "James Anderson", "email": "james.a@email.com", "rating": 5, "comment": "Impressed with the quality of vehicles available. Got exactly what I needed. Will be back!", "is_approved": True, "created_at": datetime(2017, 11, 28)},
            {"name": "Linda Thomas", "email": "linda.t@email.com", "rating": 5, "comment": "Fantastic experience from start to finish. No hassle, fair pricing, quality vehicle. Highly recommend!", "is_approved": True, "created_at": datetime(2017, 12, 8)},
            {"name": "Carlos Hernandez", "email": "carlos.h@email.com", "rating": 4, "comment": "Good selection of vehicles. Found a reliable sedan at a great price. Staff was helpful throughout.", "is_approved": True, "created_at": datetime(2017, 12, 15)},
            {"name": "Patricia White", "email": "patricia.w@email.com", "rating": 5, "comment": "Love my new car! The team made the process so easy. Great prices on bank repos!", "is_approved": True, "created_at": datetime(2017, 12, 22)},
            
            # 2018 Reviews (12 reviews)
            {"name": "John Miller", "email": "john.m@email.com", "rating": 5, "comment": "Outstanding service! Got a great deal on a quality vehicle. Will definitely recommend to friends.", "is_approved": True, "created_at": datetime(2018, 1, 15)},
            {"name": "Angela Brown", "email": "angela.b@email.com", "rating": 4, "comment": "Very satisfied with my purchase. Fair pricing and transparent process throughout.", "is_approved": True, "created_at": datetime(2018, 2, 10)},
            {"name": "Steven Davis", "email": "steven.d@email.com", "rating": 5, "comment": "Best place for bank repossessed vehicles! Got an amazing SUV at unbeatable price.", "is_approved": True, "created_at": datetime(2018, 3, 5)},
            {"name": "Michelle Wilson", "email": "michelle.w@email.com", "rating": 5, "comment": "Professional team, quality vehicles. Found exactly what I was looking for within my budget.", "is_approved": True, "created_at": datetime(2018, 4, 12)},
            {"name": "Daniel Moore", "email": "daniel.m@email.com", "rating": 4, "comment": "Great experience buying my first car here. Staff was patient and helpful. Good prices!", "is_approved": True, "created_at": datetime(2018, 5, 20)},
            {"name": "Jessica Taylor", "email": "jessica.t@email.com", "rating": 5, "comment": "Love my new vehicle! Excellent condition and the price was perfect. Highly recommend!", "is_approved": True, "created_at": datetime(2018, 6, 8)},
            {"name": "Kevin Anderson", "email": "kevin.a@email.com", "rating": 5, "comment": "Impressed with the service and vehicle quality. No hidden fees, just honest pricing.", "is_approved": True, "created_at": datetime(2018, 7, 14)},
            {"name": "Amanda Jackson", "email": "amanda.j@email.com", "rating": 4, "comment": "Happy with my purchase. Found a reliable car at a fair price. Good customer service.", "is_approved": True, "created_at": datetime(2018, 8, 22)},
            {"name": "Brian Martin", "email": "brian.m@email.com", "rating": 5, "comment": "Fantastic experience! Got a quality truck at an amazing price. Will be back for sure!", "is_approved": True, "created_at": datetime(2018, 9, 10)},
            {"name": "Nicole Garcia", "email": "nicole.g@email.com", "rating": 5, "comment": "Best car buying experience ever! Professional, honest, and great selection of vehicles.", "is_approved": True, "created_at": datetime(2018, 10, 5)},
            {"name": "Christopher Lee", "email": "chris.l@email.com", "rating": 4, "comment": "Good service and fair pricing. Found exactly what I needed. Satisfied customer!", "is_approved": True, "created_at": datetime(2018, 11, 12)},
            {"name": "Rebecca Martinez", "email": "rebecca.m@email.com", "rating": 5, "comment": "Highly recommend! Got a beautiful sedan at an unbeatable price. Thank you Miami Auto Sales!", "is_approved": True, "created_at": datetime(2018, 12, 3)},
            
            # 2019 Reviews (10 reviews)
            {"name": "Matthew Thompson", "email": "matthew.t@email.com", "rating": 5, "comment": "Excellent service and quality vehicles. Got exactly what I wanted at the right price.", "is_approved": True, "created_at": datetime(2019, 1, 18)},
            {"name": "Emily Rodriguez", "email": "emily.r@email.com", "rating": 4, "comment": "Very happy with my purchase. Professional staff and transparent pricing. Good experience!", "is_approved": True, "created_at": datetime(2019, 3, 10)},
            {"name": "Joshua Hernandez", "email": "joshua.h@email.com", "rating": 5, "comment": "Great place to buy a car! No pressure, just honest help. Got a fantastic deal!", "is_approved": True, "created_at": datetime(2019, 4, 22)},
            {"name": "Ashley Lopez", "email": "ashley.l@email.com", "rating": 5, "comment": "Love my new car! The team was amazing and helped me find the perfect vehicle.", "is_approved": True, "created_at": datetime(2019, 6, 8)},
            {"name": "Andrew Wilson", "email": "andrew.w@email.com", "rating": 4, "comment": "Good selection and fair prices. Staff was helpful throughout the process.", "is_approved": True, "created_at": datetime(2019, 7, 15)},
            {"name": "Stephanie Moore", "email": "stephanie.m@email.com", "rating": 5, "comment": "Fantastic experience! Got a quality SUV at an amazing price. Highly recommend!", "is_approved": True, "created_at": datetime(2019, 8, 5)},
            {"name": "Ryan Taylor", "email": "ryan.t@email.com", "rating": 5, "comment": "Best place for bank repos! Professional service and great vehicles. Very satisfied!", "is_approved": True, "created_at": datetime(2019, 9, 20)},
            {"name": "Melissa Anderson", "email": "melissa.a@email.com", "rating": 4, "comment": "Happy with my purchase. Fair pricing and good customer service. Would recommend!", "is_approved": True, "created_at": datetime(2019, 10, 12)},
            {"name": "Justin Thomas", "email": "justin.t@email.com", "rating": 5, "comment": "Excellent experience buying my truck here. No hassle and great price!", "is_approved": True, "created_at": datetime(2019, 11, 8)},
            {"name": "Rachel Jackson", "email": "rachel.j@email.com", "rating": 5, "comment": "Outstanding service! Got exactly what I needed within budget. Thank you!", "is_approved": True, "created_at": datetime(2019, 12, 15)},
            
            # 2020 Reviews (8 reviews)
            {"name": "Brandon White", "email": "brandon.w@email.com", "rating": 5, "comment": "Great experience despite pandemic. Safe process, quality vehicle, fair price!", "is_approved": True, "created_at": datetime(2020, 2, 10)},
            {"name": "Victoria Harris", "email": "victoria.h@email.com", "rating": 4, "comment": "Happy with my purchase. Professional service and good selection of vehicles.", "is_approved": True, "created_at": datetime(2020, 4, 20)},
            {"name": "Tyler Martin", "email": "tyler.m@email.com", "rating": 5, "comment": "Excellent service! Found my perfect car at an amazing price. Highly recommend!", "is_approved": True, "created_at": datetime(2020, 6, 15)},
            {"name": "Samantha Clark", "email": "samantha.c@email.com", "rating": 5, "comment": "Love my new vehicle! Professional team and transparent pricing. Best experience!", "is_approved": True, "created_at": datetime(2020, 8, 8)},
            {"name": "Jacob Lewis", "email": "jacob.l@email.com", "rating": 4, "comment": "Good service and fair pricing. Found exactly what I was looking for.", "is_approved": True, "created_at": datetime(2020, 9, 22)},
            {"name": "Lauren Walker", "email": "lauren.w@email.com", "rating": 5, "comment": "Fantastic experience! Got a quality SUV at great price. Will recommend to everyone!", "is_approved": True, "created_at": datetime(2020, 10, 18)},
            {"name": "Nathan Hall", "email": "nathan.h@email.com", "rating": 5, "comment": "Best car buying experience! No pressure, honest pricing, quality vehicle!", "is_approved": True, "created_at": datetime(2020, 11, 12)},
            {"name": "Brittany Allen", "email": "brittany.a@email.com", "rating": 4, "comment": "Very satisfied with my purchase. Professional staff and good selection.", "is_approved": True, "created_at": datetime(2020, 12, 5)},
            
            # 2021 Reviews (8 reviews)
            {"name": "Eric Young", "email": "eric.y@email.com", "rating": 5, "comment": "Outstanding service! Got exactly what I wanted at the perfect price. Highly recommend!", "is_approved": True, "created_at": datetime(2021, 2, 14)},
            {"name": "Kimberly King", "email": "kimberly.k@email.com", "rating": 5, "comment": "Love my new car! Professional team made everything so easy. Great prices!", "is_approved": True, "created_at": datetime(2021, 4, 8)},
            {"name": "Jonathan Wright", "email": "jonathan.w@email.com", "rating": 4, "comment": "Good experience overall. Fair pricing and helpful staff. Happy with my purchase!", "is_approved": True, "created_at": datetime(2021, 6, 20)},
            {"name": "Amber Scott", "email": "amber.s@email.com", "rating": 5, "comment": "Excellent experience! Found the perfect vehicle within my budget. Thank you!", "is_approved": True, "created_at": datetime(2021, 7, 18)},
            {"name": "Robert Taylor", "email": "robert.t@email.com", "rating": 5, "comment": "Impressed with the quality and service. Got a great deal on a bank repo. Highly recommended!", "is_approved": True, "created_at": datetime(2021, 9, 10)},
            {"name": "Crystal Green", "email": "crystal.g@email.com", "rating": 4, "comment": "Happy with my purchase. Professional service and transparent pricing throughout.", "is_approved": True, "created_at": datetime(2021, 10, 5)},
            {"name": "Aaron Baker", "email": "aaron.b@email.com", "rating": 5, "comment": "Fantastic experience! Got a quality truck at amazing price. Will be back!", "is_approved": True, "created_at": datetime(2021, 11, 15)},
            {"name": "Heather Adams", "email": "heather.a@email.com", "rating": 5, "comment": "Best place to buy a car! No hassle, fair pricing, excellent service!", "is_approved": True, "created_at": datetime(2021, 12, 8)},
            
            # 2022 Reviews (6 reviews)
            {"name": "Marcus Nelson", "email": "marcus.n@email.com", "rating": 5, "comment": "Outstanding service! Got exactly what I needed at the right price. Highly recommend!", "is_approved": True, "created_at": datetime(2022, 2, 12)},
            {"name": "Lisa Anderson", "email": "lisa.a@email.com", "rating": 4, "comment": "Very happy with my purchase! Staff was friendly and professional. Found exactly what I needed.", "is_approved": True, "created_at": datetime(2022, 2, 28)},
            {"name": "Derek Carter", "email": "derek.c@email.com", "rating": 5, "comment": "Excellent experience! Quality vehicle at unbeatable price. Thank you Miami Auto Sales!", "is_approved": True, "created_at": datetime(2022, 5, 18)},
            {"name": "Monica Mitchell", "email": "monica.m@email.com", "rating": 5, "comment": "Love my new SUV! Professional team and transparent pricing. Best experience ever!", "is_approved": True, "created_at": datetime(2022, 8, 22)},
            {"name": "Gregory Perez", "email": "gregory.p@email.com", "rating": 4, "comment": "Good service and fair prices. Found a reliable vehicle within budget.", "is_approved": True, "created_at": datetime(2022, 10, 10)},
            {"name": "Tiffany Roberts", "email": "tiffany.r@email.com", "rating": 5, "comment": "Fantastic experience! Got exactly what I wanted. Highly recommend to everyone!", "is_approved": True, "created_at": datetime(2022, 11, 28)},
            
            # 2023 Reviews (4 reviews)
            {"name": "Keith Turner", "email": "keith.t@email.com", "rating": 5, "comment": "Great service! Found my perfect car at an amazing price. Very professional team!", "is_approved": True, "created_at": datetime(2023, 3, 15)},
            {"name": "Vanessa Phillips", "email": "vanessa.p@email.com", "rating": 4, "comment": "Happy with my purchase. Good selection and fair pricing. Would recommend!", "is_approved": True, "created_at": datetime(2023, 6, 8)},
            {"name": "Raymond Campbell", "email": "raymond.c@email.com", "rating": 5, "comment": "Excellent experience! No pressure sales, just honest help. Got a great deal!", "is_approved": True, "created_at": datetime(2023, 9, 20)},
            {"name": "Natalie Parker", "email": "natalie.p@email.com", "rating": 5, "comment": "Love my new vehicle! Professional service and quality cars. Highly recommend!", "is_approved": True, "created_at": datetime(2023, 11, 12)},
            
            # 2024 Reviews (3 reviews)
            {"name": "Gary Evans", "email": "gary.e@email.com", "rating": 5, "comment": "Outstanding experience! Got exactly what I needed at the perfect price!", "is_approved": True, "created_at": datetime(2024, 4, 10)},
            {"name": "Denise Edwards", "email": "denise.e@email.com", "rating": 4, "comment": "Very satisfied with my purchase. Professional staff and good prices.", "is_approved": True, "created_at": datetime(2024, 8, 15)},
            {"name": "Russell Collins", "email": "russell.c@email.com", "rating": 5, "comment": "Fantastic service! Found the perfect truck at an amazing price. Thank you!", "is_approved": True, "created_at": datetime(2024, 11, 20)},
            
            # 2025 Reviews (2 reviews)
            {"name": "Sharon Stewart", "email": "sharon.s@email.com", "rating": 5, "comment": "Excellent experience! Professional team and quality vehicles. Highly recommend!", "is_approved": True, "created_at": datetime(2025, 2, 8)},
            {"name": "Philip Sanchez", "email": "philip.s@email.com", "rating": 4, "comment": "Happy with my purchase. Fair pricing and good customer service.", "is_approved": True, "created_at": datetime(2025, 5, 18)},
            
            # 2026 Reviews (2 reviews)
            {"name": "James Wilson", "email": "james.w@email.com", "rating": 5, "comment": "Outstanding experience from start to finish! The team went above and beyond. Great prices!", "is_approved": True, "created_at": datetime(2026, 5, 12)},
            {"name": "Patricia Davis", "email": "patricia.d@email.com", "rating": 5, "comment": "Couldn't be happier with my purchase! Professional service and quality vehicle!", "is_approved": True, "created_at": datetime(2026, 7, 20)}
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
