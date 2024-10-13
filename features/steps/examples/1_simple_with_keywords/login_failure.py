from behave import when, then

from kdb.webdriver import kdb_driver


@when("Login with <{email}> and <{password}>")
def step_impl(context, email, password):
    # Enter the email
    kdb_driver.update_text('id=email', email)
    # Enter the password
    kdb_driver.update_text('id=password', password)
    # Click [Log in] button
    kdb_driver.click('id=submit-button')


@then("The error message is displayed: <{error_message}>")
def step_impl(context, error_message):
    kdb_driver.verify_text_on_page(error_message)
    kdb_driver.screen_shot()
