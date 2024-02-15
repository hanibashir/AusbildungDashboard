from app import db
from sqlalchemy.orm import relationship


class Page(db.Model):
    __tablename__ = 'Pages'

    PageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(250))
    Content = db.Column(db.Text)
    ImageUrl = db.Column(db.Text, nullable=True)
    Links = db.Column(db.Text, nullable=True)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Categories.CategoryID'))
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    Published = db.Column(db.Boolean, default=False)
    PublishedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)

    # Define relationships with the Categories and Users tables
    category = relationship('Category', backref='pages')
    user = relationship('User', backref='pages')

    def __init__(self, title, content, category_id, user_id, published_date, updated_date, published=False,
                 image_url=None, links=None):
        self.Title = title
        self.Content = content
        self.ImageUrl = image_url
        self.Links = links
        self.CategoryID = category_id
        self.UserID = user_id
        self.PublishedDate = published_date
        self.UpdatedDate = updated_date
        self.Published = published

    def to_dict(self):
        return {
            "page_id": self.PageID,
            "title": self.Title,
            "content": self.Content,
            "category_id": self.CategoryID,
            "user_id": self.UserID,
            "image_url": "upload/images/users/profile.png",
            "links": self.Links,
            "published": self.Published
        }

    def __repr__(self):
        return f"<Page(PageID={self.PageID}, Title={self.Title})>"
