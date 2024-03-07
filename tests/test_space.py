from lib.space import Space
import datetime

""""
constructs space object with name, location, description, user id
"""
def test_constructs_space_object():
    example = Space(1, "appt 1", "london", 50.00, "jbvsdjh", 1)
    assert example.id == 1
    assert example.name == "appt 1"
    assert example.location == "london"
    assert example.price == 50.00
    assert example.description == "jbvsdjh"
    assert example.user_id == 1

def test_equality():
    space1 = Space(4, 'Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3)
    space2 = Space(4, 'Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3)
    assert space1 == space2

    # datetime.date(2023, 6, 20)

def test_formatting():
    space = Space(4, 'Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3)
    assert str(space) == "Space(4, Mi Casa, Madrid, 45.5, Es tu Casa., 3)"

    