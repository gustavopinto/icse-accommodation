from datetime import datetime, timezone
from app import db


class AccommodationRequest(db.Model):
    __tablename__ = "accommodation_requests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, index=True)
    institution = db.Column(db.String(200), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    roommate_gender_pref = db.Column(db.String(20), nullable=False)
    smoker = db.Column(db.Boolean, default=False, nullable=False)
    accepts_smoker = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    social_media = db.Column(db.String(300), nullable=True)
    website = db.Column(db.String(300), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<AccommodationRequest {self.name} ({self.email})>"
