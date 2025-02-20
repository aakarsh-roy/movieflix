from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from bson import ObjectId
from routes.database import users, movies_collection
from routes.auth import login_required

user = Blueprint("user", __name__)

@user.route("/profile")
@login_required
def profile():
    user_data = users.find_one({"_id": ObjectId(session["user_id"])})
    
    if not user_data:
        flash("User not found!", "error")
        return redirect(url_for("auth.signin"))
    
    return render_template("profile.html", user=user_data)

@user.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    user_id = ObjectId(session["user_id"])
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        favorite_genres = request.form.getlist("favorite_genres")
        notifications_enabled = bool(request.form.get("notifications"))

        users.update_one(
            {"_id": user_id},
            {"$set": {
                "name": name,
                "email": email,
                "preferences.favorite_genres": favorite_genres,
                "preferences.notification_enabled": notifications_enabled
            }}
        )
        
        flash("Settings updated successfully!", "success")
        return redirect(url_for("user.settings"))
    
    user_data = users.find_one({"_id": user_id})
    genres = movies_collection.distinct("genre")
    
    return render_template("settings.html", user=user_data, genres=genres)
