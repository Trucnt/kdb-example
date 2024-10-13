from kdb.common.profiles import Profiles
from kdb.scripts import BaseComponent


# todo: Step 1 - create the class extend BaseComponent
class CookiesConfirmComponent(BaseComponent):
    # todo: Step 3 - create the element locator
    ACCEPT_ALL_COOKIES_BUTTON = 'id=onetrust-accept-btn-handler'
    NECESSARY_COOKIES_ONLY_BUTTON = 'id=onetrust-reject-all-handler'
    CUSTOMIZE_SETTINGS_BUTTON = 'id=onetrust-pc-btn-handler'

    # the more locators...

    # todo: Step 2 - create the constructor
    def __init__(self, profile: Profiles):
        super().__init__(profile)

    # todo: Step 4 - create the functions to interact with web element using kdb_driver

    def click_accept_all_cookies(self):
        self.kdb_driver.click(self.ACCEPT_ALL_COOKIES_BUTTON)
        return self

    def click_necessary_cookies_only(self):
        self.kdb_driver.click(self.NECESSARY_COOKIES_ONLY_BUTTON)
        return self

    def click_customize_settings(self):
        self.kdb_driver.click(self.CUSTOMIZE_SETTINGS_BUTTON)
        return self
