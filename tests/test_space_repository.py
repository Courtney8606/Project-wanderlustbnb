from lib.space_repository import SpaceRepository
from lib.space import Space
import datetime
from lib.image import Image

""""
.all()
attribute should retrieve all spaces on the database with their data presented neatly.

space(1, "appt1", ...)

"""
def test_get_all_spaces(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = SpaceRepository(db_connection)
    assert repository.all() == [
        #fill in with correct format
        Space(1, 'Wizarding Cupboard', 'London', 50.00, 'A cosy room under the stairs. Comes with complementary spiders.', 1, 'house1.jpg'),
        Space(2, 'Amore Penthouse', 'Paris', 87.00, 'Within view of the Eiffel Tower, this penthouse is your parisian dream.', 2, 'house2.jpg'),
        Space(3, 'Paella Place', 'Madrid', 31.59, 'Eat paella and sleep.', 3, 'house3.jpg'),
        Space(4, 'Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3, 'house4.jpg'),
    ]

def test_find_spaces_by_user_id(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = SpaceRepository(db_connection)
    assert repository.return_all_user_id(3) == [
        Space(3, 'Paella Place', 'Madrid', 31.59, 'Eat paella and sleep.', 3, 'house3.jpg'),
        Space(4, 'Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3, 'house4.jpg'),
    ]

"""
When I call .find() on the SpaceRepository with an id
I get the space corresponding to that id back
"""
def test_find_one_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = SpaceRepository(db_connection)
    result = repository.find(3)
    assert result == Space(3,  'Paella Place', 'Madrid', 31.59, 'Eat paella and sleep.', 3, 'house3.jpg')


def test_create_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = SpaceRepository(db_connection)
    image = Image(None, 'house5.jpg')
    space = Space(5, 'House', 'London', 75.50, 'This is a house', 3, image.title)
    repository.create(space)
    spaces = repository.all()
    assert spaces[-1] == Space(5, 'House', 'London', 75.50, 'This is a house', 3, 'house5.jpg')

def test_delete_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = SpaceRepository(db_connection)
    repository.delete(1)
    spaces = repository.all()
    assert spaces == [
        Space(2, 'Amore Penthouse', 'Paris', 87.00, 'Within view of the Eiffel Tower, this penthouse is your parisian dream.', 2, 'house2.jpg'),
        Space(3, 'Paella Place', 'Madrid', 31.59, 'Eat paella and sleep.', 3, 'house3.jpg'),
        Space(4, 'Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3, 'house4.jpg')
    ]

def test_update_space(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = SpaceRepository(db_connection)
    space = Space(1, 'Cupboard under the stairs', 'London', 50.00, 'A cosy room under the stairs. Comes with complementary spiders.', 1, 'house1.jpg')
    repository.update(space)
    result = repository.all()
    assert result == [
        Space(2, 'Amore Penthouse', 'Paris', 87.00, 'Within view of the Eiffel Tower, this penthouse is your parisian dream.', 2, 'house2.jpg'),
        Space(3, 'Paella Place', 'Madrid', 31.59, 'Eat paella and sleep.', 3, 'house3.jpg'),
        Space(4, 'Mi Casa', 'Madrid', 45.50, 'Es tu Casa.', 3, 'house4.jpg'),
        Space(1, 'Cupboard under the stairs', 'London', 50.00, 'A cosy room under the stairs. Comes with complementary spiders.', 1, 'house1.jpg')
    ]
