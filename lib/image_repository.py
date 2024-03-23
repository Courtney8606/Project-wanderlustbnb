from lib.image import Image

class ImageRepository:
    # Initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all images
    def all(self):
        rows = self._connection.execute('SELECT * from upload')
        images = []
        for row in rows:
            item = Image(row["id"], row["title"])
            images.append(item)
        return images

    # Upload new image
    def create(self, image):
        self._connection.execute('INSERT INTO upload (title) VALUES (%s)', [image.title])
    
    #Update an image
    def update(self, image):
        self._connection.execute('UPDATE upload SET title = %s WHERE id = %s', [image.title, image.id])
        