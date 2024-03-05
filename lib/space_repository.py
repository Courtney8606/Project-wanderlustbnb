from lib.space import Space

class SpaceRepository():
    def __init__(self, connection):
        self._connection = connection
    

    def all(self):
        rows = self._connection.execute('SELECT * from spaces')
        spaces = []
        for row in rows:
            print(row)
            row = Space(row["id"], row["name"], row["booking_date"], row["location"], row["price"], row["description"], row["user_id"])
            spaces.append(row)
        return spaces
    

    def find(self):
        pass







    def create(self, space):
        self._connection.execute('INSERT INTO spaces (name, booking_date, location, price, description, user_id) VALUES (%s, %s, %s, %s, %s, %s)', [space.name, space.booking_date, space.location, space.price, space.description, space.user_id])
        return None







    def delete(self, space):
        self._connection.execute('DELETE FROM spaces WHERE id = %s', [space.id])
        return None
