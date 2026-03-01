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

    if not Admin.query.filter_by(username="ghlp").first():
        admin_user = Admin(username="ghlp")
        admin_user.set_password("1234")
        db.session.add(admin_user)
        db.session.commit()
        print("Administrador (painel /admin) criado: ghlp / 1234")
    else:
        print("Administrador ghlp já existe.")
