from datetime import datetime
from app.models.page import Page
from app.utils.constants import api_routes_urls, CREATED, OK, UPDATED, NOT_FOUND
from tests import BaseTestCase


class PageRoutesTestCase(BaseTestCase):

    def create_and_insert_fake_page(self):
        published_date = datetime.now()
        updated_date = datetime.now()
        # Create a fake page
        fake_page = Page(
            title="About App",
            content="Lorem ipsum dolor sit amet. Et voluptatibus debitis aut nisi voluptatem et doloribus velit et consectetur exercitationem ut omnis inventore ut consequatur illo At explicabo assumenda. Eos soluta quod ad modi blanditiis qui quia nihil sed repudiandae facilis in excepturi error ut Quis internos eos doloremque aperiam.",
            category_id=1,
            user_id=1,
            image_url="upload/images/users/user.png",
            links="ausbildung.de, fachinformatiker.de",
            published=False,
            published_date=published_date,
            updated_date=updated_date
        )
        # add it to the fake database
        self.db.session.add(fake_page)
        self.db.session.commit()
        return fake_page

    def test_create_page(self):
        # Create a fake page payload
        page_data = {
            "title": "About App",
            "content": "Lorem ipsum dolor sit amet. Et voluptatibus debitis aut nisi voluptatem et doloribus velit et consectetur exercitationem ut omnis inventore ut consequatur illo At explicabo assumenda. Eos soluta quod ad modi blanditiis qui quia nihil sed repudiandae facilis in excepturi error ut Quis internos eos doloremque aperiam.",
            "category_id": 1,
            "user_id": 1,
            "image_url": "upload/images/users/user.png",
            "links": "ausbildung.de, fachinformatiker.de",
            "published": False
        }

        # Make a POST request to create a page
        response = self.client.post(api_routes_urls['page']['create_page'], json=page_data)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, CREATED)  # 201

        # Check if the page is added to the fake database
        created_page = Page.query.filter_by(Title='About App').first()
        self.assertIsNotNone(created_page)
        self.assertEqual(created_page.Title, 'About App')

    def test_get_single_page(self):
        fake_page = self.create_and_insert_fake_page()
        # GET request to retrieve the fake page
        response = self.client.get(f'{api_routes_urls['page']['get_pages_list']}/{fake_page.PageID}')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, OK)  # 200 status code

        # Check if the page data in the response matches the fake page
        response_data = response.get_json()
        self.assertEqual(response_data['title'], 'About App')
        self.assertEqual(response_data['published'], False)
        self.assertEqual(response_data['category_id'], 1)

    def test_update_page(self):
        fake_page = self.create_and_insert_fake_page()

        update_data = {
            "title": "General Info",
            "content": "Lorem ipsum dolor sit amet. Et voluptatibus debitis aut nisi voluptatem et doloribus velit et consectetur exercitationem ut omnis inventore ut consequatur illo At explicabo assumenda. Eos soluta quod ad modi blanditiis qui quia nihil sed repudiandae facilis in excepturi error ut Quis internos eos doloremque aperiam.",
            "category_id": 2,
            "user_id": 1,
            "image_url": "upload/images/users/user.png",
            "links": "ausbildung.de, fachinformatiker.de",
            "published": True
        }
        # PUT request to update the page
        response = self.client.put(
            f'{api_routes_urls["page"]["get_pages_list"]}/{fake_page.PageID}',
            json=update_data
        )

        # Assert that the response is as expected
        self.assertEqual(response.status_code, UPDATED)

        # Check if there is content in the response before trying to parse JSON
        if response.get_data(as_text=True):
            # Print the response content
            print(response.get_data(as_text=True))

            # Check if the page in the fake database is updated
            updated_page = Page.query.get(fake_page.PageID)
            self.assertIsNotNone(updated_page)
            self.assertEqual(updated_page.Title, 'General Info')
            self.assertEqual(updated_page.CategorID, 2)
            self.assertEqual(updated_page.Published, True)
        else:
            print(f"Response contains only status code {response.status_code} and No JSON Content.")

    def test_delete_page(self):
        fake_page = self.create_and_insert_fake_page()

        # Send a DELETE request to delete the page
        response = self.client.delete(f'{api_routes_urls['page']['get_pages_list']}/{fake_page.PageID}')
        # Check the response status code
        assert response.status_code == 204

        deleted_page_response = self.client.get(
            f'{api_routes_urls['page']['get_pages_list']}/{fake_page.PageID}')
        assert deleted_page_response.status_code == NOT_FOUND
