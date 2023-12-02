category_data = {
    "title": "Computer Science",
    "description": "All cs related aus pages",
    "image_url": "https://example.com/image.jpg"
}


def test_get_all_users(client):
    response = client.get('/categories')
    assert response.status_code == 200
