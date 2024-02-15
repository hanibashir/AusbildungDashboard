from flask import session
from app import db
from app.utils.constants import CREATED, BAD_REQUEST, UPDATED
from app.database.api_queries.queries import Queries
from app.data.models.post import Post


class PostQueries(Queries):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.post = Post

    def select_all(self):
        return self.post.query.all()

    def insert_post(self, image_short_path):
        published_date = self.date_time.now()
        updated_date = self.date_time.now()

        try:
            new_post = Post(
                title=self.data['title'],
                duration=self.data['duration'],
                certificate=self.data['certificate'],
                content=self.data['content'],
                category_id=self.data['category_id'],
                user_id=session['user_id'],
                published_date=published_date,
                updated_date=updated_date,
                image_url=image_short_path or None,
                shift_type=self.data['shift_type'] or None,
                first_year_salary=self.data['first_year_salary'] or 0,
                second_year_salary=self.data['second_year_salary'] or 0,
                third_year_salary=self.data['third_year_salary'] or 0,
                fourth_year_salary=self.data['fourth_year_salary'] or 0,
                best_paid=self.data['best_paid'] or False,
                popular=self.data['popular'] or False,
                # links=self.data['links'] or None,
                published=self.data['publish'] or False
            )

            # insert into users table
            self.insert(new_post)

            return self.message('aus_page', CREATED)
        except self.sql_exception:
            return self.message('aus_page', BAD_REQUEST)

    def select_post(self, post_id):
        return db.session.get(self.post, post_id)
        # return self.aus_page.query.get(page_id)

    def update_post(self, post: Post):
        # title, duration, certificate, content, category_id, user_id, published_date, updated_date,
        # image_url = None, shift_type = None, first_year_salary = 0, second_year_salary = 0, third_year_salary = 0,
        # fourth_year_salary = 0, best_paid = False, popular = False, links = None, published = False
        published_date = post.PublishedDate
        updated_date = self.date_time.now()

        try:
            post.Title = self.data['title']
            post.Duration = self.data['duration']
            post.Certificate = self.data['certificate']
            post.Content = self.data['content']
            post.CategoryID = self.data['category_id']
            post.UserID = self.data['user_id']
            post.ShiftType = self.data['shift_type']
            post.FirstYearSalary = self.data['first_year_salary']
            post.SecondYearSalary = self.data['second_year_salary']
            post.ThirdYearSalary = self.data['third_year_salary']
            post.FourthYearSalary = self.data['fourth_year_salary']
            post.BestPaid = self.data['best_paid']
            post.Popular = self.data['popular']
            post.Links = self.data['links']
            post.Published = self.data['published']
            post.ImageUrl = self.data['image_url']
            post.PublishedDate = published_date
            post.UpdatedDate = updated_date

            # commit changes to api_queries
            self.flush_and_commit()

            return self.message('aus_page', UPDATED)
        except self.sql_exception:
            return self.message('aus_page', BAD_REQUEST)

    def delete_post(self, page_id) -> tuple[bool, str]:
        try:
            self.post.query.filter(Post.AusPageID == page_id).delete()
            # commit changes to api_queries
            self.flush_and_commit()
            return True, self.message('aus_page', 204)
        except self.sql_exception:
            return False, self.message('aus_page', BAD_REQUEST)
