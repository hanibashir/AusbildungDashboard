from app import db


class Category(db.Model):
    __tablename__ = 'Categories'

    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(250))
    Description = db.Column(db.Text, nullable=True)
    ImageUrl = db.Column(db.Text, nullable=True)

    def __init__(self, title, description=None, image_url=None):
        self.Title = title
        self.Description = description
        self.ImageUrl = image_url

    def to_dict(self):
        return {
            "Category_id": self.CategoryID,
            "title": self.Title,
            "description": self.Description,
            "image_url": self.ImageUrl
        }

    def __repr__(self):
        return f"<Category(CategoryID={self.CategoryID}, Title={self.Title})>"
