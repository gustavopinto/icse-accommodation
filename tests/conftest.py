import pytest
from app import create_app, db as _db
from app.models.user import User


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    yield _db
    _db.session.rollback()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user(db):
    u = User(name="Test User", email="test@example.com")
    u.set_password("password123")
    db.session.add(u)
    db.session.commit()
    yield u
    db.session.delete(u)
    db.session.commit()
