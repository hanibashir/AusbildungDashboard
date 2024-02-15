from ..image_service import ImageService
from ...data.dashboard_queries.category.category_queries import CategoryQueries
from ...data.models.category import Category
from ...services.validation.category.category_validator import CategoryValidator
from flask import request, current_app
from ...utils.constants import CONFLICT
from ...utils.messages import message


class CategoryService:
    def __init__(self, data=None):
        self.data = data
        self.category = Category

    def get_categories(self):
        pass

    def get_category_by_id(self):
        return CategoryQueries().select_category(category_id=self.data['category_id'])

    def get_category_by_title(self):
        return CategoryQueries().select_category(title=self.data['title'])

    def insert_category(self):
        queries = CategoryQueries(data=self.data)
        image_service = ImageService()

        # validate user input
        valid, msg = self.validate_category()
        if not valid:
            return False, msg

        image = request.files["img"]
        if not image:
            image_short_url = current_app.config["DEFAULT_CATEGORY_IMAGE"]
        else:
            # get image path
            image_short_url = (
                image_service.upload_image(folder_path=current_app.config["CATEGORY_UPLOAD_FOLDER"], image=image))

        # insert into category table
        insert_msg = queries.insert_category(image_url=image_short_url)
        return True, insert_msg

    def update_category(self, category_id):
        pass

    def delete_category(self, category_id):
        pass

    def category_exists(self):
        return CategoryQueries().select_category(title=self.data['title'])

    def validate_category(self):
        # Query database to check if category already exists
        if self.category_exists():
            return False, message('category', CONFLICT)
        validated, validate_msg = CategoryValidator(data=self.data).validate_category_input()
        return validated, validate_msg
