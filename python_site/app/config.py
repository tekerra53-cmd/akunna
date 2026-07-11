import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


class Settings:
    BASE_DIR = PROJECT_DIR
    INSTANCE_DIR = PROJECT_DIR / "instance"
    UPLOAD_DIR = PROJECT_DIR / "uploads"
    MODEL_DIR = PROJECT_DIR / "models"
    DATASET_DIR = PROJECT_DIR / "dataset"

    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-secret")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR / 'crop_disease.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    TOP_K = int(os.getenv("TOP_K", "3"))
    UNKNOWN_THRESHOLD = float(os.getenv("UNKNOWN_THRESHOLD", "0.25"))

    LOCAL_MODEL_PATH = Path(os.getenv("LOCAL_MODEL_PATH", str(MODEL_DIR / "local_classifier.pt")))

    PRIMARY_MODEL_ID = os.getenv("PRIMARY_MODEL_ID", "mesabo/agri-plant-disease-resnet50")
    CASSAVA_MODEL_ID = os.getenv("CASSAVA_MODEL_ID", "nexusbert/resnet50-cassava-finetuned")
    RICE_MODEL_ID = os.getenv("RICE_MODEL_ID", "prithivMLmods/Rice-Leaf-Disease")
    HF_TOKEN = os.getenv("HF_TOKEN")
