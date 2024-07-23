## WanderlustBnB

Welcome to WanderlustBnB, a Python web app inspired by Airbnb allowing users to search for and book holiday properties as a Guest, or manage property listings as a Host. While originally a group project, I've been excited to take this project forward and significantly expanded it individually, delivering an array of new features to enhance the user experience.

# Key Features

1. Seamless Stripe Integration: Enables users to securely pay for confirmed property bookings directly through the website.
2. Advanced Search Filters: Allows users to filter property searches based on real-time property availability, ensuring efficient and accurate search results.
3. Dynamic Booking Calendar: Integrated DateTime booking calendar automatically disables dates for already confirmed bookings, providing an intuitive and error-free booking experience.
4. Comprehensive Host Management: Hosts can manage all aspects of their properties and bookings through their accounts. This includes creating new property listings with image uploads, updating property details, deleting properties, approving or rejecting booking requests, and reviewing confirmed bookings.
5. User-Friendly Guest Accounts: Guests can easily navigate their accounts to review their bookings and make payments for approved bookings, ensuring a smooth user experience.
6. In-App Notifications: Real-time notifications alert users of any newly approved booking requests, keeping them informed and engaged.

# Installation instructions

These instructions are for macOS, and it is assumed that that the following are already installed:

- pipenv
- python (if you use python3 or any other command incorporating a version number, you may need to amend instructions accordingly)
- PostgreSQL

After cloning the repository, using the CLI, change into the top-level directory of the locally cloned version. Then execute the following commands in sequence:

**Install any dependencies and set up your virtual environment**

- pipenv install
  (ensure Flask, playwright and psycopg are installed)

**Activate your virtual environment**

- pipenv shell

**Create a test and development database**

- createdb wanderlustbnb
- createdb wanderlustbnb_test

**Seed your databases**

- psql wanderlustbnb < seeds/spaces_table.sql
- psql wanderlustbnb_test < seeds/spaces_table.sql

**Change the UPLOAD*FOLDER path in app.py to a relevant local path /\_your*/_path_/_here_/Project-wanderlustbnb/static/uploads/'**

**Run the app**
; python app.py

At this stage, the back-end server should be running. Open the following url in your browser:

http://localhost:5001

**You can run the tests with the following command within the virtual environment**

- pytest
