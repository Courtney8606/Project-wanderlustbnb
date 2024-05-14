## WanderlustBnB

Welcome to WanderlustBnB, a Python web app inspired by Airbnb allowing users to either search for and book holiday properties as a Guest, or manage property listings as a Host. While originally a group project, I've been excited to take this project forward and significantly expanded it individually, delivering an array of new features to enhance the user experience. 

# Key Features

1. Ability to filter your property search by availability.
2. Integrated DateTime booking calendar with any confirmed booking dates disabled within the calendar for that property.
3. Ability to manage all properties and bookings via a Host account, including creating a new property listing (with image upload), updating a property's details, deleting a property, approving or rejecting booking requests, and reviewing confirmed bookings. 
4. Ability to navigate to a Guest account, to review all confirmed or pending booking requests.
5. In-app notifications for any newly approved booking requests. 

# Installation instructions

These instructions are for macOS, and it is assumed that that the following are already installed:

* pipenv
* python (if you use python3 or any other command incorporating a version number, you may need to amend instructions accordingly)
* PostgreSQL 

After cloning the repository, using the CLI, change into the top-level directory of the locally cloned version. Then execute the following commands in sequence:

**Install any dependencies and set up your virtual environment**
* pipenv install 
(ensure Flask, playwright and psycopg are installed)

**Activate your virtual environment**
* pipenv shell

**Create a test and development database**
* createdb wanderlustbnb
* createdb wanderlustbnb_test

**Seed your databases**
* psql wanderlustbnb < seeds/spaces_table.sql
* psql wanderlustbnb_test < seeds/spaces_table.sql

**Change the UPLOAD_FOLDER path in app.py to a relevant local path /*your*/*path*/*here*/Project-wanderlustbnb/static/uploads/'**

**Run the app**
; python app.py

At this stage, the back-end server should be running. Open the following url in your browser: 

http://localhost:5001

**You can run the tests with the following command within the virtual environment**
* pytest 