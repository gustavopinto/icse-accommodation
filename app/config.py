import os


def _database_uri() -> str:
    url = (os.environ.get("DATABASE_URL") or "").strip()
    if not url:
        url = "sqlite:///app.db"
    # Alguns PaaS usam postgres://; SQLAlchemy 1.4+ exige postgresql://
    elif url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    # E-mail (MailerSend SMTP). Notifications sent to MAIL_NOTIFY_TO on new accommodation.
    SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.mailersend.net")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USERNAME = os.environ.get("SMTP_USERNAME") or ""
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD") or ""
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@localhost")
    MAIL_DEFAULT_SENDER_NAME = os.environ.get("MAIL_DEFAULT_SENDER_NAME", "")
    MAIL_NOTIFY_TO = os.environ.get("MAIL_NOTIFY_TO", "gpinto@ufpa.br")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
