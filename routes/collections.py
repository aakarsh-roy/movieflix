# setup_collections.py
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def setup_collections():
    """Create collections and add sample data for MovieFlix application"""
    
    # Connect to MongoDB Atlas
    client = MongoClient(
        os.getenv("MONGO_URI"),
        tlsInsecure=True,
        serverSelectionTimeoutMS=5000
    )
    
    db = client.get_database()
    
    print("Creating collections and adding sample data...")
    
    # 1. USERS Collection
    if "users" not in db.list_collection_names():
        db.create_collection("users")
    
    # Sample users
    sample_users = [
        {
            "_id": ObjectId(),
            "name": "John Doe",
            "email": "john@example.com",
            "password": "hashed_password_here",
            "phone": "1234567890",
            "join_date": datetime.now()
        },
        {
            "_id": ObjectId(),
            "name": "Jane Smith", 
            "email": "jane@example.com",
            "password": "hashed_password_here",
            "phone": "0987654321",
            "join_date": datetime.now()
        }
    ]
    
    if db.users.count_documents({}) == 0:
        db.users.insert_many(sample_users)
        print("✅ Users collection created with sample data")
    
    # 2. MOVIES Collection
    if "movies" not in db.list_collection_names():
        db.create_collection("movies")
    
    # Sample movies based on your app structure
    sample_movies = [
        {
            "_id": ObjectId(),
            "title": "Avengers: Endgame",
            "genre": "Action",
            "description": "The Avengers take a final stand against Thanos.",
            "duration": "181 minutes",
            "rating": 8.4,
            "price": 200,
            "type": "trending",
            "image": "avengers.jpg",
            "showtimes": ["10:00 AM", "2:00 PM", "6:00 PM", "10:00 PM"],
            "release_date": datetime(2019, 4, 26),
            "cast": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"]
        },
        {
            "_id": ObjectId(),
            "title": "Spider-Man: No Way Home",
            "genre": "Action",
            "description": "Spider-Man seeks help from Doctor Strange.",
            "duration": "148 minutes", 
            "rating": 8.2,
            "price": 250,
            "type": "showing",
            "image": "spiderman.jpg",
            "showtimes": ["11:00 AM", "3:00 PM", "7:00 PM", "11:00 PM"],
            "release_date": datetime(2021, 12, 17),
            "cast": ["Tom Holland", "Zendaya", "Benedict Cumberbatch"]
        },
        {
            "_id": ObjectId(),
            "title": "Dune: Part Two",
            "genre": "Sci-Fi",
            "description": "Paul Atreides unites with Chani and the Fremen.",
            "duration": "166 minutes",
            "rating": 8.7,
            "price": 300,
            "type": "upcoming",
            "image": "dune2.jpg", 
            "showtimes": ["12:00 PM", "4:00 PM", "8:00 PM"],
            "release_date": datetime(2024, 3, 1),
            "cast": ["Timothée Chalamet", "Zendaya", "Rebecca Ferguson"]
        },
        {
            "_id": ObjectId(),
            "title": "The Batman",
            "genre": "Action", 
            "description": "Batman ventures into Gotham City's underworld.",
            "duration": "176 minutes",
            "rating": 7.8,
            "price": 220,
            "type": "showing",
            "image": "batman.jpg",
            "showtimes": ["1:00 PM", "5:00 PM", "9:00 PM"],
            "release_date": datetime(2022, 3, 4),
            "cast": ["Robert Pattinson", "Zoë Kravitz", "Paul Dano"]
        }
    ]
    
    if db.movies.count_documents({}) == 0:
        db.movies.insert_many(sample_movies)
        print("✅ Movies collection created with sample data")
    
    # 3. EVENTS Collection  
    if "events" not in db.list_collection_names():
        db.create_collection("events")
    
    # Sample events
    sample_events = [
        {
            "_id": ObjectId(),
            "title": "Marvel Movie Marathon",
            "description": "Watch all Marvel movies in chronological order",
            "date": datetime.now() + timedelta(days=7),
            "venue": "MovieFlix Grand Theater",
            "price": 500,
            "image": "marvel_marathon.jpg",
            "capacity": 200,
            "booked": 45
        },
        {
            "_id": ObjectId(), 
            "title": "Horror Night Special",
            "description": "Spine-chilling horror movie experience",
            "date": datetime.now() + timedelta(days=14),
            "venue": "MovieFlix IMAX",
            "price": 350,
            "image": "horror_night.jpg", 
            "capacity": 150,
            "booked": 28
        }
    ]
    
    if db.events.count_documents({}) == 0:
        db.events.insert_many(sample_events)
        print("✅ Events collection created with sample data")
    
    # 4. BOOKINGS Collection
    if "bookings" not in db.list_collection_names():
        db.create_collection("bookings")
    
    # Sample bookings (using the sample user and movie IDs)
    user_id = sample_users[0]["_id"]
    movie_id = sample_movies[0]["_id"]
    
    sample_bookings = [
        {
            "_id": ObjectId(),
            "user_id": user_id,
            "movie_id": movie_id,
            "title": "Avengers: Endgame",
            "name": "John Doe",
            "email": "john@example.com", 
            "seats": ["A1", "A2"],
            "showtime": "6:00 PM",
            "total_price": 400,
            "booking_date": datetime.now() - timedelta(days=2),
            "status": "confirmed"
        }
    ]
    
    if db.bookings.count_documents({}) == 0:
        db.bookings.insert_many(sample_bookings)
        print("✅ Bookings collection created with sample data")
    
    # 5. REVIEWS Collection
    if "reviews" not in db.list_collection_names():
        db.create_collection("reviews")
    
    # Sample reviews
    sample_reviews = [
        {
            "_id": ObjectId(),
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": 5,
            "comment": "Amazing movie! Loved every moment of it.",
            "date": datetime.now() - timedelta(days=1)
        },
        {
            "_id": ObjectId(),
            "user_id": sample_users[1]["_id"],
            "movie_id": sample_movies[1]["_id"], 
            "rating": 4,
            "comment": "Great action sequences and storyline.",
            "date": datetime.now() - timedelta(hours=12)
        }
    ]
    
    if db.reviews.count_documents({}) == 0:
        db.reviews.insert_many(sample_reviews)
        print("✅ Reviews collection created with sample data")
    
    # Create useful indexes
    print("Creating indexes...")
    db.users.create_index("email", unique=True)
    db.movies.create_index("title")
    db.movies.create_index("type")
    db.movies.create_index("genre")
    db.bookings.create_index("user_id")
    db.reviews.create_index("movie_id")
    db.events.create_index("date")
    
    print("✅ All indexes created")
    print("\n🎉 Database setup completed successfully!")
    print(f"📊 Collections created:")
    print(f"   • Users: {db.users.count_documents({})} documents")
    print(f"   • Movies: {db.movies.count_documents({})} documents") 
    print(f"   • Events: {db.events.count_documents({})} documents")
    print(f"   • Bookings: {db.bookings.count_documents({})} documents")
    print(f"   • Reviews: {db.reviews.count_documents({})} documents")
    
    client.close()

if __name__ == "__main__":
    setup_collections()