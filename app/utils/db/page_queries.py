from app import db
from app.models.page import Page
from app.utils.constants import CREATED, BAD_REQUEST, UPDATED
from app.utils.db.queries import Queries


class PageQueries(Queries):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.page = Page

    def select_all(self):
        return self.page.query.all()

    def insert_page(self):
        # title, content, category_id, user_id, published_date, updated_date, published=False,
        # image_url=None, links=None
        published_date = self.date_time.now()
        updated_date = self.date_time.now()

        try:
            new_aus = Page(
                title=self.data['title'],
                content=self.data['content'],
                category_id=self.data['category_id'],
                user_id=self.data['user_id'],
                published_date=published_date,
                updated_date=updated_date,
                image_url=self.data['image_url'] or None,
                links=self.data['links'] or None,
                published=self.data['published'] or False
            )
            # insert into users table
            self.insert(new_aus)
            return self.message('page', CREATED)
        except self.sql_exception:
            return self.message('page', BAD_REQUEST)

    def select_page(self, page_id):
        return db.session.get(self.page, page_id)

    def update_page(self, page: Page):
        # title, content, category_id, user_id, published_date, updated_date, published=False,
        # image_url=None, links=None
        published_date = page.PublishedDate
        updated_date = self.date_time.now()

        try:
            page.Title = self.data['title']
            page.Content = self.data['content']
            page.CategoryID = self.data['category_id']
            page.UserID = self.data['user_id']
            page.Links = self.data['links']
            page.Published = self.data['published']
            page.ImageUrl = self.data['image_url']
            page.PublishedDate = published_date
            page.UpdatedDate = updated_date

            # commit changes to db
            self.flush_and_commit()

            return self.message('page', UPDATED)
        except self.sql_exception:
            return self.message('page', BAD_REQUEST)

    def delete_page(self, page_id) -> tuple[bool, str]:
        try:
            self.page.query.filter(Page.PageID == page_id).delete()
            # commit changes to db
            self.flush_and_commit()
            return True, self.message('page', 'DELETED')
        except self.sql_exception:
            return False, self.message('page', BAD_REQUEST)
