from flask import request
from flask_restful import Resource, Api
from . import category_blueprint

from ...utils.db.category_queries import CategoryQueries
from ...utils.to_json import rows_to_json

api = Api(category_blueprint)


# get all categories
class CategoryListResource(Resource):
    def __init__(self):
        self.category_query = CategoryQueries()

    def get(self):
        # get all categories and convert response to json
        return rows_to_json(self.category_query.select_all())


# User routes
# api.add_resource(CategoryResource, '/categories/<int:cat_id>', endpoint='/categories/<int:user_id>')
api.add_resource(CategoryResource, '/categories/create', endpoint='/categories/create')
api.add_resource(CategoryListResource, '/categories', endpoint='/categories')