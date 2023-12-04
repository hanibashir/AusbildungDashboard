from app import db
from app.models.category import Category
from app.utils.db.Queries import Queries


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
            return True, self.message(model='category', status=self.status.CONFLICT)
        else:
            return False, ''

    def insert_category(self):
        # title, description, image_url
        try:
            new_cat = Category(
                title=self.data['title'],
                description=self.data['description'],
                image_url=self.data['image_url']
            )
            # insert into categories table
            self.insert(new_cat)
            return self.message('category', self.status.CREATED)
        except self.sql_exception:
            return self.message('category', self.status.BAD_REQUEST)
