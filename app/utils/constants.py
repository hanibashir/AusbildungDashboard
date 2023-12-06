OK = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404
CONFLICT = 409
UPDATED = 204
# DELETED = 204


api_routes_urls: dict = {
    "user": {
        "create_user": "/users/create",
        "get_single_user": "/users/<int:user_id>",
        "get_users_list": "/users"
    },
    "aus_page": {
        "create_aus_page": "/aus_pages/create",
        "get_single_aus_page": "/aus_pages/<int:page_id>",
        "get_aus_pages_list": "/aus_pages"
    },
    "category": {
        "create_category": "/categories/create",
        "get_single_category": "/categories/<int:category_id>",
        "get_categories_list": "/categories"
    },
}
