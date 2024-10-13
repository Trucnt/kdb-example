import json

from behave import when, then

from scripts.examples.api_object.example_get_api import ExampleGetAPI
from scripts.examples.api_object.example_post_api import ExamplePostAPI

api: ExampleGetAPI


@when("5_api - Execute the GET request with id={data_id}")
def step_impl(context, data_id):
    global api
    profile = context.profile
    api = ExampleGetAPI(profile)
    api.execute(data_id=data_id)


@then("5_api - Verify json schema of response")
def step_impl(context):
    global api
    response_schema = json.loads(str(context.text))
    api.verify_response_schema(response_schema)


@then("5_api - Verify response's body")
def step_impl(context):
    global api
    for row_data in context.table:
        api.verify_response_with_row(row_data)


@when("5_api - Execute the GET request and verify response with data table")
def step_impl(context):
    global api
    for row_data in context.table:
        api.add_comment_on_report(f'Execute request with id={row_data.get("id")}') \
            .execute(data_id=row_data.get('id')) \
            .verify_response('id', row_data.get('id')) \
            .verify_response('userId', row_data.get('userId')) \
            .verify_response('title', row_data.get('title')) \
            .verify_response('body', row_data.get('body'))


@when("5_api - Execute the POST request and verify response")
def step_impl(context):
    profile = context.profile
    api_post = ExamplePostAPI(profile)

    for row_data in context.table:
        data = {
            'title': row_data.get('title'),
            'body': row_data.get('body'),
            'userId': row_data.get('userId')
        }

        api_post.add_comment_on_report(f'Execute POST request with userId={row_data.get("userId")}') \
            .execute(data) \
            .verify_response('userId', row_data.get('userId')) \
            .verify_response('title', row_data.get('title')) \
            .verify_response('body', row_data.get('body'))
