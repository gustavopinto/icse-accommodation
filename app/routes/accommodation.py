from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.forms.accommodation import AccommodationRequestForm
from app.models.accommodation import AccommodationRequest

accommodation_bp = Blueprint("accommodation", __name__)


@accommodation_bp.route("/", methods=["GET"])
def index():
    requests = AccommodationRequest.query.order_by(
        AccommodationRequest.created_at.desc()
    ).all()
    form = AccommodationRequestForm()
    return render_template("main/acomodacoes.html", requests=requests, form=form)


@accommodation_bp.route("/", methods=["POST"])
def create():
    form = AccommodationRequestForm()
    if form.validate_on_submit():
        try:
            entry = AccommodationRequest(
                name=form.name.data,
                email=form.email.data,
                institution=form.institution.data,
                check_in=form.check_in.data,
                check_out=form.check_out.data,
                gender=form.gender.data,
                roommate_gender_pref=form.roommate_gender_pref.data,
                smoker=form.smoker.data,
                accepts_smoker=False,
                social_media=form.social_media.data or None,
                website=form.website.data or None,
                notes=form.notes.data or None,
            )
            db.session.add(entry)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Erro ao salvar. Tente novamente.", "error")
            requests = AccommodationRequest.query.order_by(
                AccommodationRequest.created_at.desc()
            ).all()
            return render_template("main/acomodacoes.html", requests=requests, form=form)
        flash("Pedido de acomodação registrado com sucesso!", "success")
        return redirect(url_for("accommodation.index"))

    requests = AccommodationRequest.query.order_by(
        AccommodationRequest.created_at.desc()
    ).all()
    return render_template("main/acomodacoes.html", requests=requests, form=form)
