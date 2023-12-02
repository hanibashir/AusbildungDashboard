from flask import request
from flask_restful import Resource, Api
from . import aus_page_blueprint
from ...utils.constants import Status
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
        return rows_to_json(self.user_query.select_all())


class AusPageResource(Resource):
    def __init__(self):
        self.data = request.get_json()
        self.validator = AusPageValidator(data=self.data)
        self.aus_page_query = AusPageQueries(data=self.data)

    """
        {
            "title": "متخصص في تكنولوجيا المعلومات",
            "duration": "ثلاث سنوات ونصف",
            "certificate": "الثانوية",
            "content":"إنها سلسلة من الكلمات اللاتينية التي ، عند وضعها في موضعها ، لا تشكل جملًا بمعنى كامل ، ولكنها تعطي الحياة لنص اختبار مفيد لملء الفراغات التي يتم شغلها لاحقًا من نصوص مخصصة كتبها متخصصون في الاتصال.",
            "category_id": 1,
            "user_id": 1,
            "shift_type": "دوام متغير",
            "first_year_salary": 800,
            "second_year_salary": 900,
            "third_year_salary": 1000,
            "fourth_year_salary": 0,
            "best_paid": false,
            "popular": true,
            "image_url": "upload/images/users/user.png",
            "links": "ausbildung.de, fachinformatiker.de",
            "published": false
        }
    """

    def post(self):
        # Receive and validate aus page data
        validated, validate_msg = self.validator.validate_aus_page_input()

        if not validated:
            return message_to_json(validate_msg, Status.BAD_REQUEST.value)  # Return a 400 Bad Request status code

        # insert new ausbildung page
        insert_msg = self.aus_page_query.insert_aus_page()
        return message_to_json(msg=insert_msg, status=Status.CREATED.value)  # Return a 201 Created status code

    def get(self, page_id):
        aus_page: AusPage = self.aus_page_query.select_aus_page(page_id)
        if not aus_page:
            get_msg = message(model='aus_page', status=Status.NOT_FOUND)
            return message_to_json(msg=get_msg, status=Status.NOT_FOUND.value)  # Return a 404 Not Found status code
        return row_to_json(row=aus_page)

    def put(self, page_id):
        aus_page = self.aus_page_query.select_aus_page(page_id)
        if not aus_page:
            msg = message(model='aus_page', status=Status.NOT_FOUND)
            return message_to_json(msg=msg, status=Status.NOT_FOUND.value)  # Return a 404 Not Found status code

        # Receive and validate aus page data
        validated, msg = self.validator.validate_aus_page_input()
        if not validated:
            return message_to_json(msg, Status.BAD_REQUEST.value)  # Return a 400 Bad Request status code

        update_msg = self.aus_page_query.update_aus_page(aus_page)

        return message_to_json(msg=update_msg, status=Status.UPDATED.value)  # Return a 204 Updated status code

    def delete(self, page_id):
        # Retrieve aus page by ID
        aus_page: AusPage = self.aus_page_query.select_aus_page(page_id)

        if not aus_page:
            not_found_msg = message(model='aus_page', status=Status.NOT_FOUND)
            return message_to_json(
                msg=not_found_msg,
                status=Status.NOT_FOUND.value
            )  # Return a 404 Not Found status code

        deleted, delete_msg = self.aus_page_query.delete_aus_page(aus_page.AusPageID)
        if deleted:
            return message_to_json(msg=delete_msg, status=Status.DELETED.value)  # Return a 204 Deleted status code
        else:
            return message_to_json(msg=delete_msg, status=Status.BAD_REQUEST.value)


# Aus_page routes
api.add_resource(AusPageResource, '/aus_pages/<int:page_id>', endpoint='/aus_pages/<int:page_id>')
api.add_resource(AusPageResource, '/aus_pages/create', endpoint='/aus_pages/create')
api.add_resource(AusPageListResource, '/aus_pages', endpoint='/aus_pages')
