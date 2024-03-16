from lib.image import Image


class ImageRepository:
    # We initialise with a database connection
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

    # # Find a single book by its id
    # def find(self, book_id):
    #     rows = self._connection.execute(
    #         'SELECT * from books WHERE id = %s', [book_id])
    #     row = rows[0]
    #     return Book(row["id"], row["title"], row["author_name"])

    # Upload new image
    def create(self, image):
        self._connection.execute('INSERT INTO upload (title) VALUES (%s)', [image.title])


    # # Delete a book by its id
    # def delete(self, book_id):
    #     self._connection.execute(
    #         'DELETE FROM books WHERE id = %s', [book_id])
    #     return None
