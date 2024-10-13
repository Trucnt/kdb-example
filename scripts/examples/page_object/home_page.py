from kdb.common.profiles import Profiles

from scripts.examples import BaseExamplePageObject


# todo: Step 1 - create the class extend BaseExamplePageObject
class HomePage(BaseExamplePageObject):
    # todo: Step 3 - create the element locator
    LOGIN_BUTTON = '//a[contains(@href, "/users/login") and contains(@class, "s-topbar")]'
    SIGNUP_BUTTON = '//a[contains(@href, "/users/signup") and contains(@class, "s-topbar")]'

    # the more locators...

    def __init__(self, profile: Profiles):
        # todo: Step 2 - create the constructor and given the path, title, page_loaded_text of this page
        super().__init__(profile,
                         path='/',
                         page_title='Stack Overflow - Where Developers Learn, Share, & Build Careers',
                         page_loaded_text='tab open to Stack Overflow.')

    # todo: Step 4 - create the functions to interact with web element using kdb_driver

    def click_login(self):
        self.kdb_driver.click(self.LOGIN_BUTTON)
        return self

    def click_signup(self):
        self.kdb_driver.click(self.SIGNUP_BUTTON)
        return self
