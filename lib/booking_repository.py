from lib.booking import Booking
from datetime import timedelta
import datetime

class BookingRepository():
    # Initialise with a database connection
    def __init__(self, connection):
        self._connection = connection
        self._bookingstoreview = []
    
    # Return all bookings
    def all(self):
        rows = self._connection.execute('SELECT * from bookings')
        bookings = []
        for row in rows:
            row = Booking(row["id"], row["space_id"], row["date_booked"], row["userid_booker"], row["userid_approver"], row["approved"])
            bookings.append(row)
        return bookings
    
    # Return bookings for a particular property
    def all_by_space_id(self, space_id):
        rows = self._connection.execute('SELECT * from bookings WHERE space_id = %s', [space_id])
        bookings = []
        for row in rows:
            row = Booking(row["id"], row["space_id"], row["date_booked"], row["userid_booker"], row["userid_approver"], row["approved"])
            bookings.append(row)
        return bookings

    def all_by_space_id_dates_booked(self, space_id):
        rows = self._connection.execute('SELECT * from bookings WHERE space_id = %s', [space_id])
        bookings = []
        for row in rows:
            date_booked = (str(row["date_booked"]))
            bookings.append(date_booked)
        return bookings
    
    # Create a new booking
    def create(self, booking):
        self._connection.execute('INSERT INTO bookings (space_id, date_booked, userid_booker, userid_approver, approved) VALUES (%s, %s, %s, %s, %s)', [booking.space_id, booking.date_booked, booking.userid_booker, booking.userid_approver, booking.approved])
        return None

    # Delete a booking
    def delete(self, booking_id):
        self._connection.execute('DELETE FROM bookings WHERE id = %s', [booking_id])
        return None

    # Return unapproved bookings by specific property
    def unapproved_bookings_by_space(self, user_id, space_id):
        rows = self._connection.execute('SELECT * from bookings WHERE approved = False AND userid_approver = %s AND space_id = %s', [user_id, space_id])
        bookings = []
        for row in rows:
            row = Booking(row["id"], row["space_id"], row["date_booked"], row["userid_booker"], row["userid_approver"], row["approved"])
            bookings.append(row)
        return bookings

    # Return approved bookings by specific property
    def approved_bookings_by_space(self, user_id, space_id):
        rows = self._connection.execute('SELECT * from bookings WHERE approved = True AND userid_approver = %s AND space_id = %s', [user_id, space_id])
        bookings = []
        for row in rows:
            row = Booking(row["id"], row["space_id"], row["date_booked"], row["userid_booker"], row["userid_approver"], row["approved"])
            bookings.append(row)
        return bookings
    
    # Return approved bookings in a string(datepicker calendar)
    def approved_bookings_string(self, space_id):
        rows = self._connection.execute('SELECT * from bookings WHERE approved = True AND space_id = %s', [space_id])
        bookings = []
        for row in rows:
            date_booked = str(row["date_booked"])
            bookings.append(date_booked)
        return bookings
    
    # Return unapproved bookings by user
    def unapproved_bookings_by_user_id(self, user_id):
        rows = self._connection.execute('SELECT * from bookings WHERE approved = False AND userid_approver = %s', [user_id])
        bookings = []
        for row in rows:
            row = Booking(row["id"], row["space_id"], row["date_booked"], row["userid_booker"], row["userid_approver"], row["approved"])
            bookings.append(row)
        return bookings

    # Return approved bookings by user
    def approved_bookings_by_user_id(self, user_id):
        rows = self._connection.execute('SELECT * from bookings WHERE approved = True AND userid_approver = %s', [user_id])
        bookings = []
        for row in rows:
            row = Booking(row["id"], row["space_id"], row["date_booked"], row["userid_booker"], row["userid_approver"], row["approved"])
            bookings.append(row)
        return bookings

    # Update booking approval state
    def update_approval(self, booking_id):
        self._connection.execute('UPDATE bookings SET approved = True WHERE id = %s', [booking_id])
