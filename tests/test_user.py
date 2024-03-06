from lib.user import User

# test user constructs with name, username and password

def test_constructs_user():
    user = User(1, 'She-ra', 'Adora Rainbowfist', 'heycatra1')
    assert user.id == 1
    assert user.username == 'She-ra'
    assert user.name == 'Adora Rainbowfist'
    assert user.password == 'heycatra1'

def test_equality():
    user1 = User(1, 'She-ra', 'Adora Rainbowfist', 'heycatra1')
    user2 = User(1, 'She-ra', 'Adora Rainbowfist', 'heycatra1')
    assert user1 == user2

def test_formatting():
    user = User(1, 'She-ra', 'Adora Rainbowfist', 'heycatra1')
    assert str(user) == 'User(1, She-ra, Adora Rainbowfist, heycatra1)'