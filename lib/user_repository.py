from lib.user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def find(self, email):
        rows = self._connection.execute("SELECT * FROM users WHERE email = %s", [email])
        row = rows[0]
        return User(row['username'],row['name'],row['password'],)
    