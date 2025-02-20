from pymongo import MongoClient
from config import Config

# Initialize MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client.get_database()

# Collections
users = db["users"]
movies_collection = db["movies"]
events = db["events"]
bookings = db["bookings"]
reviews = db["reviews"]

