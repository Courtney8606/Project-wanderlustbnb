from lib.booking import Booking
from lib.space import Space
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

def test_get_all_bookings_by_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    assert repository.all_by_space_id(4) == [
        Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, False),
    ]

def test_create_booking(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    booking = Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, False)
    repository.create(booking)
    Bookings = repository.all()
    assert Bookings[-1] == Booking(4, 4, datetime.date(2024, 7, 12), 1, 3, False)

def test_unapproved_bookings_by_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.unapproved_bookings_by_space(3, 4)
    assert result == [
        Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, False),
    ]

def test_unapproved_bookings_by_space_when_none(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.unapproved_bookings_by_space(1, 1)
    assert result == []

def test_approved_bookings_by_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.approved_bookings_by_space(2, 2)
    assert result == [
        Booking(3, 2, datetime.date(2024, 7, 12), 1, 2, True)
    ]

def test_unapproved_bookings_by_user_id(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.unapproved_bookings_by_user_id(3)
    assert result == [
        Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, False),
        Booking(2, 3, datetime.date(2024, 7, 12), 2, 3, False),
    ]

def test_approved_bookings_by_user_id(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.approved_bookings_by_user_id(2)
    assert result == [
        Booking(3, 2, datetime.date(2024, 7, 12), 1, 2, True)
    ]

def test_update_approval(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    booking_id = 1
    repository.update_approval(booking_id)
    result = repository.approved_bookings_by_space(3, 4)
    assert result == [
        Booking(1, 4, datetime.date(2024, 7, 12), 1, 3, True)
    ]

def test_return_list_of_approved_bookings_string_for_a_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    result = repository.approved_bookings_string(2)
    assert result == [
        '2024-07-12'
    ]

def test_delete_booking(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = BookingRepository(db_connection)
    repository.delete(1)
    bookings = repository.all()
    assert bookings == [
        Booking(2, 3, datetime.date(2024, 7, 12), 2, 3, False),
        Booking(3, 2, datetime.date(2024, 7, 12), 1, 2, True)
    ]
