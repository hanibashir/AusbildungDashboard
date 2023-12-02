from app.models.category import Category
from app.utils.db.Queries import Queries


class CategoryQueries(Queries):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.category = Category

    def select_all(self):
        return self.category.query.all()
