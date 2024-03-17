from lib.image import Image

""""
constructs space object with name, location, description, user id
"""
def test_constructs_space_object():
    example = Image(1, 'house1.jpg')
    assert example.title == 'house1.jpg'

def test_equality():
    image1 = Image(4, 'house4.jpg')
    image2 = Image(4, 'house4.jpg')
    assert image1 == image2

def test_formatting():
    image = Image(4,'house4.jpg')
    assert str(image) == "Image(4, house4.jpg)"

    