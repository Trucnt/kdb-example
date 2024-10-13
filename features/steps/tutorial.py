from behave import *
from kdb import report
from kdb.webdriver import kdb_driver


@given('we have behave installed')
def step_impl(context):
    # write a text in html report
    report.add_comment("we have behave installed")
    # start browser
    # load page for test.


@when('we implement a test')
def step_impl(context):
    report.add_comment("we implement a test")
    # On button click, confirm box will appear


@then('behave will test it for us')
def step_impl(context):
    report.add_comment("behave will test it for us")
    # On button click, prompt box will appear


@step("the following users exist")
def step_impl(context):
    report.add_comment("the following users exist:")
    for row in context.table:
        report.add_comment(row['name'])


@step("I not implement it")
def step_impl(context):
    report.add_comment(u'STEP: But I not implement it')
