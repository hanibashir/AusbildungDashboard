from flask import request, make_response
from flask_restful import Resource, Api
from . import category_blueprint
from ...models.category import Category
from ...utils.constants import api_routes_urls, OK, BAD_REQUEST, CONFLICT, CREATED, NOT_FOUND, UPDATED
from ...utils.db.category_queries import CategoryQueries
from ...utils.messages import message
from ...utils.to_json import rows_to_json, message_to_json, row_to_json
from ...utils.validation.category_validator import CategoryValidator

api = Api(category_blueprint)


# get all categories
class CategoryListResource(Resource):
    def __init__(self):
        self.category_query = CategoryQueries()

    def get(self):
        # get all categories and convert response to json
        return make_response(rows_to_json(self.category_query.select_all()), OK)


class CategoryResource(Resource):
    def __init__(self):
        self.queries = None
        self.data = None
        self.validator = None

    def post(self):
        if request.get_json():
            self.data = request.get_json()
            self.validator = CategoryValidator(data=self.data)
            self.queries = CategoryQueries(data=self.data)
        # Receive and validate category input data
        validated, validate_msg = self.validator.validate_category_input()

        if not validated:
            return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)

        # Check if the email already exists in the database
        cat_exists, check_cat_msg = self.queries.check_category_exists()
        if cat_exists:
            return make_response(message_to_json(msg=check_cat_msg, status=CONFLICT), CONFLICT)

        # insert new category
        insert_msg = self.queries.insert_category()
        return make_response(message_to_json(msg=insert_msg, status=CREATED), CREATED)

    def get(self, category_id):
        if category_id:
            self.queries = CategoryQueries()
            # Retrieve a Category by ID
            category: Category = self.queries.select_category(category_id=category_id)

            if not category:
                not_found_msg = message(model='category', status=NOT_FOUND)

                return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

                # return Response(json_msg, status=Status.NOT_FOUND.value, mimetype='application/json')

            # return category data in a JSON response
            # name, password, confirm_password, email, image_url, registered_date, last_login
            return make_response(row_to_json(category), OK)  # 200 request ok

    def put(self, category_id):
        if request.get_json():
            self.data = request.get_json()
            self.validator = CategoryValidator(data=self.data)
            self.queries = CategoryQueries(data=self.data)

        # check category exists
        category = self.queries.select_category(category_id)

        if not category:
            not_found_msg = message(model='category', status=NOT_FOUND)
            return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

        # Receive and validate category input data
        validated, validate_msg = self.validator.validate_category_input()

        if not validated:
            return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)

        update_msg = self.queries.update_category(category)
        return make_response(message_to_json(update_msg, UPDATED), UPDATED)

    def delete(self, category_id):
        self.queries = CategoryQueries()
        # Retrieve a category by ID
        category = self.queries.select_category(category_id)

        if not category:
            not_found_msg = message(model='category', status=NOT_FOUND)
            return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

        deleted, delete_msg = self.queries.delete_category(category.CategoryID)
        if deleted:
            return make_response(
                message_to_json(msg=delete_msg, status='DELETED'), 204)
        else:
            return make_response(message_to_json(msg=delete_msg, status=BAD_REQUEST), BAD_REQUEST)


# Category routes
api.add_resource(
    CategoryResource,
    api_routes_urls['category']['create_category'],
    endpoint=api_routes_urls['category']['create_category']
)
api.add_resource(
    CategoryResource,
    api_routes_urls['category']['get_single_category'],
    endpoint=api_routes_urls['category']['get_single_category']
)

api.add_resource(
    CategoryListResource,
    api_routes_urls['category']['get_categories_list'],
    endpoint=api_routes_urls['category']['get_categories_list']
)
