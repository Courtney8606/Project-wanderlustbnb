import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from lib import space_repository
from lib.database_connection import get_flask_database_connection
from lib.space_repository import Space, SpaceRepository
from lib.booking_repository import BookingRepository
from lib.user_repository import UserRepository
from lib.booking import Booking
from lib.user import User
from lib.space import Space
from flask import redirect


# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    spaces = space_repository.all()
    return render_template('index.html', spaces=spaces)

# show all properties on specific date
# datetime scares me man

# show specific property
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_space_by_id(space_id):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    space = space_repository.find(space_id) # assuming the method is called #find
    return render_template('spaces/space.html', space=space)
    
# # booking has been successful page
# @app.route('/success', methods=['GET'])
# def get_successful_booking(space_id):
#     connection = get_flask_database_connection(app)
#     space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
#     space = space_repository.find(space_id) # assuming the method is called #find
#     return render_template('booking/success.html', space=space) # page that says 'your booking at [SPACE] has been successful!

# User bookings reviewed by approver
@app.route('/users/<int:user_id>/requests', methods=['GET'])
def get_unapproved_bookings(user_id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    unapproved = booking_repository.unapproved_bookings(user_id)
    return render_template('requests.html', unapproved=unapproved)

# User approves a booking
@app.route('/approvebooking', methods=['POST'])
def approve_booking():
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    booking_id = request.form['booking_id']
    approver_id = request.form['approver_id']
    booking_repository.update_approval(booking_id)
    return redirect(f'/users/{approver_id}/requests')


# Create a new booking request
@app.route('/spaces/space_id', methods=['POST'])
def create_booking():
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    date_booked = request.form['date_booked']
    space_id = request.form['space_id']
    userid_approver = request.form['approver_id']
    userid_booker = 1
    approved = False
    booking = Booking(None, space_id, date_booked, userid_booker, userid_approver, approved)
    repository.create(booking)
    return render_template('successfulbooking.html')


# login page
@app.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html', message="Login")

@app.route('/login', methods=['POST']) # type: ignore
def post_login():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection)
    username = request.form['username'] # this 
    password = request.form['password']
    
    
# signup page
@app.route('/signup', methods=['GET'])
def get_signup_page():
    return render_template('signup.html')
    



@app.route('/signup', methods=['POST'])
def post_signup_page():
    connection = get_flask_database_connection(app) # set up the database connection
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        user = User(username, name,  password)
        return redirect(url_for('login_page'))
    return render_template('signup.html') 
        
    
    


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
