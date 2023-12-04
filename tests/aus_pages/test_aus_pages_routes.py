from app.utils.constants import Status, api_routes_urls

aus_pages_data = {
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


def test_create_user(client):
    response = client.post(
        api_routes_urls['aus_page']['create_aus_page'],
        json=aus_pages_data
    )
    assert response.status_code == Status.CREATED.value


def test_get_all_users(client):
    response = client.get(api_routes_urls['aus_page']['get_aus_pages_list'])
    assert response.status_code == Status.OK.value
