from flask import session
from app import db
from app.models.category import Category
from app.utils.constants import CREATED, BAD_REQUEST, UPDATED
from app.utils.dashboard_queries.queries import Queries
from app.models.post import Post


class PostService(Queries):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.post = Post

    def get_all_posts(self):
        return self.post.query.all()

    def get_posts_by_user_id(self, user_id):
        return self.post.query.filter_by(UserID=user_id)

    def get_post_by_id(self, post_id):
        return db.session.get(self.post, post_id)
        # return self.post.query.get(page_id)

    def insert_post(self, image_url):
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
                image_url=image_url or None,
                shift_type=self.data['shift_type'] or None,
                first_year_salary=self.data['first_year_salary'] or 0,
                second_year_salary=self.data['second_year_salary'] or 0,
                third_year_salary=self.data['third_year_salary'] or 0,
                fourth_year_salary=self.data['fourth_year_salary'] or 0,
                popular=int(self.data.get('popular', 0)),
                best_paid=int(self.data.get('best_paid', 0)),
                # links=self.data['links'] or None,
                published=int(self.data.get('publish', 0))
            )

            # insert into users table
            self.insert(new_post)

            return self.message('post', CREATED)
        except self.sql_exception as se:
            if se:
                return se
            return self.message('post', BAD_REQUEST)

    def update_post(self, post: Post, image_url=None):
        """
            title, duration, certificate, content, category_id, user_id, published_date, updated_date,
            image_url = None, shift_type = None, first_year_salary = 0, second_year_salary = 0, third_year_salary = 0,
            fourth_year_salary = 0, best_paid = False, popular = False, links = None, published = False
        """
        updated_date = self.date_time.now()

        try:
            post.Title = self.data['title']
            post.Duration = self.data['duration']
            post.Certificate = self.data['certificate']
            post.Content = self.data['content']
            post.CategoryID = self.data['category_id']
            post.UserID = session['user_id']
            post.ShiftType = self.data['shift_type']
            post.FirstYearSalary = self.data['first_year_salary']
            post.SecondYearSalary = self.data['second_year_salary']
            post.ThirdYearSalary = self.data['third_year_salary']
            post.FourthYearSalary = self.data['fourth_year_salary']
            post.Popular = int(self.data.get('popular', 0))
            post.Best_paid = int(self.data.get('best_paid', 0))
            # links=self.data['links'] or None,
            post.Published = int(self.data.get('publish', 0))
            post.ImageUrl = image_url
            post.UpdatedDate = updated_date

            # commit changes to api_queries
            self.flush_and_commit()

            return self.message('post', UPDATED)
        except self.sql_exception as se:
            if se:
                return False, se
            return self.message('post', BAD_REQUEST)

    def delete_post(self, post_id) -> tuple[bool, str]:
        try:
            self.post.query.filter(Post.PostID == post_id).delete()
            # commit changes to api_queries
            self.flush_and_commit()
            return True, self.message('post', 'DELETED')
        except self.sql_exception as se:
            if se:
                return False, se
            return False, self.message('post', BAD_REQUEST)
