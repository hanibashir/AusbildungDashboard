from flask import request
from flask_restful import Resource, Api
from . import user_blueprint
from ...models.user import User
from ...utils.db.user_queries import UserQueries
from ...utils.validation.user_validator import UserValidator
from ...utils.messages import message, Status
from ...utils.to_json import message_to_json, row_to_json, rows_to_json

api = Api(user_blueprint)


# get all users
class UserListResource(Resource):
    def __init__(self):
        self.user_query = UserQueries()

    def get(self):
        # get all users and convert response to json
        return rows_to_json(self.user_query.select_all())


class UserResource(Resource):
    def __init__(self):
        # received data from request as json
        self.data = request.get_json()
        self.validator = UserValidator(data=self.data)
        self.user_query = UserQueries(data=self.data)

    def post(self):
        # Receive and validate user registration data
        validated, validate_msg = self.validator.validate_user_register_input()

        if not validated:
            return message_to_json(validate_msg, Status.BAD_REQUEST.value)  # Return a 400 Bad Request status code

        # Check if the email already exists in the database
        email_exists, check_email_msg = self.user_query.check_email_exists()
        if email_exists:
            return message_to_json(msg=check_email_msg,
                                   status=Status.CONFLICT.value)  # Return a 409 Conflict status code

        # insert new user
        insert_msg = self.user_query.insert_user()
        return message_to_json(msg=insert_msg, status=Status.CREATED.value)  # Return a 201 Created status code

    def get(self, user_id):
        if user_id:
            # Retrieve a user by ID
            user: User = self.user_query.select_user(user_id=user_id)

            if not user:
                not_found_msg = message(model='user', status=Status.NOT_FOUND)
                return message_to_json(msg=not_found_msg,
                                       status=Status.NOT_FOUND.value)  # Return a 404 Not Found status code

            # return user data in a JSON response
            # name, password, confirm_password, email, image_url, registered_date, last_login
            return row_to_json(user)

    def put(self, user_id):
        # Retrieve a user by ID
        user = self.user_query.select_user(user_id)

        if not user:
            not_found_msg = message(model='user', status=Status.NOT_FOUND)
            return message_to_json(msg=not_found_msg,
                                   status=Status.NOT_FOUND.value)  # Return a 404 Not Found status code

        validated, validate_msg = self.validator.validate_user_register_input()

        if not validated:
            return message_to_json(validate_msg, Status.BAD_REQUEST.value)  # Return a 400 Bad Request status code

        # Check if the email already exists in the database
        email_exists, check_email_msg = self.user_query.check_email_exists()
        if email_exists:
            return message_to_json(msg=check_email_msg,
                                   status=Status.CONFLICT.value)  # Return a 409 Conflict status code

        update_msg = self.user_query.update_user(user)

        return message_to_json(msg=update_msg, status=Status.UPDATED.value)  # Return a 204 Updated status code

    def delete(self, user_id):
        # Retrieve a user by ID
        user = self.user_query.select_user(user_id)

        if not user:
            not_found_msg = message(model='user', status=Status.NOT_FOUND)
            return message_to_json(
                msg=not_found_msg,
                status=Status.NOT_FOUND.value
            )  # Return a 404 Not Found status code

        deleted, delete_msg = self.user_query.delete_user(user.UserID)
        if deleted:
            return message_to_json(msg=delete_msg, status=Status.DELETED.value)  # Return a 204 Deleted status code
        else:
            return message_to_json(msg=delete_msg, status=Status.BAD_REQUEST.value)


# User routes
api.add_resource(UserResource, '/users/<int:user_id>', endpoint='/users/<int:user_id>')
api.add_resource(UserResource, '/users/create', endpoint='/users/create')
api.add_resource(UserListResource, '/users', endpoint='/users')
