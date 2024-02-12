from app.utils.messages import message


class PageValidator:
    """
            validate page form input.
            [data] contains fields values in json format:
                 title, content, category_id, user_id, published_date, updated_date, published=False,
                 image_url=None, links=None

        """

    def __init__(self, data):
        self.__title = data['title']
        self.__content = data['content']
        self.__category_id = data['category_id']

    def validate_page_input(self) -> tuple[bool, str]:
        # if the fields are empty
        if not self.__title:
            return False, message('page', 'EMPTY_FIELD', 'title')
        elif not self.__content:
            return False, message('page', 'EMPTY_FIELD', 'content')
        elif not self.__category_id:
            return False, message('page', 'EMPTY_FIELD', 'category_id')
        else:
            return True, ''
