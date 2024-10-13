import os
import pkgutil

from behave import given, step, then
from kdb.webdriver import kdb_driver

__all__ = []
PATH = [os.path.dirname(__file__)]
for loader, module_name, is_pkg in pkgutil.walk_packages(PATH):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module


@given("Open <{browser_name}> browser")
def step_impl(context, browser_name):
    """
    browser_name can be:
        - "ch" or "chrome" for chrome browser
        - "ed" or "edge" for ms edge browser
        - "ff" or "firefox" for firefox browser
        - "ie" or "internetexplorer" for internet explorer browser
        - "android" for chrome browser on android device
        - "ios" for safari browser on ios device
    """
    kdb_driver.start_browser(browser_name)


@then("Close browser")
def step_impl(context):
    kdb_driver.close_browser()


@step("Goto <{url}>")
def step_impl(context, url):
    kdb_driver.open_url(url)
