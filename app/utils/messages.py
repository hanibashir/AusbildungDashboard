from app.utils.constants import CREATED, OK, UPDATED, CONFLICT, NOT_FOUND, BAD_REQUEST


def message(model, status, field=None):
    if model == 'user':
        if field:
            return messages_list['user'][status][field]
        else:
            return messages_list['user'][status]
    elif model == 'post':
        if field:
            return messages_list['post'][status][field]
        else:
            return messages_list['post'][status]
    elif model == 'category':
        if field:
            return messages_list['category'][status][field]
        else:
            return messages_list['category'][status]
    elif model == 'page':
        if field:
            return messages_list['page'][status][field]
        else:
            return messages_list['page'][status]


messages_list = {
    'user': {
        # new profile created
        CREATED: 'User created successfully',
        # profile successfully logged in
        OK: '',
        UPDATED: 'User updated successfully',
        'DELETED': 'User successfully deleted',
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
        CONFLICT: 'This email already exists. Please change it or login',
        NOT_FOUND: 'User not found',
        BAD_REQUEST: 'Something went wrong!'
    },
    'post': {
        'TITLE_NOT_VALID': '',
        'EMPTY_FIELD': {
            'title': 'Please enter the ausbildung post title',
            'duration': 'Please enter ausbildung duration',
            'certificate': 'Please enter ausbildung certificate',
            'content': 'Please enter ausbildung content',
            'category_id': 'Please choose ausbildung category'
        },
        CREATED: 'Ausbildung Page created successfully',
        NOT_FOUND: 'Post not found',
        OK: '',
        UPDATED: 'Post updated successfully',
        'DELETED': 'Post successfully deleted',
        BAD_REQUEST: 'Something went wrong!'
    },
    'category': {
        'EMPTY_FIELD': {
            'title': 'Please enter the category title'
        },
        CONFLICT: 'This category already exists',
        CREATED: 'Category created successfully',
        NOT_FOUND: 'Category not found',
        OK: '',
        UPDATED: 'Category updated successfully',
        'DELETED': 'Category deleted successfully',
        BAD_REQUEST: 'Something went wrong!'
    },
    'page': {
        'TITLE_NOT_VALID': '',
        'EMPTY_FIELD': {
            'title': 'Please enter the page title',
            'content': 'Please enter page content',
            'category_id': 'Please choose page category'
        },
        CREATED: 'Page created successfully',
        NOT_FOUND: 'Page not found',
        OK: '',
        UPDATED: 'Page updated successfully',
        'DELETED': 'Page deleted successfully',
        BAD_REQUEST: 'Something went wrong!'
    }
}
