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

    
def test_post_a_listing(db_connection, web_client):
    db_connection.seed("seeds/spaces_table.sql")
    post_response = web_client.post("spaces/new", data={
        'name': 'Test',
        'booking_date': '2024-04-10',
        'location': 'Canterbury',
        'price': '48.0',
        'description': 'A cosy test under the tests. Comes with complementary tests.',
        'user_id': '1'
    })
    assert post_response.status_code == 200
    assert post_response.data.decode('utf-8') == ""

    get_response = web_client.get("/spaces")
    assert get_response.status_code == 200
    assert get_response.data.decode('utf-8') == "" \
        "Space('Wizarding Cupboard', '2024-05-12', 'London', 50.00, 'A cosy room under the stairs. Comes with complementary spiders.', 1)\n" \
        "Space('Amore Penthouse', '2024-07-12', 'Paris', 87.00, 'Within view of the Eiffel Tower, this penthouse is your parisian dream.', 2)\n" \
        "Space('Paella Place', '2024-07-14', 'Madrid', 31.59, 'Eat paella and sleep.', 3)\n" \
        "Space('Mi Casa', '2024-07-12', 'Madrid', 45.50, 'Es tu Casa.', 3)\n"



def test_signup_page_loads_correctly(web_client, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    response = web_client.get('/signup')
    assert response.status_code == 200
    assert b'Sign Up' in response.data

def test_signup_page_renders_correctly(web_client, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    response = web_client.get('/signup')
    assert response.status_code == 200
    assert b'Sign Up' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

def test_signup_page_has_correct_form_elements(web_client, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    response = web_client.get('/signup')
    assert b'Sign Up' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

def test_signup_page_with_username_and_password(web_client, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    response = web_client.get('/signup?name=Inigo Montoya,password=prepare2die')
    assert response.status_code == 200
    assert b'Sign Up' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

