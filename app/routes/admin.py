from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from app import db
from app.models.accommodation import AccommodationRequest
from app.models.admin import Admin

admin_bp = Blueprint("admin", __name__)


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.index"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(
            username=form.username.data, active=True
        ).first()
        if admin and admin.check_password(form.password.data):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.index"))
        flash("Invalid username or password.", "danger")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@admin_required
def index():
    entries = AccommodationRequest.query.filter_by(active=True).order_by(
        AccommodationRequest.created_at.desc()
    ).all()
    return render_template("admin/index.html", entries=entries)


@admin_bp.route("/delete/<int:entry_id>", methods=["POST"])
@admin_required
def delete(entry_id):
    entry = db.session.get(AccommodationRequest, entry_id)
    if entry:
        entry.active = False
        db.session.commit()
        flash(f"Entry for {entry.name} removed.", "success")
    else:
        flash("Entry not found.", "danger")
    return redirect(url_for("admin.index"))
