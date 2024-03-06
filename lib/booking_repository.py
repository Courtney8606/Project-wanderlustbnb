from lib.booking import Booking

class BookingRepository():
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * from bookings')
        bookings = []
        for row in rows:
            row = Booking(row["id"], row["space_id"], row["date_booked"], row["userid_booker"], row["userid_approver"])
            bookings.append(row)
        return bookings

    def create(self, booking):
        self._connection.execute('INSERT INTO bookings (space_id, date_booked, userid_booker, userid_approver) VALUES (%s, %s, %s, %s)', [booking.space_id, booking.date_booked, booking.userid_booker, booking.userid_approver])
        return None

    def delete(self, booking_id):
        self._connection.execute('DELETE FROM bookings WHERE id = %s', [booking_id])
        return None

    # def find(self, id):
    #     rows = self._connection.execute("SELECT * FROM spaces WHERE id = %s", [id])
    #     row = rows[0]
    #     return Space(row["id"], row["name"], row["booking_date"], row["location"], row["price"], row["description"], row["user_id"])
    
    # def update(self, space):
    #     self._connection.execute('UPDATE spaces SET name = %s, booking_date = %s, location = %s, price = %s, description = %s, user_id = %s WHERE id = %s', [space.name, space.booking_date, space.location, space.price, space.description, space.user_id, space.id])
