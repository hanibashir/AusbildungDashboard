import unittest
from app.models.category import Category
from app.utils.constants import api_routes_urls, CREATED, OK
from tests import BaseTestCase


class CategoryRoutesTestCase(BaseTestCase):
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
        # Create a fake category
        fake_category = Category(
            title='Test Category',
            description='A test category',
            image_url='https://example.com/image.jpg'
        )
        # Save it in the fake database
        self.db.session.add(fake_category)
        self.db.session.commit()

        # GET request to retrieve the category
        response = self.client.get(f'{api_routes_urls['category']['get_categories_list']}/{fake_category.CategoryID}')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, OK)

        # Check if the category data in the response matches the fake category
        response_data = response.get_json()
        self.assertEqual(response_data['title'], 'Test Category')
        self.assertEqual(response_data['description'], 'A test category')

    # TODO: other category routes tests


if __name__ == '__main__':
    unittest.main()
