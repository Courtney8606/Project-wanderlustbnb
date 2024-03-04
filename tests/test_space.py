from lib.space import Space

""""
constructs space object with name, date_booked, location, description, user id
"""
def test_constructs_space_object():
    example = Space(1, "appt 1", "2024-05-12", "london", 50.00, "jbvsdjh", 1)
    assert example.id == 1
    assert example.name == "appt 1"
    assert example.date_booked == "2024-05-12"
    assert example.location == "london"
    assert example.price == 50.00
    assert example.description == "jbvsdjh"
    assert example.user_id == 1



    