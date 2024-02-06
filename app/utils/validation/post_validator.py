from app.utils.messages import message


class PostValidator:
    """
            validate ausbildung page form input.
            [data] contains fields values in json format:
                title, duration, certificate, content, category_id, etc...
        """

    def __init__(self, data):
        self.__title = data['title']
        self.__duration = data['duration']
        self.__certificate = data['certificate']
        self.__content = data['content']
        self.__category_id = data['category_id']

    def validate_post_input(self) -> tuple[bool, str]:
        # if the fields are empty
        if not self.__title:
            return False, message('aus_page', 'EMPTY_FIELD', 'title')
        elif not self.__duration:
            return False, message('aus_page', 'EMPTY_FIELD', 'duration')
        elif not self.__certificate:
            return False, message('aus_page', 'EMPTY_FIELD', 'certificate')
        elif not self.__content:
            return False, message('aus_page', 'EMPTY_FIELD', 'content')
        elif not self.__category_id:
            return False, message('aus_page', 'EMPTY_FIELD', 'category_id')
        else:
            return True, ''
