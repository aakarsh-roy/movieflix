from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from bson import ObjectId
from datetime import datetime
from routes.database import movies_collection, bookings, users, reviews
from routes.auth import login_required
from fpdf import FPDF
from utils import send_booking_confirmation

movie = Blueprint('movie', __name__)

@movie.route("/movies")
def list_movies():
    genre = request.args.get('genre')
    sort = request.args.get('sort', 'rating')
    
    query = {"type": "showing"}
    if genre:
        query["genre"] = genre
    
    sort_criteria = [("rating", -1)] if sort == "rating" else [("title", 1)]
    
    all_movies = list(movies_collection.find(query).sort(sort_criteria))
    genres = movies_collection.distinct("genre")
    
    return render_template(
        "movies.html",
        movies=all_movies,
        genres=genres,
        current_genre=genre,
        current_sort=sort
    )

@movie.route("/book/<movie_id>", methods=["GET", "POST"])
@login_required
def book_ticket(movie_id):
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
    
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            seats = request.form.getlist("seats[]")[0].split(',')  # Split comma-separated seats
            seats = [seat.strip() for seat in seats]  # Clean up whitespace
            showtime = request.form["showtime"]
            total_price = len(seats) * movie.get("price", 200)
            
            booking_data = {
                "user_id": ObjectId(session['user_id']),
                "movie_id": ObjectId(movie_id),
                "title": movie["title"],
                "name": name,
                "email": email,
                "seats": seats,
                "showtime": showtime,
                "total_price": total_price,
                "booking_date": datetime.now(),
                "status": "confirmed"
                
            }

            # Insert booking into database
            booking_id = bookings.insert_one(booking_data).inserted_id
            booking_data['_id'] = str(booking_id)
            
            try:
                # Send confirmation email with PDF
                if send_booking_confirmation(email, booking_data):
                    flash(f"Successfully booked {len(seats)} tickets! Check your email for confirmation.", "success")
                else:
                    flash("Booking successful but email confirmation failed.", "warning")
            except Exception as e:
                flash(f"Booking successful but email confirmation failed: {str(e)}", "warning")
            
            return redirect(url_for("booking.booking_confirmation", booking_id=booking_id))
            
        except Exception as e:
            flash(f"Booking failed: {str(e)}", "error")
            return redirect(url_for("booking.book_ticket", movie_id=movie_id))
    
    return render_template("booking.html", movie=movie)

@movie.route("/booking_confirmation/<booking_id>")
@login_required
def booking_confirmation(booking_id):
    booking = bookings.find_one({"_id": ObjectId(booking_id)})
    movie = movies_collection.find_one({"_id": booking["movie_id"]})
    
    return render_template(
        "confirmation.html",
        booking=booking,
        movie=movie
    )

@movie.route('/add_review/<movie_id>', methods=['POST'])
@login_required
def add_review(movie_id):
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')
    
    review_data = {
        "user_id": ObjectId(session['user_id']),
        "movie_id": ObjectId(movie_id),
        "rating": rating,
        "comment": comment,
        "date": datetime.now()
    }
    
    reviews.insert_one(review_data)
    flash('Review added successfully!', 'success')
    return redirect(url_for('movie.movie_details', movie_id=movie_id))

@movie.route('/movie/<movie_id>')
def movie_details(movie_id):
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
    movie_reviews = list(reviews.find({"movie_id": ObjectId(movie_id)}).sort("date", -1))
    
    review_details = []
    for review in movie_reviews:
        user = users.find_one({"_id": review["user_id"]})
        if user:
            review_details.append({
                "user_name": user["name"],
                "rating": review["rating"],
                "comment": review["comment"],
                "date": review["date"]
            })
    
    return render_template('movie_details.html', movie=movie, reviews=review_details)

@movie.route('/cancel_booking/<booking_id>')
@login_required
def cancel_booking(booking_id):
    booking = bookings.find_one({"_id": ObjectId(booking_id)})
    
    if booking and str(booking["user_id"]) == session["user_id"]:
        bookings.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": "cancelled"}}
        )
        flash('Booking cancelled successfully!', 'success')
    else:
        flash('Invalid booking!', 'error')
    
    return redirect(url_for('user.profile'))