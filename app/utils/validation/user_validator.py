from app.utils.messages import message
import re


class UserValidator:
    """
        validate user registration form input.
        [data] contains fields values in json format:
            name, password, confirm_password, email, image_url, registered_date, last_login
    """

    def __init__(self, data):
        self.__name = data['name']
        self.__email = data['email']
        self.__password = data['password']
        self.__confirm_password = data['c_password']

    def validate_user_register_input(self) -> tuple[bool, str]:
        # if the fields are empty
        if self.__name:
            if not self.validate_name():
                return False, message('user', 'NAME_NOT_VALID')
        else:
            return False, message('user', 'EMPTY_FIELD', 'name')
        # check email
        if self.__email:
            # validate email
            if not self.validate_user_email():
                return False, message('user', 'EMAIL_NOT_VALID')
        else:
            return False, message('user', 'EMPTY_FIELD', 'email')
        # check password
        if self.__password:
            # validate password
            if not self.validate_password():
                return False, message('user', 'PASS_FORMAT')
        else:
            return False, message('user', 'EMPTY_FIELD', 'password')
        # check password confirm not empty
        if not self.__confirm_password:
            return False, message('user', 'EMPTY_FIELD', 'c_password')

        # password confirmation
        if self.__password != self.__confirm_password:
            return False, message('user', 'PASS_CONFIRM')

        return True, ''

    def validate_name(self):
        # regular expression to validate the name
        pattern = r"^[A-Za-z\s']+$"
        return bool(re.match(pattern, self.__name))

    def validate_user_email(self):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        return bool(re.match(pattern, self.__email))

    def validate_password(self):
        password = self.__password
        # Check for minimum length, uppercase, lowercase, and digit
        if (
                (len(password) < 8) or (len(password) > 16) or
                (not re.search(r'[A-Z]', password)) or
                (not re.search(r'[a-z]', password)) or
                (not re.search(r'\d', password))):
            return False
        return True
