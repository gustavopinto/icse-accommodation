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
        "Full name",
        validators=[DataRequired(), Length(min=2, max=60)],
        render_kw={"maxlength": "60", "minlength": "2"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"type": "email", "maxlength": "100"},
    )
    institution = StringField(
        "Institution",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"maxlength": "100"},
    )
    check_in = DateField(
        "Check-in date",
        default=date(2026, 4, 12),
        validators=[DataRequired()],
    )
    check_out = DateField(
        "Check-out date",
        default=date(2026, 4, 18),
        validators=[DataRequired()],
    )
    gender = SelectField(
        "I identify as",
        choices=[
            ("masculino", "Male"),
            ("feminino", "Female"),
            ("nao_binario", "Non-binary"),
            ("outro", "Other"),
            ("prefiro_nao_dizer", "Prefer not to say"),
        ],
        validators=[DataRequired()],
    )
    roommate_gender_pref = SelectField(
        "I'm looking for",
        choices=[
            ("sem_restricoes", "No preference"),
            ("masculino", "Male"),
            ("feminino", "Female"),
            ("nao_binario", "Non-binary"),
            ("outro", "Other"),
        ],
        validators=[DataRequired()],
    )
    smoker = BooleanField("Smoker")
    social_media = StringField(
        "Social media",
        validators=[Optional(), Length(max=150)],
        render_kw={"type": "url", "maxlength": "150", "placeholder": "https://linkedin.com/in/…"},
    )
    website = StringField(
        "Personal website",
        validators=[Optional(), Length(max=150)],
        render_kw={"type": "url", "maxlength": "150", "placeholder": "https://…"},
    )
    notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(max=280)],
        render_kw={"maxlength": "280"},
    )
    data_sharing_consent = BooleanField(
        "I agree to share my data publicly",
        validators=[DataRequired(message="You must agree to share your data to submit the request.")],
    )
    submit = SubmitField("Submit request")

    _EVENT_START = date(2026, 4, 10)
    _EVENT_END = date(2026, 4, 20)

    def validate_check_in(self, field):
        if field.data and not (self._EVENT_START <= field.data <= self._EVENT_END):
            raise ValidationError("Date outside the event period (Apr 10–Apr 20).")

    def validate_check_out(self, field):
        if field.data and not (self._EVENT_START <= field.data <= self._EVENT_END):
            raise ValidationError("Date outside the event period (Apr 10–Apr 20).")
        if self.check_in.data and field.data and field.data <= self.check_in.data:
            raise ValidationError("Check-out date must be after check-in date.")
