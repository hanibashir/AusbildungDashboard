from app.helpers.db.Queries import Queries
from app.models.aus_page import AusPage


class AusPageQueries(Queries):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.aus_page = AusPage

    def select_all(self):
        return self.aus_page.query.all()

    def insert_aus_page(self):

        image_url = self.data['image_url']
        registered_date = self.date_time.now()
        last_login = self.date_time.now()
        try:
            new_user = User(
                name=self.data['name'],
                password=generate_password_hash(self.data['password']),
                email=self.data['email'],
                image_url=image_url,
                registered_date=registered_date,
                last_login=last_login
            )
            # insert into users table
            self.insert(new_user)
            return self.message('user', self.status.CREATED)
        except self.sql_exception:
            return self.message('user', self.status.BAD_REQUEST)
