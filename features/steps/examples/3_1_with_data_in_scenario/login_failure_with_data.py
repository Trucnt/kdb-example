from behave import then
from kdb.common.profiles import Profiles

from kdb.webdriver import kdb_driver

from scripts.examples.page_object.login_page import LoginPage


@then("Login with invalid email/password then verifying the error message is displayed")
def step_impl(context):
    # todo: step 1 - get profile from context
    profile: Profiles = context.profile

    # todo: step 2 - initialize the page object with profile above
    login_page = LoginPage(profile)
    login_page.load_page()

    # todo: step 3 - loop the table data in context
    for row in context.table:
        # todo: step 4 - using the methods of page object to interact with web element
        login_page \
            .enter_email(row['email']) \
            .enter_password(row['password']) \
            .click_login()

        # Verify the error message is displayed
        kdb_driver.verify_text_on_page(row['error_message'])
        # Take a screenshot of current page
        kdb_driver.screen_shot()
