from app import db
from app.data.models.category import Category
from app.utils.constants import CONFLICT, CREATED, BAD_REQUEST, UPDATED
from app.data.dashboard_queries.queries import Queries


class CategoryQueries(Queries):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.category = Category

    def select_all(self):
        return self.category.query.all()

    def select_category(self, category_id=None, title=None):
        if category_id:
            return db.session.get(self.category, category_id)
        if title:
            # Return the first result of this Query or None if the result doesn't contain any row.
            return self.category.query.filter_by(Title=title).first()

    def check_category_exists(self) -> tuple[bool, str]:
        cat_exists = self.select_category(title=self.data['title'])
        if cat_exists:
            return True, self.message(model='category', status=CONFLICT)
        else:
            return False, ''

    def insert_category(self, image_url=None):
        # title, description, image_url
        try:
            new_cat = Category(
                title=self.data['title'],
                description=self.category_description(),
                image_url=image_url
            )
            # insert into categories table
            self.insert(new_cat)
            return self.message('category', CREATED)
        except self.sql_exception as se:
            if se:
                return self.message('category', se)
            return self.message('category', BAD_REQUEST)

    def update_category(self, category: Category):
        # title, description, image_url
        try:
            category.Title = self.data['title']
            category.Description = self.category_description()
            category.ImageUrl = self.data['image_url']

            # commit changes to api_queries
            self.flush_and_commit()

            return self.message('category', UPDATED)
        except self.sql_exception:
            return self.message('category', BAD_REQUEST)

    def delete_category(self, cat_id) -> tuple[bool, str]:
        try:
            self.category.query.filter(Category.CategoryID == cat_id).delete()
            # commit changes to api_queries
            self.flush_and_commit()
            return True, self.message('category', 'DELETED')
        except self.sql_exception:
            return False, self.message('category', BAD_REQUEST)

    def category_description(self):
        if not self.data['description'] or self.data['description'] == '':
            return "No description"

        return self.data['description']
