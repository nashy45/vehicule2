"""
Add sample customer reviews to the database
"""
from app import app, db, Review
from datetime import datetime

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

with app.app_context():
    # Check if reviews already exist
    existing_count = Review.query.count()
    
    if existing_count > 0:
        print(f"Database already has {existing_count} reviews.")
        response = input("Do you want to add more sample reviews? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled. No reviews added.")
            exit()
    
    print("Adding sample reviews...\n")
    
    for idx, review_data in enumerate(sample_reviews, 1):
        review = Review(**review_data)
        db.session.add(review)
        year = review_data['created_at'].year
        print(f"{idx}. Added review by {review_data['name']} - {review_data['rating']} stars ({year})")
    
    db.session.commit()
    print(f"\n✅ Successfully added {len(sample_reviews)} reviews!")
    print("\nThese reviews span from 2017 to 2026.")
    print("You can manage them in the admin panel at: /admin/reviews")
