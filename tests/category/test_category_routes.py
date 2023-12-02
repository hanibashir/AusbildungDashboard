category_data = {
    "title": "Computer Science",
    "description": "All cs related aus pages",
    "image_url": "https://example.com/image.jpg"
}


def test_get_all_categories(client):
    response = client.get('/categories')
    assert response.status_code == 200


def test_create_category(client):
    response = client.post('/categories/create', json=category_data)
    assert response.status_code == 200
