import pytest
from datetime import datetime
from app import db
from app.models.user import User


@pytest.fixture
def test_db():
    # Set up a test database and create a session for the tests
    engine = db.create_engine('sqlite:///:memory:')
    session = db.sessionmaker(bind=engine)()

    # Create the User table
    User.metadata.create_all(engine)

    yield session

    # Drop all tables and close the session
    User.metadata.drop_all(engine)
    session.close()


def test_user_creation(test_db):
    user = User(
        name='John Doe',
        password='password123',
        email='john@example.com',
        image_url='https://example.com/image.jpg',
        registered_date=datetime.now(),
        last_login=datetime.now()
    )

    test_db.add(user)
    test_db.commit()

    # Retrieve the user from the database
    retrieved_user = test_db.query(User).filter_by(Name='John Doe').first()

    assert retrieved_user is not None
    assert retrieved_user.Name == 'John Doe'
    assert retrieved_user.Password == 'password123'
    assert retrieved_user.Email == 'john@example.com'
    assert retrieved_user.ImageUrl == 'https://example.com/image.jpg'
    assert retrieved_user.RegisteredDate is not None
    assert retrieved_user.LastLogin is not None


def test_to_dict_method():
    user = User(
        name='Jane Doe',
        password='pass123',
        email='jane@example.com',
        image_url=None,
        registered_date=datetime.now(),
        last_login=datetime.now()
    )

    user_dict = user.to_dict()

    assert isinstance(user_dict, dict)
    assert 'user_id' in user_dict
    assert 'name' in user_dict
    assert 'email' in user_dict
    assert 'image_url' in user_dict
    assert 'registered_date' in user_dict
    assert 'last_login' in user_dict


def test_repr_method():
    user = User(
        name='Alice',
        password='alicepass',
        email='alice@example.com',
        image_url='http://example.com/alice.jpg',
        registered_date=datetime.now(),
        last_login=datetime.now()
    )

    repr_string = repr(user)

    assert isinstance(repr_string, str)
    assert 'User' in repr_string
    assert 'UserID' in repr_string
    assert 'Name' in repr_string
    assert 'Email' in repr_string
    assert 'Image' in repr_string
    assert 'Reg.Date' in repr_string
    assert 'LastLogin' in repr_string
