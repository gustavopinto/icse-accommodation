from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    TextAreaField,
    SubmitField,
)
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError


class AccommodationRequestForm(FlaskForm):
    name = StringField(
        "Nome completo",
        validators=[DataRequired(), Length(min=2, max=60)],
        render_kw={"maxlength": "60", "minlength": "2"},
    )
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email()],
        render_kw={"type": "email", "maxlength": "100"},
    )
    institution = StringField(
        "Instituição",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"maxlength": "100"},
    )
    check_in = DateField(
        "Data de chegada",
        default=date(2026, 4, 12),
        validators=[DataRequired()],
    )
    check_out = DateField(
        "Data de saída",
        default=date(2026, 4, 18),
        validators=[DataRequired()],
    )
    gender = SelectField(
        "Eu me identifico como",
        choices=[
            ("masculino", "Masculino"),
            ("feminino", "Feminino"),
            ("nao_binario", "Não-binário"),
            ("outro", "Outro"),
            ("prefiro_nao_dizer", "Prefiro não dizer"),
        ],
        validators=[DataRequired()],
    )
    roommate_gender_pref = SelectField(
        "Procuro pessoas",
        choices=[
            ("sem_restricoes", "Sem restrições"),
            ("masculino", "Masculino"),
            ("feminino", "Feminino"),
            ("nao_binario", "Não-binário"),
            ("outro", "Outro"),
        ],
        validators=[DataRequired()],
    )
    smoker = BooleanField("Fumante")
    social_media = StringField(
        "Rede social",
        validators=[Optional(), Length(max=150)],
        render_kw={"type": "url", "maxlength": "150", "placeholder": "https://linkedin.com/in/…"},
    )
    website = StringField(
        "Site pessoal",
        validators=[Optional(), Length(max=150)],
        render_kw={"type": "url", "maxlength": "150", "placeholder": "https://…"},
    )
    notes = TextAreaField(
        "Observações",
        validators=[Optional(), Length(max=280)],
        render_kw={"maxlength": "280"},
    )
    data_sharing_consent = BooleanField(
        "Concordo com o compartilhamento dos meus dados",
        validators=[DataRequired(message="É necessário concordar com o compartilhamento dos dados para enviar o pedido.")],
    )
    submit = SubmitField("Registrar pedido")

    _EVENT_START = date(2026, 4, 10)
    _EVENT_END = date(2026, 4, 20)

    def validate_check_in(self, field):
        if field.data and not (self._EVENT_START <= field.data <= self._EVENT_END):
            raise ValidationError("Data fora do período do evento (10/04 a 20/04).")

    def validate_check_out(self, field):
        if field.data and not (self._EVENT_START <= field.data <= self._EVENT_END):
            raise ValidationError("Data fora do período do evento (10/04 a 20/04).")
        if self.check_in.data and field.data and field.data <= self.check_in.data:
            raise ValidationError("A data de saída deve ser posterior à data de chegada.")
