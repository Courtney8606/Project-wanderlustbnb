from lib.booking import Booking
from lib.booking_repository import BookingRepository
import datetime

def test_get_all_bookings(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    assert repository.all() == [
        Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, False),
        Booking(2, 3, datetime.date(2024, 7, 12), 2, 3, False),
        Booking(3, 2, datetime.date(2024, 7, 12), 1, 2, True)
    ]
def test_create_booking(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    booking = Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, False)
    repository.create(booking)
    Bookings = repository.all()
    assert Bookings[-1] == Booking(4, 4, datetime.date(2024, 7, 12), 1, 3, False)

def test_unapproved_bookings(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.unapproved_bookings()
    assert result == [
        Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, False),
        Booking(2, 3, datetime.date(2024, 7, 12), 2, 3, False)
    ]

def test_approved_bookings(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.approved_bookings()
    assert result == [
        Booking(3, 2, datetime.date(2024, 7, 12), 1, 2, True)
    ]

def test_update_approval(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    booking = Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, True)
    repository.update_approval(booking)
    result = repository.approved_bookings()
    assert result == [
        Booking(3, 2, datetime.date(2024, 7, 12), 1, 2, True),
        Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, True)
    ]

# """
# When I call .find() on the SpaceRepository with an id
# I get the space corresponding to that id back
# """
# def test_find_one_space(db_connection):
#     db_connection.seed("seeds/spaces_table.sql")
#     repository = SpaceRepository(db_connection)
#     result = repository.find(3)
#     assert result == Space(3,  'Paella Place', datetime.date(2024, 7, 14), 'Madrid', 31.59, 'Eat paella and sleep.', 3)

def test_delete_booking(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    repository.delete(1)
    bookings = repository.all()
    assert bookings == [
        Booking(2, 3, datetime.date(2024, 7, 12), 2, 3, False),
        Booking(3, 2, datetime.date(2024, 7, 12), 1, 2, True)
    ]

# def test_update_space(db_connection):
#     db_connection.seed("seeds/spaces_table.sql")
#     repository = SpaceRepository(db_connection)
#     space = Space(1, 'Cupboard under the stairs', datetime.date(2024, 5, 12), 'London', 50.00, 'A cosy room under the stairs. Comes with complementary spiders.', 1)
#     repository.update(space)
#     result = repository.all()
#     assert result == [
#         Space(2, 'Amore Penthouse', datetime.date(2024, 7, 12), 'Paris', 87.00, 'Within view of the Eiffel Tower, this penthouse is your parisian dream.', 2),
#         Space(3, 'Paella Place', datetime.date(2024, 7, 14), 'Madrid', 31.59, 'Eat paella and sleep.', 3),
#         Space(4, 'Mi Casa', datetime.date(2024, 7, 12), 'Madrid', 45.50, 'Es tu Casa.', 3),
#         Space(1, 'Cupboard under the stairs', datetime.date(2024, 5, 12), 'London', 50.00, 'A cosy room under the stairs. Comes with complementary spiders.', 1)
#     ]