# Customer Review System Guide

## Overview
The customer review system allows customers to leave reviews about their experience with Miami Auto Sales. All reviews are reviewed and approved by admins before appearing on the website, ensuring authenticity and quality.

## Features Implemented

### 1. **Customer Review Submission**
- Public form accessible at `/submit-review` or via "Reviews" link in navigation
- Customers can rate their experience from 1-5 stars
- Optional vehicle selection (if they purchased a specific vehicle)
- Required fields: Name, Rating, Review text
- Optional fields: Email, Vehicle purchased
- All reviews require admin approval before being published

### 2. **Real Customer Satisfaction Calculation**
- The satisfaction rate on the homepage is now calculated from real customer reviews
- Formula: `(Average Rating / 5) × 100%`
- Only approved reviews count toward the satisfaction rate
- Shows "No Reviews Yet" if no approved reviews exist
- Updates automatically when reviews are approved/unapproved

### 3. **Admin Review Management**
- New "Reviews" section in admin panel at `/admin/reviews`
- Two sections: Pending Reviews and Approved Reviews
- Statistics displayed:
  - Total Reviews
  - Average Rating (1-5 stars)
  - Satisfaction Rate (percentage)

### 4. **Admin Actions**
- **Approve**: Move pending review to approved (counts toward satisfaction rate)
- **Unapprove**: Move approved review back to pending
- **Delete**: Permanently remove a review
- All actions update the satisfaction rate in real-time

### 5. **Email Notifications**
- Admin receives email notification when a new review is submitted
- Email includes: Customer name, rating, review text
- Link to admin panel for quick approval

## How It Works

### For Customers:
1. Click "Reviews" in the navigation menu
2. Fill out the review form (name, rating, review text)
3. Optionally select the vehicle they purchased
4. Submit the review
5. Review goes to admin for approval
6. Once approved, it counts toward the satisfaction rate

### For Admins:
1. Receive email notification of new review
2. Login to admin panel
3. Go to "Reviews" section
4. Review the pending submissions
5. Approve legitimate reviews
6. Delete spam or inappropriate reviews
7. Satisfaction rate updates automatically on homepage

## Database Schema

### Review Model:
```python
class Review(db.Model):
    id = Integer (Primary Key)
    vehicle_id = Integer (Foreign Key, Optional)
    name = String(100) (Required)
    email = String(120) (Optional)
    rating = Integer (1-5, Required)
    comment = Text (Required)
    is_approved = Boolean (Default: False)
    created_at = DateTime
```

## Pages Updated

### Public Pages:
1. **Homepage (`/`)**: Shows real satisfaction rate based on approved reviews
2. **Submit Review (`/submit-review`)**: New page for customers to leave reviews
3. **Navigation**: Added "Reviews" link

### Admin Pages:
1. **Admin Sidebar**: Added "Reviews" link
2. **Reviews Management (`/admin/reviews`)**: New page to manage all reviews

## Routes Added

### Public Routes:
- `GET /submit-review` - Display review submission form
- `POST /submit-review` - Process review submission

### Admin Routes:
- `GET /admin/reviews` - Display all reviews (pending and approved)
- `GET /admin/reviews/approve/<id>` - Approve a review
- `GET /admin/reviews/unapprove/<id>` - Unapprove a review
- `GET /admin/reviews/delete/<id>` - Delete a review

## Testing the System

### Test as Customer:
1. Go to http://127.0.0.1:5000
2. Click "Reviews" in navigation
3. Submit a test review with 5 stars
4. Check homepage - satisfaction rate should show "No Reviews Yet" (review pending)

### Test as Admin:
1. Go to http://127.0.0.1:5000/admin/login
2. Login with: username: `admin`, password: `admin123`
3. Click "Reviews" in sidebar
4. See the pending review
5. Click "Approve" button
6. Go back to homepage
7. Satisfaction rate should now show 100% (5/5 stars = 100%)

### Add More Reviews:
1. Submit more reviews with different ratings
2. Approve them as admin
3. Watch the satisfaction rate change based on the average

Example:
- 1 review at 5 stars = 100%
- 1 review at 5 stars + 1 review at 4 stars = 90% ((5+4)/2 = 4.5, 4.5/5 = 0.9 = 90%)
- 1 review at 5 stars + 1 review at 3 stars = 80% ((5+3)/2 = 4, 4/5 = 0.8 = 80%)

## Important Notes

1. **Reviews require approval**: All customer reviews are hidden until an admin approves them
2. **Real data only**: The satisfaction rate is calculated from actual approved reviews
3. **Transparent**: If no reviews exist, homepage shows "No Reviews Yet" instead of fake numbers
4. **Quality control**: Admins can delete spam or inappropriate reviews
5. **Email alerts**: Admin is notified immediately when new reviews arrive
6. **Anonymous option**: Customers can leave reviews without providing email

## Future Enhancements (Optional)

- Display recent reviews on homepage
- Allow customers to upload photos with reviews
- Add review responses (admin can reply to reviews)
- Filter reviews by rating (show 5-star reviews only, etc.)
- Sort reviews by date or rating
- Add review verification (only customers who made purchases)
- Public reviews page showing all approved reviews

## Troubleshooting

### Satisfaction rate shows 0%:
- Check if any reviews are approved (not just pending)
- Verify reviews exist in database with `is_approved=True`

### Reviews not appearing on homepage:
- Reviews don't display individually yet (only the satisfaction rate shows)
- To display individual reviews, add a testimonials section (future enhancement)

### Email notifications not working:
- Check Gmail app password in `app.py`
- See `EMAIL_SETUP_INSTRUCTIONS.md` for email configuration

### Can't approve reviews:
- Make sure you're logged in as admin
- Check session is active (login again if needed)
