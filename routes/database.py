from pymongo import MongoClient
from config import Config
import ssl

# Initialize MongoDB connection with proper SSL configuration
try:
    # For newer PyMongo versions, use tlsInsecure instead of ssl_cert_reqs
    client = MongoClient(
        Config.MONGO_URI,
        tlsInsecure=True,  # Disable SSL certificate verification
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000
    )
    
    # Test the connection
    client.admin.command('ping')
    print("MongoDB Atlas connection successful!")
    
    db = client.get_database()
    
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    # Try alternative SSL configuration
    try:
        client = MongoClient(
            Config.MONGO_URI,
            ssl=True,
            ssl_ca_certs=None,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        client.admin.command('ping')
        print("MongoDB Atlas connection successful with alternative SSL config!")
        db = client.get_database()
        
    except Exception as e2:
        print(f"Alternative connection also failed: {e2}")
        # Fallback to local MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["movieflix"]
        print("Using local MongoDB fallback")

# Collections
users = db["users"]
movies_collection = db["movies"]
events = db["events"]
bookings = db["bookings"]
reviews = db["reviews"]