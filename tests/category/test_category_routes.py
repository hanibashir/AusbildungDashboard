from app.utils.constants import Status

category_data = {
    "title": "Computer Science",
    "description": "All cs related aus pages",
    "image_url": "https://example.com/image.jpg"
}


def test_create_category(client):
    response = client.post('/categories/create', json=category_data)
    assert response.status_code == Status.CREATED.value


def test_get_all_categories(client):
    response = client.get('/categories')
    assert response.status_code == Status.OK.value


def test_get_category_by_id(client):
    category_id = 1
    response = client.get(f'/categories/{category_id}')
    assert response.status_code == Status.OK.value
