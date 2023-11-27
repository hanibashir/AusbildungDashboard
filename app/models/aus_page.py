from sqlalchemy.orm import relationship

from app import db


class AusPage(db.Model):
    __tablename__ = 'AusPages'

    AusPageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(250))
    ImageUrl = db.Column(db.Text, nullable=True)
    ShiftType = db.Column(db.String(250), nullable=True)
    Duration = db.Column(db.String(250))
    Certificate = db.Column(db.String(250))
    FirstYearSalary = db.Column(db.Integer, default=0)
    SecondYearSalary = db.Column(db.Integer, default=0)
    ThirdYearSalary = db.Column(db.Integer, default=0)
    FourthYearSalary = db.Column(db.Integer, default=0)
    Content = db.Column(db.Text)
    BestPaid = db.Column(db.Boolean, default=False)
    Popular = db.Column(db.Boolean, default=False)
    Links = db.Column(db.Text, nullable=True)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Categories.CategoryID'))
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    Published = db.Column(db.Boolean, default=False)
    PublishedDate = db.Column(db.DateTime)
    UpdatedDate = db.Column(db.DateTime)

    # Relationships with the Categories and Users tables
    category = relationship('Category', backref='aus_pages')
    user = relationship('User', backref='aus_pages')

    def __init__(self, title, duration, certificate, content, category_id, user_id, published_date, updated_date,
                 image_url=None, shift_type=None, first_year_salary=0, second_year_salary=0, third_year_salary=0,
                 fourth_year_salary=0, best_paid=False, popular=False, links=None, published=False):
        self.Title = title
        self.ImageUrl = image_url
        self.ShiftType = shift_type
        self.Duration = duration
        self.Certificate = certificate
        self.FirstYearSalary = first_year_salary
        self.SecondYearSalary = second_year_salary
        self.ThirdYearSalary = third_year_salary
        self.FourthYearSalary = fourth_year_salary
        self.Content = content
        self.BestPaid = best_paid
        self.Popular = popular
        self.Links = links
        self.CategoryID = category_id
        self.UserID = user_id
        self.Published = published
        self.PublishedDate = published_date
        self.UpdatedDate = updated_date

    def to_dict(self):
        return {
            "title": self.Title,
            "duration": self.Duration,
            "certificate": self.Certificate,
            "content": self.Content,
            "category_id": self.CategoryID,
            "user_id": self.UserID,
            "shift_type": "دوام متغير",
            "first_year_salary": self.FirstYearSalary,
            "second_year_salary": self.SecondYearSalary,
            "third_year_salary": self.ThirdYearSalary,
            "fourth_year_salary": self.FourthYearSalary,
            "best_paid": self.BestPaid,
            "popular": self.Popular,
            "image_url": "upload/images/users/user.png",
            "links": self.Links,
            "published": self.Published
        }

    def __repr__(self):
        return f"<AusPage(AusPageID={self.AusPageID}, Title={self.Title})>"
