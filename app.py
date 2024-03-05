import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

# show all properties
@app.route('/spaces', methods=['GET'])
def get_all_spaces():
    connection = get_flask_database_connection(app)
    space_repository = SpaceRepository(connection) # this is a placeholder waiting for the space repository class
    all_spaces = space_repository.all()
    return render_template('all.html', spaces=all_spaces) # all.html still pending


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

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
