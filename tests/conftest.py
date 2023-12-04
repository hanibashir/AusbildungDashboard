import os
import tempfile
import pytest
from app import create_app, db


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

# @pytest.fixture
# def app():
#     app = create_app()
#     with app.app_context():
#         yield app
#         db.session.remove()
#         db.drop_all()
#
#
# @pytest.fixture
# def client(app):
#     with app.test_client() as client:
#         db.create_all()
#         yield client
