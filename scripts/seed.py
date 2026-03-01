"""Script para popular o banco com dados iniciais."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="admin@example.com").first():
        admin = User(name="Admin", email="admin@example.com")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin criado: admin@example.com / admin123")
    else:
        print("Admin já existe.")
