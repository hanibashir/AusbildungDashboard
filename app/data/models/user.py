from app import db


class User(db.Model):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(250))
    Password = db.Column(db.String(250))
    Email = db.Column(db.String(250))
    ImageUrl = db.Column(db.Text, nullable=True)
    About = db.Column(db.Text, nullable=True)
    RegisteredDate = db.Column(db.DateTime)
    LastLogin = db.Column(db.DateTime)

    def __init__(self, name, password, email, image_url, about, registered_date, last_login):
        self.Name = name
        self.Password = password
        self.Email = email
        self.ImageUrl = image_url
        self.about = about
        self.RegisteredDate = registered_date
        self.LastLogin = last_login

    def to_dict(self):
        return {
            "user_id": self.UserID,
            "name": self.Name,
            "email": self.Email,
            "image_url": self.ImageUrl,
            "about": self.about,
            "registered_date": self.RegisteredDate,
            "last_login": self.LastLogin
        }

    def __repr__(self):
        return (f""
                f"<User(UserID={self.UserID}, "
                f"Name={self.Name}, "
                f"Email={self.Email},"
                f"Image={self.ImageUrl},"
                f"About={self.About},"
                f"Reg.Date={self.RegisteredDate},"
                f"LastLogin={self.LastLogin})>")
