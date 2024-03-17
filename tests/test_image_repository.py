from lib.image_repository import ImageRepository
from lib.image import Image


""""
.all() should retrieve all images on the database with their data presented neatly.
"""
def test_get_all_images(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = ImageRepository(db_connection)
    assert repository.all() == [
        #fill in with correct format
        Image(1, 'house1.jpg'),
        Image(2, 'house2.jpg'),
        Image(3, 'house3.jpg'),
        Image(4, 'house4.jpg')
    ]

def test_create_Image(db_connection):
    db_connection.seed("seeds/spaces_table.sql")
    repository = ImageRepository(db_connection)
    image = Image(5, 'house5.jpg')
    repository.create(image)
    images = repository.all()
    assert images[-1] == Image(5, 'house5.jpg')
