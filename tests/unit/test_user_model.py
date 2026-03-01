from app.models.user import User


def test_password_hashing(app):
    with app.app_context():
        u = User(name="Alice", email="alice@example.com")
        u.set_password("secret")
        assert u.check_password("secret") is True
        assert u.check_password("wrong") is False


def test_user_repr(app):
    with app.app_context():
        u = User(name="Bob", email="bob@example.com")
        assert "bob@example.com" in repr(u)
