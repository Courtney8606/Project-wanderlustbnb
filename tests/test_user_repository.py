from lib.user_repository import UserRepository, User

# test get all users when #all is called

def test_get_all_users(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    assert repository.all() == [
        User(1, 'mrs_dursley', 'Petunia Dursley', 'hatemynephew123'),
        User(2, 'ratatouille', 'Remy Rat', 'kissthecook'),
        User(3, 'montoya', 'Inigo Montoya', 'prepare2die')
    ]

def test_find_user(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    assert repository.find(3) == User(3, 'montoya', 'Inigo Montoya', 'prepare2die')

def test_find_user_by_username(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    assert repository.find_by_username("montoya") == User(3, 'montoya', 'Inigo Montoya', 'prepare2die')

def test_create_user(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    user = User(4, 'She-ra', 'Adora Rainbowfist', 'heycatra1')
    repository.create(user)
    assert repository.all() == [
        User(1, 'mrs_dursley', 'Petunia Dursley', 'hatemynephew123'),
        User(2, 'ratatouille', 'Remy Rat', 'kissthecook'),
        User(3, 'montoya', 'Inigo Montoya', 'prepare2die'),
        User(4, 'She-ra', 'Adora Rainbowfist', 'heycatra1')
    ]

def test_delete_user(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    repository.delete(1)
    assert repository.all() == [
        User(2, 'ratatouille', 'Remy Rat', 'kissthecook'),
        User(3, 'montoya', 'Inigo Montoya', 'prepare2die')
    ]

def test_update_user(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    user = User(2, 'ratatouille', 'Remy the Rat', 'kissthecook')
    repository.update(user)
    assert repository.all() == [
        User(1, 'mrs_dursley', 'Petunia Dursley', 'hatemynephew123'),
        User(3, 'montoya', 'Inigo Montoya', 'prepare2die'),
        User(2, 'ratatouille', 'Remy the Rat', 'kissthecook')
    ]

def test_login(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    username = 'mrs_dursley'
    password = 'hatemynephew123'
    assert repository.login(username, password) == True

def test_wrong_login(db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    repository = UserRepository(db_connection)
    username = 'mrs_dursley'
    password = 'lovemynephew1'
    assert repository.login(username, password) == False
