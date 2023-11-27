from app import db
from sqlalchemy.orm import relationship


class UserRole(db.Model):
    __tablename__ = 'UsersRoles'

    UserRoleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    RoleID = db.Column(db.Integer, db.ForeignKey('Roles.RoleID'))

    # Define relationships with the Users and Roles tables
    user = relationship('User', backref='user_roles')
    role = relationship('Role', backref='role_users')

    def __init__(self, user_id, role_id):
        self.UserID = user_id
        self.RoleID = role_id

    def __repr__(self):
        return f"<UserRole(UserRoleID={self.UserRoleID}, UserID={self.UserID}, RoleID={self.RoleID})>"
