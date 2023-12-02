from flask import request
from flask_restful import Resource, Api
from . import category_blueprint
from ...utils.constants import Status
from ...utils.db.category_queries import CategoryQueries
from ...utils.to_json import rows_to_json, message_to_json
from ...utils.validation.category_validator import CategoryValidator

api = Api(category_blueprint)


# get all categories
class CategoryListResource(Resource):
    def __init__(self):
        self.category_query = CategoryQueries()

    def get(self):
        # get all categories and convert response to json
        return rows_to_json(self.category_query.select_all())


class CategoryResource(Resource):
    def __init__(self):
        self.data = request.get_json()
        self.validator = CategoryValidator(data=self.data)
        self.category_query = CategoryQueries(data=self.data)

    def post(self):
        # Receive and validate category input data
        validated, validate_msg = self.validator.validate_category_input()

        if not validated:
            return message_to_json(validate_msg, Status.BAD_REQUEST.value)  # Return a 400 Bad Request status code

        # Check if the email already exists in the database
        cat_exists, check_cat_msg = self.category_query.check_category_exists()
        if cat_exists:
            return message_to_json(msg=check_cat_msg,
                                   status=Status.CONFLICT.value)  # Return a 409 Conflict status code

        # insert new user
        insert_msg = self.category_query.insert_category()
        return message_to_json(msg=insert_msg, status=Status.CREATED.value)  # Return a 201 Created status code


# User routes
# api.add_resource(CategoryResource, '/categories/<int:cat_id>', endpoint='/categories/<int:user_id>')
api.add_resource(CategoryResource, '/categories/create', endpoint='/categories/create')
api.add_resource(CategoryListResource, '/categories', endpoint='/categories')
