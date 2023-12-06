from datetime import datetime
from app.models.user import User
from app.utils.constants import api_routes_urls, CREATED, OK, UPDATED, NOT_FOUND
from tests import BaseTestCase


class UserRoutesTestCase(BaseTestCase):

    def create_and_insert_fake_user(self):
        registered_date = datetime.now()
        last_login = datetime.now()
        # Create a fake user
        fake_user = User(
            name='Jane Doe',
            email='jane.doe@example.com',
            password='Aa123456',
            image_url='https://example.com/image.jpg',
            registered_date=registered_date,
            last_login=last_login
        )
        # add it to the fake database
        self.db.session.add(fake_user)
        self.db.session.commit()
        return fake_user

    def test_create_user(self):
        # Create a fake user payload
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "Aa123456",
            "c_password": "Aa123456",
            "image_url": "https://example.com/image.jpg"
        }

        # Make a POST request to create a user
        response = self.client.post(api_routes_urls['user']['create_user'], json=user_data)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, CREATED)  # 201

        # Check if the user is added to the fake database
        created_user = User.query.filter_by(Email='john@example.com').first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.Name, 'John Doe')

    def test_get_single_user(self):
        fake_user = self.create_and_insert_fake_user()
        # GET request to retrieve the fake user
        response = self.client.get(f'{api_routes_urls['user']['get_users_list']}/{fake_user.UserID}')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, OK)  # 200 status code

        # Check if the user data in the response matches the fake user
        response_data = response.get_json()
        self.assertEqual(response_data['name'], 'Jane Doe')
        self.assertEqual(response_data['email'], 'jane.doe@example.com')

    def test_update_user(self):
        fake_user = self.create_and_insert_fake_user()

        update_data = {
            "name": "Updated User",
            "email": "john@example.com",
            "password": "NewPass123",
            "c_password": "NewPass123",
            "image_url": "https://example.com/image.png"
        }
        # PUT request to update the user
        response = self.client.put(
            f'{api_routes_urls["user"]["get_users_list"]}/{fake_user.UserID}',
            json=update_data
        )

        # Assert that the response is as expected
        self.assertEqual(response.status_code, UPDATED)

        # Check if there is content in the response before trying to parse JSON
        if response.get_data(as_text=True):
            # Print the response content
            print(response.get_data(as_text=True))

            # Check if the user in the fake database is updated
            updated_user = User.query.get(fake_user.UserID)
            self.assertIsNotNone(updated_user)
            self.assertEqual(updated_user.Name, 'Updated User')
            self.assertEqual(updated_user.Email, 'john@example.com')
            self.assertEqual(updated_user.Password, 'NewPass123')
            self.assertEqual(updated_user.ImageUrl, 'https://example.com/image.png')
        else:
            print(f"Response contains only status code {response.status_code} and No JSON Content.")

    def test_delete_user(self):
        fake_user = self.create_and_insert_fake_user()

        # Send a DELETE request to delete the user
        response = self.client.delete(f'{api_routes_urls['user']['get_users_list']}/{fake_user.UserID}')
        # Check the response status code
        assert response.status_code == 204

        deleted_user_response = self.client.get(f'{api_routes_urls['user']['get_users_list']}/{fake_user.UserID}')
        assert deleted_user_response.status_code == NOT_FOUND
