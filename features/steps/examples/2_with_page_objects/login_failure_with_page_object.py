from behave import when
from kdb.common.profiles import Profiles

from scripts.examples.page_object.login_page import LoginPage


@when("Login with <{email}> and <{password}> with page object")
def step_impl(context, email, password):
    # todo: step 1 - get profile from context
    profile: Profiles = context.profile

    # todo: step 2 - initialize the page object with profile above
    login_page = LoginPage(profile)
    login_page.load_page()

    # todo: step 3 - using the methods of page object to interact with web element
    login_page \
        .enter_email(email) \
        .enter_password(password) \
        .click_login()
