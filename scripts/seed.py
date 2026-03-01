"""Script para popular o banco com dados iniciais."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.admin import Admin

app = create_app()

with app.app_context():
    db.create_all()

    username = os.environ.get("ADMIN_USERNAME", "").strip()
    password = os.environ.get("ADMIN_PASSWORD", "").strip()
    if not username or not password:
        print("Defina ADMIN_USERNAME e ADMIN_PASSWORD no .env para criar o administrador.")
        sys.exit(1)

    if not Admin.query.filter_by(username=username).first():
        admin_user = Admin(username=username)
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Administrador (painel /admin) criado: {username}")
    else:
        print(f"Administrador {username} já existe.")
