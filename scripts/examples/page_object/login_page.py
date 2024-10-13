from kdb.common.profiles import Profiles

from scripts.examples import BaseExamplePageObject


# todo: Step 1 - create the class extend BaseExamplePageObject
class LoginPage(BaseExamplePageObject):
    # todo: Step 3 - create the element locator
    EMAIL_INPUT = 'id=email'
    PASSWORD_INPUT = 'id=password'
    LOGIN_BUTTON = 'id=submit-button'

    # the more locators...

    def __init__(self, profile: Profiles):
        # todo: Step 2 - create the constructor and given the path, title, page_loaded_text of this page
        super().__init__(profile,
                         path='/users/login',
                         page_title='Log In - Stack Overflow',
                         page_loaded_text='Forgot password?')

    # todo: Step 4 - create the functions to interact with web element using kdb_driver

    def enter_email(self, email: str):
        self.kdb_driver.update_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str):
        self.kdb_driver.update_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.kdb_driver.click(self.LOGIN_BUTTON)
        return self

    def login(self, email: str, password: str):
        self.enter_email(email) \
            .enter_password(password) \
            .click_login()
        return self
