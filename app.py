import os

from flask import Flask, jsonify, request, render_template, url_for, session, redirect
from lib import space_repository
from lib.database_connection import get_flask_database_connection
from lib.space_repository import Space, SpaceRepository
from lib.booking_repository import BookingRepository
from lib.user_repository import UserRepository
from lib.booking import Booking
from lib.user import User
from lib.space import Space



# Create a new Flask app
app = Flask(__name__)
app.secret_key = "tangerine"

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    spaces = space_repository.all()
    return render_template('index.html', spaces=spaces)


# show all properties on specific date
# datetime scares me man

# show specific property
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_space_by_id(space_id):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    space = space_repository.find(space_id)
    user_repository = UserRepository(connection)
    #username = session.get('user')
    #user = user_repository.find_by_username(username)
    user_id = 2
    booking_repository = BookingRepository(connection)
    bookings = booking_repository.approved_bookings_string(user_id)
    return render_template('spaces/space.html', space=space, bookings=bookings)
    
# # booking has been successful page
# @app.route('/success', methods=['GET'])
# def get_successful_booking(space_id):
#     connection = get_flask_database_connection(app)
#     space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
#     space = space_repository.find(space_id) # assuming the method is called #find
#     return render_template('booking/success.html', space=space) # page that says 'your booking at [SPACE] has been successful!

# User bookings reviewed by approver
@app.route('/user/requests', methods=['GET'])
def get_unapproved_and_approved_bookings():
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    spaces_repository = SpaceRepository(connection)
    user_repository = UserRepository(connection)
    username = session.get('user')
    user = user_repository.find_by_username(username)
    user_id = user.id
    unapproved = booking_repository.unapproved_bookings(user_id)
    approved = booking_repository.approved_bookings(user_id)
    space = spaces_repository.find_by_user_id(user_id)
    return render_template('requests.html', unapproved=unapproved, approved=approved, space=space)

# User approves a booking
@app.route('/approvebooking', methods=['POST'])
def approve_booking():
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    booking_id = request.form['booking_id']
    approver_id = request.form['approver_id']
    booking_repository.update_approval(booking_id)
    return redirect(f'/user/requests')

@app.route('/debug')
def debug_session():
    session_user = session.get('user')
    return f"Session User: {session_user}"

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



# login page
@app.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
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
    
    

    
#create space
@app.route('/new', methods=['GET'])
def get_listing_page():
    return render_template('createlisting.html')

@app.route('/index', methods=['POST'])
def create_a_listing():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    location = request.form['location']
    #booking_start = request.form['booking_start']
    #booking_end = request.form['booking_end']
    user_id = 1
    space = Space(None, name, location, price, description, user_id)
    space_repository.create(space)
    return redirect('/index')

# signup page
@app.route('/signup', methods=['GET'])
def get_signup_page():
    return render_template('signup.html')

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


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
