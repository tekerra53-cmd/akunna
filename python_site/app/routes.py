from __future__ import annotations

import json

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from sqlalchemy import desc, func, or_

from .database import db
from .models import Disease, Prediction
from .utils import allowed_file, save_uploaded_file

main_bp = Blueprint("main", __name__)

CROP_OPTIONS = [
    "maize",
    "cassava",
    "rice",
    "tomato",
    "potato",
    "pepper",
    "apple",
    "grape",
]


def _prediction_engine():
    return current_app.extensions["prediction_engine"]


@main_bp.get("/")
def dashboard():
    total_scans = db.session.query(func.count(Prediction.id)).scalar() or 0
    healthy_scans = db.session.query(func.count(Prediction.id)).filter(Prediction.is_healthy.is_(True)).scalar() or 0
    avg_confidence = db.session.query(func.avg(Prediction.confidence)).scalar() or 0.0
    most_common = (
        db.session.query(Prediction.disease_name, func.count(Prediction.id).label("cnt"))
        .group_by(Prediction.disease_name)
        .order_by(desc("cnt"))
        .first()
    )
    recent = Prediction.query.order_by(Prediction.created_at.desc()).limit(8).all()
    distribution = (
        db.session.query(Prediction.disease_name, func.count(Prediction.id).label("cnt"))
        .group_by(Prediction.disease_name)
        .order_by(desc("cnt"))
        .all()
    )

    return render_template(
        "dashboard.html",
        stats={
            "total_scans": total_scans,
            "healthy_scans": healthy_scans,
            "diseased_scans": max(total_scans - healthy_scans, 0),
            "avg_confidence": avg_confidence,
            "most_common_disease": most_common[0] if most_common else "N/A",
        },
        recent=recent,
        distribution=distribution,
    )


@main_bp.route("/scan", methods=["GET", "POST"])
def scan():
    if request.method == "GET":
        return render_template("scan.html", crop_options=CROP_OPTIONS)

    image = request.files.get("leaf_image")
    crop_hint = request.form.get("crop_type", "").strip() or None
    if crop_hint == "auto":
        crop_hint = None

    if not image or not image.filename:
        flash("Upload a leaf image first.", "danger")
        return redirect(url_for("main.scan"))

    if not allowed_file(image.filename):
        flash("Unsupported image format. Use JPG, PNG, or WEBP.", "danger")
        return redirect(url_for("main.scan"))

    filename, image_path = save_uploaded_file(image, current_app.config["UPLOAD_DIR"])
    prediction_payload = _prediction_engine().predict(image_path=image_path, crop_hint=crop_hint)

    prediction = Prediction(
        crop_type=prediction_payload["crop_type"],
        disease_name=prediction_payload["disease_name"],
        confidence=prediction_payload["confidence"],
        severity=prediction_payload["severity"],
        treatment=prediction_payload["treatment"],
        is_healthy=prediction_payload["is_healthy"],
        image_path=filename,
        top_candidates=json.dumps(prediction_payload.get("top_candidates", [])),
    )
    db.session.add(prediction)
    db.session.commit()

    flash("Scan completed successfully.", "success")
    return redirect(url_for("main.result_detail", prediction_id=prediction.id))


@main_bp.get("/history")
def history():
    search = request.args.get("q", "").strip()
    query = Prediction.query
    if search:
        like = f"%{search}%"
        query = query.filter(or_(Prediction.crop_type.ilike(like), Prediction.disease_name.ilike(like)))
    rows = query.order_by(Prediction.created_at.desc()).limit(200).all()
    return render_template("history.html", predictions=rows, search=search)


@main_bp.get("/results/<int:prediction_id>")
def result_detail(prediction_id: int):
    prediction = Prediction.query.get_or_404(prediction_id)
    top_candidates = json.loads(prediction.top_candidates) if prediction.top_candidates else []
    return render_template("result_detail.html", prediction=prediction, top_candidates=top_candidates)


@main_bp.get("/diseases")
def diseases():
    search = request.args.get("q", "").strip()
    query = Disease.query
    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                Disease.name.ilike(like),
                Disease.crop_type.ilike(like),
                Disease.description.ilike(like),
                Disease.symptoms.ilike(like),
            )
        )
    rows = query.order_by(Disease.crop_type.asc(), Disease.name.asc()).all()
    return render_template("disease_library.html", diseases=rows, search=search)


@main_bp.get("/diseases/<int:disease_id>")
def disease_detail(disease_id: int):
    disease = Disease.query.get_or_404(disease_id)
    return render_template("disease_detail.html", disease=disease)


@main_bp.get("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(current_app.config["UPLOAD_DIR"], filename)


@main_bp.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "python-crop-disease-detector"})


@main_bp.post("/api/predict")
def api_predict():
    image = request.files.get("leaf_image")
    crop_hint = request.form.get("crop_type", "").strip() or None
    if crop_hint == "auto":
        crop_hint = None

    if not image or not image.filename:
        return jsonify({"error": "leaf_image is required"}), 400
    if not allowed_file(image.filename):
        return jsonify({"error": "Unsupported file format"}), 400

    filename, image_path = save_uploaded_file(image, current_app.config["UPLOAD_DIR"])
    prediction_payload = _prediction_engine().predict(image_path=image_path, crop_hint=crop_hint)

    prediction = Prediction(
        crop_type=prediction_payload["crop_type"],
        disease_name=prediction_payload["disease_name"],
        confidence=prediction_payload["confidence"],
        severity=prediction_payload["severity"],
        treatment=prediction_payload["treatment"],
        is_healthy=prediction_payload["is_healthy"],
        image_path=filename,
        top_candidates=json.dumps(prediction_payload.get("top_candidates", [])),
    )
    db.session.add(prediction)
    db.session.commit()

    return jsonify(prediction.to_dict()), 201
