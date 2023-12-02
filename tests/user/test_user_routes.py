import os
import tempfile
import pytest
from app import create_app

user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Aa123456",
    "c_password": "Aa123456",
    "image_url": "https://example.com/image.jpg"
}


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_get_all_users(client):
    response = client.get('/users')
    assert response.status_code == 200


def test_create_user(client):
    response = client.post('/users/create', json=user_data)
    assert response.status_code == 200


# def test_get_user_by_id(client):
#     # Retrieve the user from the database
#     retrieved_user = db.session.query(User).filter_by(Name=user_data['name']).first()
#     assert retrieved_user is not None

# TODO: more test functions for other endpoints (e.g., update and delete)
