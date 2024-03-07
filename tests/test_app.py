from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository, User

# Tests for your routes go here

"""
We can render the index page
"""
# def test_get_index(page, test_web_address):
#     # We load a virtual browser and navigate to the /index page
#     page.goto(f"http://{test_web_address}/index")

#     # We look at the <p> tag
#     title = page.locator("Title")

#    # We assert that it has the text "This is the homepage."
#     expect(title).to_have_text("MakersBnB")

# check /spaces route works

def test_get_all_spaces(page, test_web_address, db_connection, web_client):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/spaces')
    response = web_client.get('/spaces')
    assert response.status_code == 200
    div_tags = page.locator('div')
    expect(div_tags).to_have_text([
        'Name: Wizarding Cupboard\nLocation: London',
        'Name: Amore Penthouse\nLocation: Paris',
        'Name: Paella Place\nLocation: Madrid',
        'Name: Mi Casa\nLocation: Madrid'
    ])

# check each individual space on /spaces/<space_id>

def test_get_individual_space_1(page, test_web_address, db_connection, space_id=1):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/spaces/{space_id}')
    header = page.locator('h1')
    space_info = page.locator('p')
    expect(header).to_have_text('Wizarding Cupboard')
    expect(space_info).to_have_text('Location: London\nDescription: A cosy room under the stairs. Comes with complementary spiders.\nPrice per night: 50.0')

def test_get_individual_space_2(page, test_web_address, db_connection, space_id=2):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/spaces/{space_id}')
    header = page.locator('h1')
    space_info = page.locator('p')
    expect(header).to_have_text('Amore Penthouse')
    expect(space_info).to_have_text('Location: Paris\nDescription: Within view of the Eiffel Tower, this penthouse is your parisian dream.\nPrice per night: 87.0')

def test_login_page(page, test_web_address, db_connection):
        db_connection.seed('seeds/spaces_table.sql')
        page.goto(f'http://{test_web_address}/login')
        page.fill("input[name='username']", "montoya")
        page.fill("input[name='password']", "prepare2die")
        page.click("input[type='submit']")
        welcome_message = page.locator('h3')
        expect(welcome_message).to_have_text('Welcome, montoya, you have successfully logged in.')

def test_failed_login(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/login')
    page.fill("input[name='username']", "montoya")
    page.fill("input[name='password']", "prepare2live")
    page.click("input[type='submit']")
    error_message = page.locator('p')
    expect(error_message).to_have_text("Username or password do not match, please try again.\nDon't have an account? Sign up!")

def test_failed_signup(page, test_web_address, db_connection):
        db_connection.seed('seeds/spaces_table.sql')
        page.goto(f'http://{test_web_address}/signup')
        page.fill("input[name='username']", "lord_snow")
        page.fill("input[name='name']", "Jon Snow")
        page.fill("input[name='password']", "ghost")
        page.fill("input[name='repeat_password']", "ghosty")
        page.click("input[type='submit']")
        error_message = page.locator('p')
        expect(error_message).to_have_text("Passwords do not match. Please try again.")

def test_successful_signup(page, test_web_address, db_connection):
        db_connection.seed('seeds/spaces_table.sql')
        page.goto(f'http://{test_web_address}/signup')
        page.fill("input[name='username']", "lord_snow")
        page.fill("input[name='name']", "Jon Snow")
        page.fill("input[name='password']", "ghost")
        page.fill("input[name='repeat_password']", "ghost")
        page.click("input[type='submit']")
        user_repository = UserRepository(db_connection)
        assert user_repository.all() == [
            User(1, 'mrs_dursley', 'Petunia Dursley', 'hatemynephew123'),
            User(2, 'ratatouille', 'Remy Rat', 'kissthecook'),
            User(3, 'montoya', 'Inigo Montoya', 'prepare2die'),
            User(4, 'lord_snow', 'Jon Snow', 'ghost')
        ]
        welcome_message = page.locator('h3')
        expect(welcome_message).to_have_text('Welcome, lord_snow, you have successfully signed up.')
