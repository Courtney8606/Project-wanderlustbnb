import os
import logging
from flask import Flask, flash, jsonify, request, render_template, url_for, session, redirect
from lib import space_repository
from lib.database_connection import get_flask_database_connection
from lib.space_repository import Space, SpaceRepository
from lib.booking_repository import BookingRepository
from lib.user_repository import UserRepository
from lib.booking import Booking
from lib.user import User
from lib.space import Space
import urllib.request
from werkzeug.utils import secure_filename
from lib.image_repository import ImageRepository
from lib.image import Image
from functools import wraps

import psycopg2
import psycopg2.extras


# Creating a new Flask app
app = Flask(__name__, template_folder='templates')
app.secret_key = "tangerine"

# File upload setup

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def get_user_id():
    username = session.get('user')
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    user = user_repository.find_by_username(username)
    return user.id


# == Routes ==

# GET /index - Returns the homepage
# http://localhost:5000/

@app.route('/index', methods=['GET'])
@login_required
def get_index():
    connection = get_flask_database_connection(app) 
    space_repository = SpaceRepository(connection)
    spaces = space_repository.all()
    return render_template('index.html', spaces=spaces)

# Returns a property by space id
@app.route('/spaces/<int:space_id>', methods=['GET'])
@login_required
def get_space_by_id(space_id):
    connection = get_flask_database_connection(app)
    user_id = get_user_id()
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)
    booking_repository = BookingRepository(connection)
    bookings = booking_repository.approved_bookings_string(user_id)
    return render_template('space.html', space=space, bookings=bookings)

# Create a new booking request
@app.route('/spaces/booking', methods=['POST'])
@login_required
def create_booking():
    connection = get_flask_database_connection(app)
    userid_booker = get_user_id()
    booking_repository = BookingRepository(connection) 
    date_booked = request.form['date_booked']
    userid_approver = request.form['approver_id']
    space_id = request.form['space_id']
    approved = False
    booking = Booking(None, space_id, date_booked, userid_booker, userid_approver, approved)
    booking_repository.create(booking)
    return render_template('successfulbooking.html')
    
# Returns user account page
@app.route('/account', methods=['GET'])
@login_required
def get_account_page():
    return render_template('account.html')

# Returns Host account page with a list of active properties by user id
@app.route('/host', methods=['GET'])
@login_required
def get_host_page():
    connection = get_flask_database_connection(app)
    user_id = get_user_id()
    space_repository = SpaceRepository(connection)
    spaces = space_repository.return_all_user_id(user_id)
    return render_template('host.html', spaces=spaces)

# Returns Guest Account page to review own holiday bookings by user id
@app.route('/guest', methods=['GET'])
@login_required
def get_unapproved_and_approved_bookings():
    connection = get_flask_database_connection(app)
    user_id = get_user_id()
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    unapproved = booking_repository.unapproved_bookings_by_user_id(user_id)
    approved = booking_repository.approved_bookings_by_user_id(user_id)
    space = spaces_repository.find_by_user_id(user_id)
    return render_template('guest.html', unapproved=unapproved, approved=approved, space=space)

# Returns Host pending and confirmed bookings by space id 

@app.route('/user/requests/<space_name>/<int:space_id>', methods=['GET'])
@login_required
def get_unapproved_and_approved_bookings_by_space(space_name, space_id):
    connection = get_flask_database_connection(app)
    user_id = get_user_id()
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    unapproved = booking_repository.unapproved_bookings_by_space(user_id, space_id)
    approved = booking_repository.approved_bookings_by_space(user_id, space_id)
    space = spaces_repository.find(space_id)
    return render_template('requests.html', unapproved=unapproved, approved=approved, space=space)

# Host approves a booking
@app.route('/approvebooking', methods=['POST'])
@login_required
def approve_booking():
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    booking_id = request.form['booking_id']
    space_id = request.form['space_id']
    booking_repository.update_approval(booking_id)
    space = spaces_repository.find(space_id)
    return redirect(url_for('get_unapproved_and_approved_bookings_by_space', space_name=space.name, space_id=space.id))

# Host Reject a booking
@app.route('/reject/<int:booking_id>', methods=['POST'])
@login_required
def reject_booking(booking_id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    booking_id = request.form['booking_id']
    space_id = request.form['space_id']
    booking_repository.delete(booking_id)
    space = spaces_repository.find(space_id)
    return redirect(url_for('get_unapproved_and_approved_bookings_by_space', space_name=space.name, space_id=space.id))
    
# Returns form to create a new property listing
@app.route('/new', methods=['GET'])
@login_required
def get_listing_page():
    return render_template('createlisting.html')

# Creates a new property listing and updates all()
@app.route('/newlisting', methods=['POST'])
@login_required
def create_a_listing():
    connection = get_flask_database_connection(app)
    user_id = get_user_id()
    space_repository = SpaceRepository(connection)
    image_repository = ImageRepository(connection)
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    location = request.form['location']
    file = request.files['file']
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = Image(None, filename)
        image_repository.create(image)
    space = Space(None, name, location, price, description, user_id, filename)
    space_repository.create(space)
    return redirect('/index')

# Render Update a property listing page
@app.route('/user/update/<space_name>/<int:space_id>', methods=['GET'])
@login_required
def get_space_update_page(space_name, space_id):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)
    return render_template('updateproperty.html', space=space)

# Update a property
@app.route('/updated/<int:space_id>', methods=['GET', 'POST'])
@login_required
def update_property_listing(space_id):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    image_repository = ImageRepository(connection)
    user_id = get_user_id()
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    location = request.form['location']
    file = request.files['file']
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = Image(space_id, filename)
        image_repository.update(image)
    space = Space(space_id, name, location, price, description, user_id, filename)
    space_repository.update(space)
    return redirect('/host')

# Host deletes a space
@app.route('/delete/<int:space_id>', methods=['POST'])
@login_required
def delete_space(space_id):
    connection = get_flask_database_connection(app)
    spaces_repository = SpaceRepository(connection)
    space_id = request.form['space_id']
    spaces_repository.delete(space_id)
    spaces = spaces_repository.all()
    return redirect(url_for('get_host_page', spaces=spaces))

# Renders Login page
@app.route('/', methods=['GET'])
def get_login_page():
    return render_template('login.html')

# User can login
@app.route('/', methods=['POST'])
def post_login():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    username = request.form['username']
    password = request.form['password']
    if user_repository.login(username, password) == False:
        error_message = 'Username or password do not match, please try again.'
        signup_prompt = "Don't have an account? Sign up!"
        return render_template('login.html', error_message=error_message, signup_prompt=signup_prompt)
    else:
        session['user'] = username
        return redirect('/index')
    
# Renders signup page
@app.route('/signup', methods=['GET'])
def get_signup_page():
    return render_template('signup.html')

# User can sign up and login
@app.route('/signup', methods=['POST'])
def post_signup_page():
    connection = get_flask_database_connection(app) 
    user_repository = UserRepository(connection)
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    repeat_password = request.form['repeat_password']
    if password != repeat_password:
        error_message = 'Passwords do not match. Please try again.'
        return render_template('signup.html', error_message=error_message)
    elif password == '':
        error_message = 'You have not entered a password. Please enter a password to set up your account.'
        return render_template('signup.html', error_message=error_message)
    else:
        user = User(None, username, name, password)
        user_repository.create(user)
        session['user'] = username
        return redirect('/index')
    
@app.route('/logout', methods=['GET'])
@login_required
def log_out():
    session.pop('user', None)
    return redirect('/')

# Debug route to session user

@app.route('/debug')
@login_required
def debug_session():
    session_user = session.get('user')
    return f"Session User: {session_user}"


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
