from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository, User
import os
from unittest.mock import MagicMock

    # print(page.url)
    # print(page.content())

# Signup and Login Testing

def user_logs_in(page, test_web_address):
    page.goto(f'http://{test_web_address}/')
    page.fill("input[name='username']", "montoya")
    page.fill("input[name='password']", "prepare2die")
    page.click("button[type='submit']")  

def test_successful_login(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)
    welcome_message = page.locator('h1.user-welcome')
    expect(welcome_message).to_have_text('Welcome, montoya.')


def test_failed_login(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/')
    page.fill("input[name='username']", "montoya")
    page.fill("input[name='password']", "prepare2live")
    page.click("button[type='submit']")
    error_message = page.locator('p.error-login')
    expect(error_message).to_have_text("Username or password do not match, please try again.\nDon't have an account? Sign up!")

def test_successful_signup(page, test_web_address, db_connection):
        db_connection.seed('seeds/spaces_table.sql')
        page.goto(f'http://{test_web_address}/signup')
        page.fill("input[name='username']", "lord_snow")
        page.fill("input[name='name']", "Jon Snow")
        page.fill("input[name='password']", "ghost")
        page.fill("input[name='repeat_password']", "ghost")
        page.click("button[type='submit']")
        welcome_message = page.locator('h1.user-welcome')
        expect(welcome_message).to_have_text('Welcome, lord_snow.')

def test_failed_signup_matching_passwords(page, test_web_address, db_connection):
        db_connection.seed('seeds/spaces_table.sql')
        page.goto(f'http://{test_web_address}/signup')
        page.fill("input[name='username']", "lord_snow")
        page.fill("input[name='name']", "Jon Snow")
        page.fill("input[name='password']", "ghost")
        page.fill("input[name='repeat_password']", "ghosty")
        page.click("button[type='submit']")
        error_message = page.locator('#signup-error')
        expect(error_message).to_have_text("Passwords do not match. Please try again.")

# Render the Index page with all() available properties for booking when a user is logged in

def test_get_all_spaces(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)
    page.goto(f'http://{test_web_address}/index')
    div_tags = page.locator('div.col-lg-4 h3')
    expect(div_tags).to_have_text([
        'Wizarding Cupboard',
        'Amore Penthouse',
        'Paella Place',
        'Mi Casa'
    ])

# Render the Index page with filters available properties based on search criteria

def test_get_all_spaces_filtered_search(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address) 
    page.fill("input[name='checkin']", "2024-07-12")
    page.click("button[type='Submit']")
    div_tags = page.locator('div.col-lg-4 h3')
    expect(div_tags).to_have_text(
        'Wizarding Cupboard'
    )

# When trying to access /index, return to Login page if user if not logged in

def test_redirect_login(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/index')
    h1_tag = page.locator('h1')
    expect(h1_tag).to_have_text('Login | MakersBnB')

# User can create a new listing when logged in 

def test_create_a_listing(db_connection, page, test_web_address):
    db_connection.seed("seeds/spaces_table.sql")
    user_logs_in(page, test_web_address)
    page.goto(f'http://{test_web_address}/new')
    page.fill("input[name='name']", "Test Property")
    page.fill("input[name='location']", "Test Location")
    page.fill("input[name='price']", "54.00")
    page.fill("input[name='description']", "Test Description")
    current_dir = os.path.dirname(__file__)
    relative_path = '../static/images/house1.jpg'
    file = os.path.abspath(os.path.join(current_dir, relative_path))
    print(file)
    page.set_input_files("input[name='file']", file)
    page.click("input[type='submit']")
    div_tags = page.locator('div.col-lg-4 h3')
    expect(div_tags).to_have_text([
        'Wizarding Cupboard',
        'Amore Penthouse',
        'Paella Place',
        'Mi Casa',
        'Test Property'
    ])

# User redirected to login from /new if not logged in - cannot create a new listing

def test_create_a_listing_no_session(db_connection, page, test_web_address):
    db_connection.seed("seeds/spaces_table.sql")
    page.goto(f'http://{test_web_address}/new')
    h1_tag = page.locator('h1')
    expect(h1_tag).to_have_text('Login | MakersBnB')

# Individual spaces render when user is logged in

def test_get_individual_space_1(page, test_web_address, db_connection, space_id=1):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)
    page.goto(f'http://{test_web_address}/spaces/{space_id}')
    header = page.locator('h1')
    space_info = page.locator('p')
    expect(space_info).to_have_text('Location: London \n Description: A cosy room under the stairs. Comes with complementary spiders. \n Price per night: £50.0')
    expect(header).to_have_text('Wizarding Cupboard')

# Individual spaces don't render when user is not logged in

def test_get_individual_space_fails_no_session(page, test_web_address, db_connection, space_id=1):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/spaces/{space_id}')
    h1_tag = page.locator('h1')
    expect(h1_tag).to_have_text('Login | MakersBnB')


# Test successfully create a property booking

def test_create_booking(page, test_web_address, db_connection, space_id=2):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)
    page.goto(f'http://{test_web_address}/spaces/{space_id}')
    page.wait_for_selector('#datepicker')
    page.click("#datepicker")
    page.wait_for_selector('.datepicker-days')
    page.evaluate(
    '''() => {
        const datePicker = $('#datepicker');
        const desiredDate = '2024-07-12';
        datePicker.datepicker('setDate', desiredDate);
    }'''
)
    page.click("button[type='submit']")
    header = page.locator("h1")
    expect(header).to_have_text("SUCCESS!")

# Test navigation to Host account with correct properties listed and correct bookings available for review

def test_navigate_host_account(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)
    page.click("#account-link")
    h3_tag = page.locator('h3')
    expect(h3_tag).to_have_text(['Host', 'Guest'])
    page.click("#host-link")
    h3_tag = page.locator('h3')
    expect(h3_tag).to_have_text(['Paella Place', 'Mi Casa'])
    page.click(f"a[href='/user/requests/Mi Casa/4']")
    unapproved_booking_container = page.query_selector('.booking-container#unapproved')
    unapproved_text = unapproved_booking_container.inner_text()
    assert "Property: Mi Casa" in unapproved_text


# Test guest booking can be approved by Host user

def test_approve_booking(page, test_web_address, db_connection, space_id=4, space_name='Mi Casa'):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)
    page.goto(f'http://{test_web_address}/user/requests/{space_name}/{space_id}')
    first_booking_form = page.query_selector('.booking-container#unapproved .booking')
    approve_button = first_booking_form.query_selector('.file_submit')
    approve_button.click()
    approved_booking_container = page.query_selector('.booking-container#approved')
    property_name_element = approved_booking_container.query_selector('h3')
    property_name = property_name_element.inner_text()
    space_name_text = property_name.replace('Property: ', '')
    assert space_name_text == space_name, f"Space name mismatch. Expected: {space_name}, Actual: {space_name_text}"

# Test guest booking can be rejected by Host user

def test_reject_booking(page, test_web_address, db_connection, space_id=4, space_name='Mi Casa'):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)  
    page.goto(f'http://{test_web_address}/user/requests/{space_name}/{space_id}')
    delete_button = page.locator('button.file_delete')
    delete_button.click()
    approved_booking_container = page.query_selector('.booking-container#approved')
    approved_text = approved_booking_container.inner_text()
    assert "Confirmed bookings" in approved_text
    assert len(approved_text.strip()) == len("Confirmed bookings")
    unapproved_booking_container = page.query_selector('.booking-container#unapproved')
    unapproved_text = unapproved_booking_container.inner_text()
    assert "Bookings for approval" in unapproved_text
    assert len(unapproved_text.strip()) == len("Bookings for approval")

# Test navigation to Guestaccount with correct bookings available for review

def test_navigate_guest_account(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/')
    page.fill("input[name='username']", "ratatouille")
    page.fill("input[name='password']", "kissthecook")
    page.click("button[type='submit']")  
    page.click("#account-link")
    h3_tag = page.locator('h3')
    expect(h3_tag).to_have_text(['Host', 'Guest'])
    page.click("#guest-link")
    unapproved_booking_container = page.query_selector('.booking-container#unapproved')
    unapproved_text = unapproved_booking_container.inner_text()
    assert "Property: Paella Place" in unapproved_text

# Test guest booking can be rejected by Host user

def test_logout(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    user_logs_in(page, test_web_address)
    logout_button = page.locator('#logout-link')
    logout_button.click()
    login_form = page.locator('#login-form')
    expect(login_form).to_be_visible()
    page.goto(f'http://{test_web_address}/')
    h1_tag = page.locator('h1')
    expect(h1_tag).to_have_text('Login | MakersBnB')

def test_new_guest_message_after_approval(page, test_web_address, db_connection):
    db_connection.seed('seeds/spaces_table.sql')
    page.goto(f'http://{test_web_address}/')
    page.fill("input[name='username']", "mrs_dursley")
    page.fill("input[name='password']", "hatemynephew123")
    page.click("button[type='submit']")  
    message = page.locator('#new-approval-link')
    expect(message).to_have_text('New Message 🔔')
