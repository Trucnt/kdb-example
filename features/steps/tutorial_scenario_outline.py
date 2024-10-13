from behave import *
from kdb import report


@given('there are {start} cucumbers')
def step_impl(context, start):
    print(start)
    report.add_comment(start)


@when("I eat {eat} cucumbers")
def step_impl(context, eat):
    report.add_comment(eat)


@then("I should have {left} cucumbers")
def step_impl(context, left):
    report.add_comment(left)
