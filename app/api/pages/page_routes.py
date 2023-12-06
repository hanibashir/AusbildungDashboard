from flask import make_response, request
from flask_restful import Resource, Api
from app.api.pages import page_blueprint
from app.models.page import Page
from app.utils.constants import OK, BAD_REQUEST, CREATED, NOT_FOUND, UPDATED, api_routes_urls
from app.utils.db.page_queries import PageQueries
from app.utils.messages import message
from app.utils.to_json import rows_to_json, message_to_json, row_to_json
from app.utils.validation.page_validator import PageValidator

api = Api(page_blueprint)


class PageListResource(Resource):
    def __init__(self):
        self.page_query = PageQueries()

    def get(self):
        # get all aus pages and convert response to json
        return make_response(
            rows_to_json(self.page_query.select_all()),
            OK
        )


class PageResource(Resource):
    def __init__(self):
        self.queries = None
        self.data = None
        self.validator = None

    def post(self):
        # Receive and validate aus page data
        if request.get_json():
            self.data = request.get_json()
            self.validator = PageValidator(data=self.data)
            self.queries = PageQueries(data=self.data)
        validated, validate_msg = self.validator.validate_page_input()

        if not validated:
            return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)  # 400 Bad Request

        # insert new ausbildung page
        insert_msg = self.queries.insert_page()
        return make_response(message_to_json(msg=insert_msg, status=CREATED), CREATED)  # 201 Created status code

    def get(self, page_id):
        if page_id:
            self.queries = PageQueries()
            page: Page = self.queries.select_page(page_id)
            if not page:
                get_msg = message(model='aus_page', status=NOT_FOUND)
                return make_response(message_to_json(msg=get_msg, status=NOT_FOUND), NOT_FOUND)  # 404
            return make_response(row_to_json(row=page), OK)

    def put(self, page_id):
        if page_id:
            if request.get_json():
                self.data = request.get_json()
                self.validator = PageValidator(data=self.data)
                self.queries = PageQueries(data=self.data)
            # get page by id
            page = self.queries.select_page(page_id)
            if not page:
                msg = message(model='aus_page', status=NOT_FOUND)
                return make_response(message_to_json(msg=msg, status=NOT_FOUND), NOT_FOUND)  # 404

            # Receive and validate aus page data
            validated, msg = self.validator.validate_page_input()
            if not validated:
                return make_response(message_to_json(msg, BAD_REQUEST), BAD_REQUEST)  # 400 Bad Request

            update_msg = self.queries.update_page(page)

            return make_response(message_to_json(msg=update_msg, status=UPDATED), UPDATED)

    def delete(self, page_id):
        if page_id:
            self.queries = PageQueries()
            # Retrieve page by ID
            page: Page = self.queries.select_page(page_id)

            if not page:
                not_found_msg = message(model='aus_page', status=NOT_FOUND)
                return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

            deleted, delete_msg = self.queries.delete_page(page.PageID)
            if deleted:
                return make_response(
                    message_to_json(msg=delete_msg, status='DELETED'), 204)
            else:
                return make_response(message_to_json(msg=delete_msg, status=BAD_REQUEST), BAD_REQUEST)


# Aus_page routes
api.add_resource(
    PageResource,
    api_routes_urls['page']['create_page'],
    endpoint=api_routes_urls['page']['create_page']
)
api.add_resource(
    PageResource,
    api_routes_urls['page']['get_single_page'],
    endpoint=api_routes_urls['page']['get_single_page']
)

api.add_resource(
    PageListResource,
    api_routes_urls['page']['get_pages_list'],
    endpoint=api_routes_urls['page']['get_pages_list']
)
