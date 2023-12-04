from flask import request, make_response
from flask_restful import Resource, Api
from . import aus_page_blueprint
from ...utils.constants import Status, api_routes_urls
from ...utils.db.aus_page_queries import AusPageQueries
from ...utils.messages import message
from ...utils.to_json import row_to_json, message_to_json, rows_to_json
from ...utils.validation.aus_page_validator import AusPageValidator
from ...models.aus_page import AusPage

api = Api(aus_page_blueprint)


class AusPageListResource(Resource):
    def __init__(self):
        self.user_query = AusPageQueries()

    def get(self):
        # get all aus pages and convert response to json
        return make_response(
            rows_to_json(self.user_query.select_all()),
            Status.OK.value
        )


class AusPageResource(Resource):
    def __init__(self):
        self.data = request.get_json()
        self.validator = AusPageValidator(data=self.data)
        self.aus_page_query = AusPageQueries(data=self.data)

    def post(self):
        # Receive and validate aus page data
        validated, validate_msg = self.validator.validate_aus_page_input()

        if not validated:
            return make_response(
                message_to_json(validate_msg, Status.BAD_REQUEST.value),
                Status.BAD_REQUEST.value
            )  # Return a 400 Bad Request status code

        # insert new ausbildung page
        insert_msg = self.aus_page_query.insert_aus_page()
        return make_response(
            message_to_json(msg=insert_msg, status=Status.CREATED.value),
            Status.CREATED.value
        )  # Return a 201 Created status code

    def get(self, page_id):
        aus_page: AusPage = self.aus_page_query.select_aus_page(page_id)
        if not aus_page:
            get_msg = message(model='aus_page', status=Status.NOT_FOUND)
            return make_response(
                message_to_json(msg=get_msg, status=Status.NOT_FOUND.value),
                Status.NOT_FOUND.value
            )  # Return a 404 Not Found status code
        return make_response(
            row_to_json(row=aus_page),
            Status.OK.value
        )

    def put(self, page_id):
        aus_page = self.aus_page_query.select_aus_page(page_id)
        if not aus_page:
            msg = message(model='aus_page', status=Status.NOT_FOUND)
            return make_response(
                message_to_json(msg=msg, status=Status.NOT_FOUND.value),
                Status.NOT_FOUND.value
            )  # Return a 404 Not Found status code

        # Receive and validate aus page data
        validated, msg = self.validator.validate_aus_page_input()
        if not validated:
            return make_response(
                message_to_json(msg, Status.BAD_REQUEST.value),
                Status.BAD_REQUEST.value
            )  # Return a 400 Bad Request status code

        update_msg = self.aus_page_query.update_aus_page(aus_page)

        return make_response(
            message_to_json(msg=update_msg, status=Status.UPDATED.value),
            Status.UPDATED.value
        )  # Return a 204 Updated status code

    def delete(self, page_id):
        # Retrieve aus page by ID
        aus_page: AusPage = self.aus_page_query.select_aus_page(page_id)

        if not aus_page:
            not_found_msg = message(model='aus_page', status=Status.NOT_FOUND)
            return make_response(
                message_to_json(msg=not_found_msg, status=Status.NOT_FOUND.value),
                Status.NOT_FOUND.value
            )  # Return a 404 Not Found status code

        deleted, delete_msg = self.aus_page_query.delete_aus_page(aus_page.AusPageID)
        if deleted:
            return make_response(
                message_to_json(msg=delete_msg, status=Status.DELETED.value),
                Status.DELETED.value
            )  # Return a 204 Deleted status code
        else:
            return make_response(
                message_to_json(msg=delete_msg, status=Status.BAD_REQUEST.value),
                Status.BAD_REQUEST.value
            )  # Return a 400 Bad Request status code# Return a 400 Bad Request status code


# Aus_page routes
api.add_resource(
    AusPageResource,
    api_routes_urls['aus_page']['create_aus_page'],
    endpoint=api_routes_urls['aus_page']['create_aus_page']
)
api.add_resource(
    AusPageResource,
    api_routes_urls['aus_page']['get_single_aus_page'],
    endpoint=api_routes_urls['aus_page']['get_single_aus_page']
)

api.add_resource(
    AusPageListResource,
    api_routes_urls['aus_page']['get_aus_pages_list'],
    endpoint=api_routes_urls['aus_page']['get_aus_pages_list']
)
