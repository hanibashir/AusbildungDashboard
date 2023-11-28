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
        published_date = self.date_time.now()
        updated_date = self.date_time.now()

        try:
            new_aus = AusPage(
                title=self.data['title'],
                duration=self.data['duration'],
                certificate=self.data['certificate'],
                content=self.data['content'],
                category_id=self.data['category_id'],
                user_id=self.data['user_id'],
                published_date=published_date,
                updated_date=updated_date,
                image_url=self.data['image_url'] or None,
                shift_type=self.data['shift_type'] or None,
                first_year_salary=self.data['first_year_salary'] or 0,
                second_year_salary=self.data['second_year_salary'] or 0,
                third_year_salary=self.data['third_year_salary'] or 0,
                fourth_year_salary=self.data['fourth_year_salary'] or 0,
                best_paid=self.data['best_paid'] or False,
                popular=self.data['popular'] or False,
                links=self.data['links'] or None,
                published=self.data['published'] or False
            )
            # insert into users table
            self.insert(new_aus)
            return self.message('aus_page', self.status.CREATED)
        except self.sql_exception:
            return self.message('aus_page', self.status.BAD_REQUEST)
