from flask import Blueprint, render_template, request, redirect, url_for
from routes.database import events, movies_collection  # Ensure movies_collection is imported

event = Blueprint('event', __name__)

@event.route("/events")
def list_events():
    all_events = list(events.find())
    return render_template("events.html", events=all_events)

@event.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('general.index'))
    
    movies = list(movies_collection.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"genre": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    }))
    
    events_list = list(events.find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    }))
    
    return render_template('search_results.html', 
                         movies=movies, 
                         events=events_list, 
                         query=query)
