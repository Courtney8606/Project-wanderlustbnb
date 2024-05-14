Welcome to WanderlustBnB, a Python web app inspired by Airbnb. While originally a group project, I've significantly expanded it individually, focusing on delivering an array of new features to enhance the user experience. 

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