from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from datetime import datetime
from routes.database import users
from functools import wraps

auth = Blueprint('auth', __name__)

# ✅ Sign In Route - Ensures correct password checking
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.find_one({"email": email})

        if user:
            stored_password = user.get('password', '')

            if not stored_password:  
                flash('Account error: No password found. Please reset your password.', 'error')
                return redirect(url_for('auth.signin'))

            # ✅ Correct password validation
            if check_password_hash(stored_password, password):
                session['user_id'] = str(user['_id'])
                session['user_name'] = user['name']
                flash('Successfully logged in!', 'success')
                return redirect(url_for('general.index'))

        flash('Invalid email or password', 'error')
    
    return render_template('signin.html')


# ✅ Registration Route - Ensures proper password hashing
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # ✅ Prevent duplicate accounts
        if users.find_one({"email": email}):
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))

        # ✅ Ensure password is not empty
        if not password:
            flash('Password cannot be empty!', 'error')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)  # ✅ Correct hashing method

        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,  # ✅ Stored as a STRING
            "date_joined": datetime.now(),
            "preferences": {
                "favorite_genres": [],
                "notification_enabled": True
            }
        }

        users.insert_one(user_data)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.signin'))

    return render_template('register.html')


# ✅ Logout Route
@auth.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('general.index'))


# ✅ Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('auth.signin'))
        return f(*args, **kwargs)
    return decorated_function
