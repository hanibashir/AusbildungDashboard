from app.utils.messages import message


class CategoryValidator:
    """
            validate ausbildung category form input.
            [data] contains fields values in json format:
                title, description, image_url
        """
    def __init__(self, data):
        self.__title = data['title']
        # self.__description = data['description']
        # self.__image_url = data['image_url']

    def validate_category_input(self) -> tuple[bool, str]:
        # if the fields are empty
        if not self.__title:
            return False, message('category', 'EMPTY_FIELD', 'title')
        else:
            return True, ''
