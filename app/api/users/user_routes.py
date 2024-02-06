from flask import request, make_response
from flask_restful import Resource, Api
from . import user_blueprint
from ...models.user import User
from ...utils.constants import api_routes_urls, OK, BAD_REQUEST, CONFLICT, CREATED, NOT_FOUND, UPDATED
from ...utils.api_queries.user_queries import UserQueries
from ...utils.validation.user_validator import UserValidator
from ...utils.messages import message
from ...utils.to_json import message_to_json, row_to_json, rows_to_json

api = Api(user_blueprint)


# get all users
class UserListResource(Resource):
    def __init__(self):
        self.user_query = UserQueries()

    def get(self):
        # get all users and convert response to json
        return make_response(rows_to_json(self.user_query.select_all()), OK)


class UserResource(Resource):
    def __init__(self):
        self.queries = None
        self.data = None
        self.validator = None

    def post(self):
        # Receive and validate user registration data
        if request.get_json():
            self.data = request.get_json()
            self.validator = UserValidator(data=self.data)
            self.queries = UserQueries(data=self.data)

        validated, validate_msg = self.validator.validate_user_input()

        if not validated:
            return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)

        # Check if the email already exists in the database
        email_exists, check_email_msg = self.queries.check_email_exists()
        if email_exists:
            return make_response(message_to_json(msg=check_email_msg, status=CONFLICT), CONFLICT)

        # insert new user
        insert_msg = self.queries.insert_user()
        return make_response(message_to_json(msg=insert_msg, status=CREATED), CREATED)

    def get(self, user_id):
        if user_id:
            self.queries = UserQueries()
            # Retrieve a user by ID
            user: User = self.queries.select_user(user_id=user_id)

            if not user:
                not_found_msg = message(model='user', status=NOT_FOUND)
                return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

                # return Response(json_msg, status=Status.NOT_FOUND.value, mimetype='application/json')

            # return user data in a JSON response
            # name, password, confirm_password, email, image_url, registered_date, last_login
            return make_response(row_to_json(user), OK)

    def put(self, user_id):
        if user_id:
            if request.get_json():
                self.data = request.get_json()
                self.validator = UserValidator(data=self.data)
                self.queries = UserQueries(data=self.data)

            # check user exists
            user = self.queries.select_user(user_id)

            if not user:
                not_found_msg = message(model='user', status=NOT_FOUND)
                return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

            # Receive and validate user registration data
            validated, validate_msg = self.validator.validate_user_input()

            if not validated:
                return make_response(message_to_json(validate_msg, BAD_REQUEST), BAD_REQUEST)

            update_msg = self.queries.update_user(user)
            return make_response(message_to_json(update_msg, UPDATED), UPDATED)

    def delete(self, user_id):
        if user_id:
            self.queries = UserQueries()
            # Retrieve a user by ID
            user = self.queries.select_user(user_id)

            if not user:
                not_found_msg = message(model='user', status=NOT_FOUND)
                return make_response(message_to_json(msg=not_found_msg, status=NOT_FOUND), NOT_FOUND)

            deleted, delete_msg = self.queries.delete_user(user.UserID)
            if deleted:
                return make_response(
                    message_to_json(msg=delete_msg, status='DELETED'), 204)
            else:
                return make_response(message_to_json(msg=delete_msg, status=BAD_REQUEST), BAD_REQUEST)


# User routes
# api.add_resource(
#     UserResource,
#     api_routes_urls['user']['create_user'],
#     endpoint=api_routes_urls['user']['create_user']
# )
# api.add_resource(
#     UserResource,
#     api_routes_urls['user']['get_single_user'],
#     endpoint=api_routes_urls['user']['get_single_user']
# )
#
# api.add_resource(
#     UserListResource,
#     api_routes_urls['user']['get_users_list'],
#     endpoint=api_routes_urls['user']['get_users_list']
# )
