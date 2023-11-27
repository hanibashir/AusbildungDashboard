from ..helpers.constants import Status


def message(model, status, field=None):
    if model == 'user':
        if field:
            return messages_list['user'][status][field]
        else:
            return messages_list['user'][status]


# messages dict
messages_list = {
    'user': {
        # new user created
        Status.CREATED: 'User created successfully',
        # user successfully logged in
        Status.OK: {
            'updated': 'User updated successfully',
            'deleted': 'User deleted successfully'
        },
        'EMPTY_FIELD': {
            'name': 'Please enter your name',
            'email': 'Please enter your email',
            'password': 'Please enter your password',
            'c_password': 'Please enter your confirm password',
        },
        'NAME_NOT_VALID': 'Names must consist of only letters',
        # check password match
        'PASS_CONFIRM': 'Two passwords don\'t match',
        'PASS_FORMAT': 'Passwords must be between 8 and 16 characters and must contain at least one uppercase letter, '
                       'one lowercase letter, and one digit',
        'EMAIL_NOT_VALID': 'Email not valid',
        Status.CONFLICT: 'This email already exists. Please change it or login',
        Status.NOT_FOUND: 'User not found',
        # something wrong with the input fields
        Status.BAD_REQUEST: 'Something went wrong!'
    },
    'aus_page': {

    }
}
