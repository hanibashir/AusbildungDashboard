from instance.base import db
from app.utils.messages import message
from datetime import datetime
from sqlalchemy import exc


class Queries:
    def __init__(self):
        self.db = db
        self.message = message
        self.date_time = datetime
        self.sql_exception = exc.SQLAlchemyError

    def flush_and_commit(self):
        self.db.session.flush()
        self.db.session.commit()

    def insert(self, model=None):
        if model:
            self.db.session.add(model)
        self.flush_and_commit()
        return "inserted"

    def delete(self):
        pass
