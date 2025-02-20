from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from bson import ObjectId
from datetime import datetime
from routes.database import bookings, movies_collection, events
from routes.auth import login_required
from fpdf import FPDF
from utils import send_booking_confirmation

booking = Blueprint('booking', __name__)

@booking.route("/my_bookings")
@login_required
def my_bookings():
    user_id = ObjectId(session["user_id"])
    
    user_bookings = list(bookings.find({"user_id": user_id}).sort("booking_date", -1))
    
    for booking in user_bookings:
        if "movie_id" in booking:
            movie = movies_collection.find_one({"_id": booking["movie_id"]})
            if movie:
                booking["title"] = movie["title"]
                booking["type"] = "movie"
        elif "event_id" in booking:
            event = events.find_one({"_id": booking["event_id"]})
            if event:
                booking["title"] = event["title"]
                booking["type"] = "event"
    
    return render_template("my_bookings.html", bookings=user_bookings)

@booking.route("/cancel_booking/<booking_id>")
@login_required
def cancel_booking(booking_id):
    booking = bookings.find_one({"_id": ObjectId(booking_id)})
    
    if not booking:
        flash("Booking not found!", "error")
        return redirect(url_for("booking.my_bookings"))
    
    if str(booking["user_id"]) != session["user_id"]:
        flash("Unauthorized action!", "error")
        return redirect(url_for("booking.my_bookings"))
    
    bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": "cancelled"}}
    )
    
    flash("Booking cancelled successfully!", "success")
    return redirect(url_for("booking.my_bookings"))

@booking.route("/booking_details/<booking_id>")
@login_required
def booking_details(booking_id):
    booking = bookings.find_one({"_id": ObjectId(booking_id)})
    
    if not booking:
        flash("Booking not found!", "error")
        return redirect(url_for("booking.my_bookings"))
    
    if str(booking["user_id"]) != session["user_id"]:
        flash("Unauthorized access!", "error")
        return redirect(url_for("booking.my_bookings"))
    
    details = {}
    
    if "movie_id" in booking:
        details = movies_collection.find_one({"_id": booking["movie_id"]})
        booking["type"] = "movie"
    elif "event_id" in booking:
        details = events.find_one({"_id": booking["event_id"]})
        booking["type"] = "event"
    
    return render_template("booking_details.html", booking=booking, details=details)


@booking.route("/booking_confirmation/<booking_id>")
@login_required
def booking_confirmation(booking_id):
    booking = bookings.find_one({"_id": ObjectId(booking_id)})
    movie = movies_collection.find_one({"_id": booking["movie_id"]})
    
    return render_template(
        "confirmation.html",
        booking=booking,
        movie=movie
    )


