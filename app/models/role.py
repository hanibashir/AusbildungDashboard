from app import db


class Role(db.Model):
    __tablename__ = 'Roles'

    RoleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(250))
    Description = db.Column(db.String(250), default="No Description")

    def __init__(self, title, description="No Description"):
        self.Title = title
        self.Description = description

    def __repr__(self):
        return f"<Role(RoleID={self.RoleID}, Title={self.Title}, Description={self.Description})>"
