user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Aa123456",
    "c_password": "Aa123456",
    "image_url": "https://example.com/image.jpg"
}


def test_get_all_users(client):
    response = client.get('/users')
    assert response.status_code == 200


def test_create_user(client):
    response = client.post('/users/create', json=user_data)
    assert response.status_code == 200


def test_get_user_by_id(client):
    user_id = 1
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200

# TODO: more test functions for other endpoints (e.g., update and delete)

