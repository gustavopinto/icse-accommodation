from flask import Blueprint, current_app, render_template, redirect, url_for, flash
from app.forms.accommodation import AccommodationRequestForm
from app.backup import load_all, save_new

accommodation_bp = Blueprint("accommodation", __name__)


@accommodation_bp.route("/", methods=["GET"])
def index():
    requests = load_all(current_app)
    form = AccommodationRequestForm()
    return render_template("main/acomodacoes.html", requests=requests, form=form)


@accommodation_bp.route("/", methods=["POST"])
def create():
    form = AccommodationRequestForm()
    if form.validate_on_submit():
        try:
            save_new(
                current_app,
                name=form.name.data,
                email=form.email.data,
                institution=form.institution.data,
                check_in=form.check_in.data,
                check_out=form.check_out.data,
                gender=form.gender.data,
                roommate_gender_pref=form.roommate_gender_pref.data,
                smoker=form.smoker.data,
                social_media=form.social_media.data or None,
                website=form.website.data or None,
                notes=form.notes.data or None,
            )
        except OSError:
            flash("Erro ao salvar. Tente novamente.", "error")
            requests = load_all(current_app)
            return render_template("main/acomodacoes.html", requests=requests, form=form)
        flash("Pedido de acomodação registrado com sucesso!", "success")
        return redirect(url_for("accommodation.index"))

    requests = load_all(current_app)
    return render_template("main/acomodacoes.html", requests=requests, form=form)
