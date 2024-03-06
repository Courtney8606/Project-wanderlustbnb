from playwright.sync_api import Page, expect

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


# def test_get_album_1(page, test_web_address, db_connection, album_id=1):
#     db_connection.seed('seeds/music_library.sql')
#     page.goto(f'http://{test_web_address}/albums/{album_id}')
#     header = page.locator('h1')
#     album_info = page.locator('p')
#     expect(header).to_have_text('Doolittle')
#     expect(album_info).to_have_text('Release year: 1989\nArtist: Pixies')
    
def test_post_a_listing(db_connection, web_client):
    db_connection.seed("seeds/spaces_table.sql")
    post_response = web_client.post("/albums", data={
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

