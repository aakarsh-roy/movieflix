from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from routes.database import movies_collection, events, reviews

# Define the blueprint
general = Blueprint('general', __name__)

@general.route("/")
def index():
    trending_movies = list(movies_collection.find({"type": "trending"}).limit(3))
    upcoming_movies = list(movies_collection.find({"type": "upcoming"}).limit(3))
    featured_events = list(events.find().limit(2))
    recent_reviews = list(reviews.find().sort("date", -1).limit(2))
    
    slider_images = ["slider1.jpg", "slider2.avif", "slider4.jpg"]
    
    return render_template(
        "index.html",
        trending_movies=trending_movies,
        upcoming_movies=upcoming_movies,
        user_reviews=recent_reviews,
        events=featured_events,
        slider_images=slider_images
    )

@general.route("/search")
def search():
    query = request.args.get("q", "")
    
    if not query:
        return redirect(url_for("general.index"))  # ✅ 
    
    movies = list(movies_collection.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"genre": {"$regex": query, "$options": "i"}},
            
        ]
    }))
    
    events_list = list(events.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            
        ]
    }))
    
    return render_template("search_results.html", movies=movies, events=events_list, query=query)

# Error Handlers
