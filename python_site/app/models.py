import json
from datetime import datetime

from .database import db


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    crop_type = db.Column(db.String(64), nullable=False)
    disease_name = db.Column(db.String(128), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(16), nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    is_healthy = db.Column(db.Boolean, default=False, nullable=False)
    image_path = db.Column(db.String(256), nullable=True)
    top_candidates = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cropType": self.crop_type,
            "diseaseName": self.disease_name,
            "confidence": self.confidence,
            "severity": self.severity,
            "treatment": self.treatment,
            "isHealthy": self.is_healthy,
            "imagePath": self.image_path,
            "topCandidates": json.loads(self.top_candidates) if self.top_candidates else [],
            "createdAt": self.created_at.isoformat(),
        }


class Disease(db.Model):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    crop_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(16), nullable=False)

    __table_args__ = (db.UniqueConstraint("name", "crop_type", name="uq_disease_name_crop"),)
