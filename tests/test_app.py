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

def test_get_all_spaces(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/spaces')
    div_tags = page.locator('div')
    expect(div_tags).to_have_text([
        'Name: Wizarding Cupboard\nLocation: London',
        'Name: Amore Penthouse\nLocation: Paris',
        'Name: Paella Place\nLocation: Madrid',
        'Name: Mi Casa\nLocation: Madrid'
    ])



