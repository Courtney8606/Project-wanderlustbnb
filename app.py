import os
from flask import Flask, jsonify, request, render_template, url_for, session
from lib import space_repository
from lib.database_connection import get_flask_database_connection
from lib.space_repository import Space, SpaceRepository
from lib.user_repository import UserRepository
from lib.user import User
from flask import redirect


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
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    spaces = space_repository.all()
    return render_template('index.html', spaces=spaces)

# show all properties
@app.route('/spaces', methods=['GET'])
def get_all_spaces():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    spaces = space_repository.all()
    return render_template('spaces/all.html', spaces=spaces) # all.html still pending


# show all properties on specific date
# datetime scares me man

# show specific property
@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_space_by_id(space_id):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    space = space_repository.find(space_id) # assuming the method is called #find
    return render_template('spaces/space.html', space=space)
    
# booking has been successful page
@app.route('/success', methods=['GET'])
def get_successful_booking(space_id):
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    space = space_repository.find(space_id) # assuming the method is called #find
    return render_template('booking/success.html', space=space) # page that says 'your booking at [SPACE] has been successful!


# login page
@app.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html', message="Login")

@app.route('/login', methods=['POST']) # type: ignore
def post_login():
    connection = get_flask_database_connection(app) # set up the database connection
    repository = UserRepository(connection) # this is a placeholder waiting for the user repository class
    username = request.form['username'] 
    password = request.form['password']
    if request.method == "POST":
        user = request.form["username"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("post_login"))

    
# Route for the successful login
@app.route('/login/success')
def login_success():
    return 'Login Successful!'
    
    
    
# signup page
@app.route('/signup', methods=['GET'])
def get_signup_page():
    return render_template('signup.html')
    



@app.route('/signup', methods=['POST'])
def post_signup_page():
    connection = get_flask_database_connection(app) # set up the database connection
    repository = UserRepository(connection) # this is a placeholder waiting for the user repository class
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = request.form["username"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        return render_template("signup.html")
    
# Route for the successful page
@app.route('/signup/success')
def signup_success():
    return 'Sign Up Successful!'
    

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
