from datetime import datetime
from app.data.models import AusPage
from app.utils.constants import api_routes_urls, CREATED, OK, UPDATED, NOT_FOUND
from tests import BaseTestCase


class AusPageRoutesTestCase(BaseTestCase):

    def create_and_insert_fake_aus_page(self):
        published_date = datetime.now()
        updated_date = datetime.now()
        # Create a fake aus_page
        fake_aus_page = AusPage(
            title="Fachinformatiker",
            duration="Three years",
            certificate="High School",
            content="Lorem ipsum dolor sit amet. Et voluptatibus debitis aut nisi voluptatem et doloribus velit et consectetur exercitationem ut omnis inventore ut consequatur illo At explicabo assumenda. Eos soluta quod ad modi blanditiis qui quia nihil sed repudiandae facilis in excepturi error ut Quis internos eos doloremque aperiam.",
            category_id=1,
            user_id=1,
            shift_type="Changing Shift",
            first_year_salary=800,
            second_year_salary=900,
            third_year_salary=1000,
            fourth_year_salary=0,
            best_paid=False,
            popular=True,
            image_url="upload/images/users/user.png",
            links="ausbildung.de, fachinformatiker.de",
            published=False,
            published_date=published_date,
            updated_date=updated_date
        )
        # add it to the fake database
        self.db.session.add(fake_aus_page)
        self.db.session.commit()
        return fake_aus_page

    def test_create_aus_page(self):
        # Create a fake aus_page payload
        aus_page_data = {
            "title": "Fachinformatiker",
            "duration": "Three years",
            "certificate": "High School",
            "content": "Lorem ipsum dolor sit amet. Et voluptatibus debitis aut nisi voluptatem et doloribus velit et consectetur exercitationem ut omnis inventore ut consequatur illo At explicabo assumenda. Eos soluta quod ad modi blanditiis qui quia nihil sed repudiandae facilis in excepturi error ut Quis internos eos doloremque aperiam.",
            "category_id": 1,
            "user_id": 1,
            "shift_type": "Changing Shift",
            "first_year_salary": 800,
            "second_year_salary": 900,
            "third_year_salary": 1000,
            "fourth_year_salary": 0,
            "best_paid": False,
            "popular": True,
            "image_url": "upload/images/users/user.png",
            "links": "ausbildung.de, fachinformatiker.de",
            "published": False
        }

        # Make a POST request to create a aus_page
        response = self.client.post(api_routes_urls['aus_page']['create_aus_page'], json=aus_page_data)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, CREATED)  # 201

        # Check if the aus_page is added to the fake database
        created_aus_page = AusPage.query.filter_by(Title='Fachinformatiker').first()
        self.assertIsNotNone(created_aus_page)
        self.assertEqual(created_aus_page.Title, 'Fachinformatiker')

    def test_get_single_aus_page(self):
        fake_aus_page = self.create_and_insert_fake_aus_page()
        # GET request to retrieve the fake aus_page
        response = self.client.get(f'{api_routes_urls['aus_page']['get_aus_pages_list']}/{fake_aus_page.AusPageID}')

        # Assert that the response is as expected
        self.assertEqual(response.status_code, OK)  # 200 status code

        # Check if the aus_page data in the response matches the fake aus_page
        response_data = response.get_json()
        self.assertEqual(response_data['title'], 'Fachinformatiker')
        self.assertEqual(response_data['image_url'], 'upload/images/users/user.png')

    def test_update_aus_page(self):
        fake_aus_page = self.create_and_insert_fake_aus_page()

        update_data = {
            "title": "Fachinformatiker",
            "duration": "Three years and half",
            "certificate": "High School",
            "content": "Lorem ipsum dolor sit amet. Et voluptatibus debitis aut nisi voluptatem et doloribus velit et consectetur exercitationem ut omnis inventore ut consequatur illo At explicabo assumenda. Eos soluta quod ad modi blanditiis qui quia nihil sed repudiandae facilis in excepturi error ut Quis internos eos doloremque aperiam.",
            "category_id": 2,
            "user_id": 1,
            "shift_type": "Changing Shift",
            "first_year_salary": 800,
            "second_year_salary": 900,
            "third_year_salary": 1000,
            "fourth_year_salary": 1100,
            "best_paid": False,
            "popular": True,
            "image_url": "upload/images/users/user.png",
            "links": "ausbildung.de, fachinformatiker.de",
            "published": False
        }
        # PUT request to update the aus_page
        response = self.client.put(
            f'{api_routes_urls["aus_page"]["get_aus_pages_list"]}/{fake_aus_page.AusPageID}',
            json=update_data
        )

        # Assert that the response is as expected
        self.assertEqual(response.status_code, UPDATED)

        # Check if there is content in the response before trying to parse JSON
        if response.get_data(as_text=True):
            # Print the response content
            print(response.get_data(as_text=True))

            # Check if the aus_page in the fake database is updated
            updated_aus_page = AusPage.query.get(fake_aus_page.AusPageID)
            self.assertIsNotNone(updated_aus_page)
            self.assertEqual(updated_aus_page.Duration, 'Three years and half')
            self.assertEqual(updated_aus_page.CategorID, 2)
            self.assertEqual(updated_aus_page.FourthYearSalalry, 1100)
        else:
            print(f"Response contains only status code {response.status_code} and No JSON Content.")

    def test_delete_aus_page(self):
        fake_aus_page = self.create_and_insert_fake_aus_page()

        # Send a DELETE request to delete the aus_page
        response = self.client.delete(f'{api_routes_urls['aus_page']['get_aus_pages_list']}/{fake_aus_page.AusPageID}')
        # Check the response status code
        assert response.status_code == 204

        deleted_aus_page_response = self.client.get(
            f'{api_routes_urls['aus_page']['get_aus_pages_list']}/{fake_aus_page.AusPageID}')
        assert deleted_aus_page_response.status_code == NOT_FOUND
