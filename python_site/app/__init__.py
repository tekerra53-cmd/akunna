from flask import Flask

from .config import Settings
from .database import db
from .inference import PredictionEngine
from .routes import main_bp
from .seed_data import seed_diseases


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Settings)

    for path in (
        app.config["INSTANCE_DIR"],
        app.config["UPLOAD_DIR"],
        app.config["MODEL_DIR"],
        app.config["DATASET_DIR"],
    ):
        path.mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    with app.app_context():
        from . import models  # noqa: F401

        db.create_all()
        seed_diseases(db.session)
        db.session.commit()

    app.register_blueprint(main_bp)
    app.extensions["prediction_engine"] = PredictionEngine(app.config)
    return app
