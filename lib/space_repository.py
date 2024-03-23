from lib.space import Space

class SpaceRepository():
    # Initialise with a database connection
    def __init__(self, connection):
        self._connection = connection
    
    # Return all property listings
    def all(self):
        rows = self._connection.execute('SELECT * from spaces')
        spaces = []
        for row in rows:
            row = Space(row["id"], row["name"], row["location"], row["price"], row["description"], row["user_id"], row["image_title"])
            spaces.append(row)
        return spaces
    
    # Return all property listings by user
    def return_all_user_id(self, user_id):
        rows = self._connection.execute("SELECT * FROM spaces WHERE user_id = %s", [user_id])
        spaces = []
        for row in rows:
            row = Space(row["id"], row["name"], row["location"], row["price"], row["description"], row["user_id"], row["image_title"])
            spaces.append(row)
        return spaces

    # Return specific property listing by id
    def find(self, id):
        rows = self._connection.execute("SELECT * FROM spaces WHERE id = %s", [id])
        row = rows[0]
        return Space(row["id"], row["name"], row["location"], row["price"], row["description"], row["user_id"], row["image_title"])

    # Return specific property listing by user id
    def find_by_user_id(self, user_id):
        rows = self._connection.execute("SELECT * FROM spaces WHERE user_id = %s", [user_id])
        row = rows[0]
        return Space(row["id"], row["name"], row["location"], row["price"], row["description"], row["user_id"], row["image_title"])
    
    # Create a new property listing
    def create(self, space):
        self._connection.execute('INSERT INTO spaces (name, location, price, description, user_id, image_title) VALUES (%s, %s, %s, %s, %s, %s)', [space.name, space.location, space.price, space.description, space.user_id, space.image_title])
        return None
    
    # Delete a property listing
    def delete(self, space_id):
        self._connection.execute('DELETE FROM spaces WHERE id = %s', [space_id])
        return None
    
    # Update a property listing
    def update(self, space):
        self._connection.execute('UPDATE spaces SET name = %s, location = %s, price = %s, description = %s, user_id = %s, image_title = %s WHERE id = %s', [space.name, space.location, space.price, space.description, space.user_id, space.image_title, space.id])
        