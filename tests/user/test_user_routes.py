from app.utils.constants import Status

user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Aa123456",
    "c_password": "Aa123456",
    "image_url": "https://example.com/image.jpg"
}


def test_create_user(client):
    response = client.post('/users/create', json=user_data)
    assert response.status_code == Status.CREATED.value


def test_get_all_users(client):
    response = client.get('/users')
    assert response.status_code == Status.OK.value


def test_get_user_by_id(client):
    user_id = 1
    response = client.get(f'/users/{user_id}')
    assert response.status_code == Status.OK.value


def test_update_user(client):
    user_id = 1  # Assuming there's an existing user with ID 1

    # Send a PUT request to update the user
    response = client.put(f'/users/{user_id}', json=user_data)

    # Check the response status code
    assert response.status_code == Status.UPDATED.value

    # send a GET request to check if the user was updated
    updated_user_response = client.get(f'/users/{user_id}')
    assert updated_user_response.status_code == Status.OK.value

    # Check if the user data has been updated in the response content
    # updated_user_data = json.loads(updated_user_response.get_data(as_text=True))
    #
    # assert updated_user_data['Name'] == 'John Doe'
    # assert updated_user_data['Email'] == 'john@example.com'


def test_delete_user(client):
    user_id = 1
    # Send a DELETE request to delete the user
    response = client.delete(f'/users/{user_id}')
    # Check the response status code
    assert response.status_code == Status.DELETED.value

    # Send a GET request to check if the user was deleted
    deleted_user_response = client.get(f'/users/{user_id}')
    assert deleted_user_response.status_code == Status.NOT_FOUND.value
