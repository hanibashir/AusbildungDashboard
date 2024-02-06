from flask import request, make_response
from flask_restful import Resource, Api
from . import aus_page_blueprint
from ...utils.constants import api_routes_urls, BAD_REQUEST, CREATED, NOT_FOUND, OK, UPDATED
from ...utils.db.aus_page_queries import AusPageQueries
from ...utils.messages import message
from ...utils.to_json import row_to_json, message_to_json, rows_to_json
from ...utils.validation.aus_page_validator import AusPageValidator
from ...models.aus_page import AusPage

api = Api(aus_page_blueprint)


class AusPageListResource(Resource):
    def __init__(self):
        self.aus_page_query = AusPageQueries()

    def get(self):
        # get all aus pages and convert response to json
        return make_response(
            rows_to_json(self.aus_page_query.select_all()),
            OK
        )


class AusPageResource(Resource):
    def __init__(self):
        self.queries = None
        self.data = None
        self.validator = None

    def post(self):
        # Receive and validate aus page data
        if request.get_json():
            self.data = request.get_json()
            self.validator = AusPageValidator(data=self.data)
            self.queries = AusPageQueries(data=self.data)
        validated, validate_msg = self.validator.validate_aus_page_input()

        if not validated:
            return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)  # 400 Bad Request

        # insert new ausbildung page
        insert_msg = self.queries.insert_aus_page()
        return make_response(message_to_json(msg=insert_msg, status=CREATED), CREATED)  # 201 Created status code

    def get(self, page_id):
        if page_id:
            self.queries = AusPageQueries()
            aus_page: AusPage = self.queries.select_aus_page(page_id)
            if not aus_page:
                get_msg = message(model='aus_page', status=NOT_FOUND)
                return make_response(message_to_json(msg=get_msg, status=NOT_FOUND), NOT_FOUND)  # 404
            return make_response(row_to_json(row=aus_page), OK)

    def put(self, page_id):
        if page_id:
            if request.get_json():
                self.data = request.get_json()
                self.validator = AusPageValidator(data=self.data)
                self.queries = AusPageQueries(data=self.data)
            aus_page = self.queries.select_aus_page(page_id)
            if not aus_page:
                msg = message(model='aus_page', status=NOT_FOUND)
                return make_response(message_to_json(msg=msg, status=NOT_FOUND), NOT_FOUND)  # 404

            # Receive and validate aus page data
            validated, msg = self.validator.validate_aus_page_input()
            if not validated:
                return make_response(message_to_json(msg, BAD_REQUEST), BAD_REQUEST)  # 400 Bad Request

            update_msg = self.queries.update_aus_page(aus_page)

            return make_response(message_to_json(msg=update_msg, status=UPDATED), UPDATED)

    def delete(self, page_id):
        if page_id:
            self.queries = AusPageQueries()
            # Retrieve a user by ID
            aus_page: AusPage = self.queries.select_aus_page(page_id)

            if not aus_page:
                not_found_msg = message(model='aus_page', status=NOT_FOUND)
                return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

            deleted, delete_msg = self.queries.delete_aus_page(aus_page.AusPageID)
            if deleted:
                return make_response(
                    message_to_json(msg=delete_msg, status='DELETED'), 204)
            else:
                return make_response(message_to_json(msg=delete_msg, status=BAD_REQUEST), BAD_REQUEST)


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
