import os
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

import psycopg2
import psycopg2.extras


# Creating a new Flask app
app = Flask(__name__, template_folder='.')
app.secret_key = "tangerine"

# File upload setup

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# == Routes ==

# GET /index - Returns the homepage
# http://localhost:5000/index

@app.route('/index', methods=['GET'])
def get_index():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    spaces = space_repository.all()
    return render_template('index.html', spaces=spaces)

# Returns a property by space.id
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_space_by_id(space_id):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)
    user_repository = UserRepository(connection)
    username = session.get('user')
    user = user_repository.find_by_username(username)
    user_id = user.id
    booking_repository = BookingRepository(connection)
    bookings = booking_repository.approved_bookings_string(user_id)
    return render_template('space.html', space=space, bookings=bookings)
    
# Returns user account page
@app.route('/account', methods=['GET'])
def get_account_page():
    return render_template('account.html')

# Returns Host account page with a list of active properties by user id
@app.route('/host', methods=['GET'])
def get_host_page():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    user_repository = UserRepository(connection)
    username = session.get('user')
    user = user_repository.find_by_username(username)
    user_id = user.id
    spaces = space_repository.return_all_user_id(user_id)
    return render_template('host.html', spaces=spaces)

# Returns Guest Account page to review own holiday bookings by user id
@app.route('/guest', methods=['GET'])
def get_unapproved_and_approved_bookings():
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    user_repository = UserRepository(connection)
    username = session.get('user')
    user = user_repository.find_by_username(username)
    user_id = user.id
    unapproved = booking_repository.unapproved_bookings_by_user_id(user_id)
    approved = booking_repository.approved_bookings_by_user_id(user_id)
    space = spaces_repository.find_by_user_id(user_id)
    return render_template('guest.html', unapproved=unapproved, approved=approved, space=space)

# Returns Host pending and confirmed bookings by space id 

@app.route('/user/requests/<space_name>/<int:space_id>', methods=['GET'])
def get_unapproved_and_approved_bookings_by_space(space_name, space_id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    user_repository = UserRepository(connection)
    username = session.get('user')
    user = user_repository.find_by_username(username)
    user_id = user.id
    unapproved = booking_repository.unapproved_bookings_by_space(user_id, space_id)
    approved = booking_repository.approved_bookings_by_space(user_id, space_id)
    space = spaces_repository.find(space_id)
    return render_template('requests.html', unapproved=unapproved, approved=approved, space=space)

# Host approves a booking
@app.route('/approvebooking', methods=['POST'])
def approve_booking():
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    booking_id = request.form['booking_id']
    space_id = request.form['space_id']
    booking_repository.update_approval(booking_id)
    space = spaces_repository.find(space_id)
    return redirect(url_for('get_unapproved_and_approved_bookings_by_space', space_name=space.name, space_id=space.id))

# Create a new booking request
@app.route('/spaces/booking', methods=['POST'])
def create_booking():
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    user_repository = UserRepository(connection)
    username = session.get('user')
    date_booked = request.form['date_booked']
    userid_approver = request.form['approver_id']
    space_id = request.form['space_id']
    user = user_repository.find_by_username(username)
    userid_booker = user.id
    approved = False
    booking = Booking(None, space_id, date_booked, userid_booker, userid_approver, approved)
    repository.create(booking)
    return render_template('successfulbooking.html')

# Host Reject a booking
@app.route('/reject/<int:booking_id>', methods=['POST'])
def reject_booking(booking_id):
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    booking_id = request.form['booking_id']
    space_id = request.form['space_id']
    repository.delete(booking_id)
    space = spaces_repository.find(space_id)
    return redirect(url_for('get_unapproved_and_approved_bookings_by_space', space_name=space.name, space_id=space.id))
    
# Returns form to create a new property listing
@app.route('/new', methods=['GET'])
def get_listing_page():
    return render_template('createlisting.html')

# Creates a new property listing and updates all()
@app.route('/index', methods=['POST'])
def create_a_listing():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    repository = ImageRepository(connection)
    user_repository = UserRepository(connection)
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
        repository.create(image)
        flash('Image successfully loaded and displayed below')
    username = session.get('user')
    user = user_repository.find_by_username(username)
    user_id = user.id
    space = Space(None, name, location, price, description, user_id, filename)
    space_repository.create(space)
    return redirect('/index')

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
    session['user'] = username
    #session['user_id'] = user_repository.find_by_username(username)
    if user_repository.login(username, password) == False:
        error_message = 'Username or password do not match, please try again.'
        signup_prompt = "Don't have an account? Sign up!"
        return render_template('login.html', error_message=error_message, signup_prompt=signup_prompt)
    else:
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
    session['user'] = username
    #session['user_id'] = user_repository.find_by_username(username)
    if password != repeat_password:
        return render_template('signup.html', error_message='Passwords do not match. Please try again.')
    else:
        user = User(None, username, name, password)
        user_repository.create(user)
        return redirect('/index')

# Debug route to session user

@app.route('/debug')
def debug_session():
    session_user = session.get('user')
    return f"Session User: {session_user}"


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
