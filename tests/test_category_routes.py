import unittest
from app.models.category import Category
from app.utils.constants import api_routes_urls, CREATED, OK, UPDATED, NOT_FOUND
from tests import BaseTestCase


class CategoryRoutesTestCase(BaseTestCase):
    def create_and_insert_fake_category(self):
        # Create a fake category
        fake_category = Category(
            title='Test Category',
            description='A test category',
            image_url='https://example.com/image.jpg'
        )
        # Save it in the fake database
        self.db.session.add(fake_category)
        self.db.session.commit()
        return fake_category

    def test_create_category(self):
        # Create a fake category payload
        category_data = {
            "title": "Test Category",
            "description": "A test category",
            "image_url": "https://example.com/image.jpg"
        }

        # Make a POST request to create a category
        response = self.client.post(api_routes_urls['category']['create_category'], json=category_data)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, CREATED)

        # Check if the category is added to the fake database
        created_category = Category.query.filter_by(Title='Test Category').first()
        self.assertIsNotNone(created_category)
        self.assertEqual(created_category.Description, 'A test category')

    def test_get_single_category(self):
        fake_category = self.create_and_insert_fake_category()

        # GET request to retrieve the category
        response = self.client.get(f'{api_routes_urls['category']['get_categories_list']}/{fake_category.CategoryID}')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, OK)

        # Check if the category data in the response matches the fake category
        response_data = response.get_json()
        self.assertEqual(response_data['title'], 'Test Category')
        self.assertEqual(response_data['description'], 'A test category')

    def test_update_category(self):
        fake_category = self.create_and_insert_fake_category()

        update_data = {
            "title": "Test Category",
            "description": "A test category",
            "image_url": "https://example.com/image.jpg"
        }
        # PUT request to update the category
        response = self.client.put(
            f'{api_routes_urls["category"]["get_categories_list"]}/{fake_category.CategoryID}',
            json=update_data
        )

        # Assert that the response is as expected
        self.assertEqual(response.status_code, UPDATED)

        # Check if there is content in the response before trying to parse JSON
        if response.get_data(as_text=True):
            # Print the response content
            print(response.get_data(as_text=True))

            # Check if the user in the fake database is updated
            updated_category = Category.query.get(fake_category.UserID)
            self.assertIsNotNone(updated_category)
            self.assertEqual(updated_category.Title, 'Test Category')
            self.assertEqual(updated_category.Description, 'A test category')
            self.assertEqual(updated_category.ImageUrl, 'https://example.com/image.png')
        else:
            print(f"Response contains only status code {response.status_code} and No JSON Content.")

    def test_delete_category(self):
        fake_category = self.create_and_insert_fake_category()

        # Send a DELETE request to delete the category
        response = self.client.delete(
            f'{api_routes_urls["category"]["get_categories_list"]}/{fake_category.CategoryID}'
        )
        # Check the response status code
        assert response.status_code == 204

        deleted_category_response = self.client.get(
            f'{api_routes_urls['category']['get_categories_list']}/{fake_category.CategoryID}'
        )
        assert deleted_category_response.status_code == NOT_FOUND


if __name__ == '__main__':
    unittest.main()
