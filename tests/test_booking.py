from lib.booking import Booking
import datetime

def test_constructs_booking_object():
    example = Booking(1, 1, "2024-05-12", 1, 2)
    assert example.id == 1
    assert example.space_id == 1
    assert example.date_booked == "2024-05-12"
    assert example.userid_booker == 1
    assert example.userid_approver == 2

def test_equality():
    booking1 = Booking(1, 1, datetime.date(2024, 5, 12), 1, 2)
    booking2 = Booking(1, 1, datetime.date(2024, 5, 12), 1, 2)
    assert booking1 == booking2

def test_formatting():
    booking = Booking(1, 1, datetime.date(2024, 5, 12), 1, 2)
    assert str(booking) == "Booking(1, 1, 2024-05-12, 1, 2)"