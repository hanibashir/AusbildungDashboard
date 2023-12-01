from app.utils.db.Queries import Queries
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

    def select_aus_page(self, page_id):
        return self.aus_page.query.get(page_id)

    def update_aus_page(self, aus_page: AusPage):
        # title, duration, certificate, content, category_id, user_id, published_date, updated_date,
        # image_url = None, shift_type = None, first_year_salary = 0, second_year_salary = 0, third_year_salary = 0,
        # fourth_year_salary = 0, best_paid = False, popular = False, links = None, published = False
        aus_page_img = self.data['image_url']
        published_date = aus_page.PublishedDate
        updated_date = self.date_time.now()

        try:
            aus_page.Title = self.data['title']
            aus_page.Duration = self.data['duration']
            aus_page.Certificate = self.data['certificate']
            aus_page.Content = self.data['content']
            aus_page.CategoryID = self.data['category_id']
            aus_page.UserID = self.data['user_id']
            aus_page.content = self.data['content']
            aus_page.ShiftType = self.data['shift_type']
            aus_page.FirstYearSalary = self.data['first_year_salary']
            aus_page.SecondYearSalary = self.data['second_year_salary']
            aus_page.ThirdYearSalary = self.data['third_year_salary']
            aus_page.FourthYearSalary = self.data['fourth_year_salary']
            aus_page.BestPaid = self.data['best_paid']
            aus_page.Popular = self.data['popular']
            aus_page.Links = self.data['links']
            aus_page.Published = self.data['published']
            aus_page.ImageUrl = aus_page_img
            aus_page.PublishedDate = published_date
            aus_page.UpdatedDate = updated_date

            # commit changes to db
            self.flush_and_commit()

            return self.message('aus_page', self.status.OK, field='updated')
        except self.sql_exception:
            return self.message('aus_page', self.status.BAD_REQUEST)

    def delete_aus_page(self, page_id) -> tuple[bool, str]:
        try:
            self.aus_page.query.filter(AusPage.AusPageID == page_id).delete()
            # commit changes to db
            self.flush_and_commit()
            return True, self.message('aus_page', self.status.OK, field='deleted')
        except self.sql_exception:
            return False, self.message('aus_page', self.status.BAD_REQUEST)
