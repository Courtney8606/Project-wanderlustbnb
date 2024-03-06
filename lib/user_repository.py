from lib.user import User

class UserRepository():
    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            row = User(row["id"], row["username"], row["name"], row["password"])
            users.append(row)
        return users
    
    def find(self, user_id):
        rows = self._connection.execute("SELECT * FROM users WHERE id = %s", [user_id])
        row = rows[0]
        return User(row["id"], row["username"], row["name"], row["password"])
    
    def create(self, user):
        self._connection.execute('INSERT INTO users (username, name, password) VALUES (%s, %s, %s)', [user.username, user.name, user.password])

    def delete(self, user_id):
        self._connection.execute('DELETE FROM users WHERE id = %s', [user_id])

    def update(self, user):
        self._connection.execute('UPDATE users SET username = %s, name = %s, password = %s WHERE id = %s', [user.username, user.name, user.password, user.id])

    def login(self, username, password):
        user = self._connection.execute('SELECT * FROM users WHERE username = %s AND password =%s', [username, password])
        if user:
            return True
        else:
            return False