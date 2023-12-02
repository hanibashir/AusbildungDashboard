from app import db
from app.utils.db.Queries import Queries
from app.models.user import User
from werkzeug.security import generate_password_hash


class UserQueries(Queries):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.user = User

    def select_all(self):
        return self.user.query.all()

    def select_user(self, user_id=None, email=None):
        if user_id:
            return db.session.get(self.user, user_id)
        if email:
            # Return the first result of this Query or None if the result doesn't contain any row.
            return self.user.query.filter_by(Email=email).first()

    def check_email_exists(self) -> tuple[bool, str]:
        email_exists = self.select_user(email=self.data['email'])
        if email_exists:
            return True, self.message(model='user', status=self.status.CONFLICT)
        else:
            return False, ''

    def insert_user(self):
        # name, password, confirm_password, email, image_url, registered_date, last_login
        image_url = self.data['image_url']
        registered_date = self.date_time.now()
        last_login = self.date_time.now()
        try:
            new_user = User(
                name=self.data['name'],
                password=generate_password_hash(self.data['password']),
                email=self.data['email'],
                image_url=image_url,
                registered_date=registered_date,
                last_login=last_login
            )
            # insert into users table
            self.insert(new_user)
            return self.message('user', self.status.CREATED)
        except self.sql_exception:
            return self.message('user', self.status.BAD_REQUEST)

    def update_user(self, user):
        # name, password, confirm_password, email, image_url, registered_date, last_login
        user_img = self.data['image_url']
        registered_date = user.RegisteredDate
        last_login = user.LastLogin
        try:
            user.Name = self.data['name']
            user.Password = generate_password_hash(self.data['password'])
            user.Email = self.data['email']
            user.ImageUrl = user_img
            user.RegisteredDate = registered_date
            user.LastLogin = last_login

            # commit changes to db
            self.flush_and_commit()

            return self.message('user', self.status.OK, field='updated')
        except self.sql_exception:
            return self.message('user', self.status.BAD_REQUEST)

    def delete_user(self, user_id) -> tuple[bool, str]:
        try:
            self.user.query.filter(User.UserID == user_id).delete()
            # commit changes to db
            self.flush_and_commit()
            return True, self.message('user', self.status.OK, field='deleted')
        except self.sql_exception:
            return False, self.message('user', self.status.BAD_REQUEST)
