import re
from pathlib import Path
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

CROP_ALIASES = {
    "corn (maize)": "maize",
    "corn": "maize",
    "maize": "maize",
    "cassava": "cassava",
    "rice": "rice",
    "tomato": "tomato",
    "potato": "potato",
    "pepper": "pepper",
    "pepper bell": "pepper",
    "bell pepper": "pepper",
    "apple": "apple",
    "grape": "grape",
    "wheat": "wheat",
    "sugarcane": "sugarcane",
    "tomato leaf": "tomato",
    "potato leaf": "potato",
    "pepper leaf": "pepper",
}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file_storage: FileStorage, upload_dir: Path) -> tuple[str, Path]:
    upload_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(secure_filename(file_storage.filename or "")).suffix.lower() or ".jpg"
    filename = f"{uuid4().hex}{suffix}"
    abs_path = upload_dir / filename
    file_storage.save(abs_path)
    return filename, abs_path


def _clean_fragment(raw: str) -> str:
    cleaned = raw.replace("_", " ").replace("-", " ").strip().lower()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def _titleize(raw: str) -> str:
    words = _clean_fragment(raw).split(" ")
    return " ".join(word.capitalize() for word in words if word)


def normalize_crop_name(raw: str | None) -> str:
    if not raw:
        return "unknown"
    cleaned = _clean_fragment(raw)
    return CROP_ALIASES.get(cleaned, cleaned if cleaned else "unknown")


def normalize_disease_name(raw: str, crop: str | None = None) -> str:
    cleaned = _clean_fragment(raw)
    compressed = cleaned.replace(" ", "")

    if "healthy" in compressed:
        return "Healthy"

    if crop == "rice":
        if "bacterialblight" in compressed:
            return "Rice Bacterial Blight"
        if compressed == "blast":
            return "Rice Blast"
        if "brownspot" in compressed:
            return "Rice Brown Spot"
        if "tungro" in compressed:
            return "Rice Tungro"

    if crop == "cassava":
        if "bacterial" in compressed and "blight" in compressed:
            return "Cassava Bacterial Blight"
        if "brown" in compressed and "streak" in compressed:
            return "Cassava Brown Streak Disease"
        if "green" in compressed and "mottle" in compressed:
            return "Cassava Green Mottle"
        if "mosaic" in compressed:
            return "Cassava Mosaic Disease"

    known_shortcuts = {
        "earlyblight": "Early Blight",
        "lateblight": "Late Blight",
        "leafmold": "Leaf Mold",
        "septorialeafspot": "Septoria Leaf Spot",
        "targetspot": "Target Spot",
        "tomatoyellowleafcurlvirus": "Tomato Yellow Leaf Curl Virus",
        "yellowleafcurlvirus": "Tomato Yellow Leaf Curl Virus",
        "tomatomosaicvirus": "Tomato Mosaic Virus",
        "mosaicvirus": "Tomato Mosaic Virus",
        "spidermitestwospottedspidermite": "Spider Mites Two-spotted Spider Mite",
        "powderymildew": "Powdery Mildew",
        "commonrust": "Common Rust",
        "northernleafblight": "Northern Leaf Blight",
        "grayleafspot": "Gray Leaf Spot",
        "bacterialspot": "Bacterial Spot",
    }
    if compressed in known_shortcuts:
        base_name = known_shortcuts[compressed]
    else:
        base_name = _titleize(cleaned)

    if crop and crop not in {"unknown"} and not base_name.lower().startswith(crop):
        return f"{crop.capitalize()} {base_name}"
    return base_name


def parse_general_label(label: str) -> tuple[str, str, bool]:
    normalized = label.strip().replace("__", "___")
    if "___" in normalized:
        crop_raw, disease_raw = normalized.split("___", 1)
    else:
        crop_raw, disease_raw = "unknown", normalized

    crop = normalize_crop_name(crop_raw)
    disease = normalize_disease_name(disease_raw, crop=crop)
    is_healthy = disease.lower() == "healthy"
    if is_healthy:
        disease = "Healthy"
    return crop, disease, is_healthy


def parse_specialized_label(label: str, fixed_crop: str) -> tuple[str, str, bool]:
    crop = normalize_crop_name(fixed_crop)
    disease = normalize_disease_name(label, crop=crop)
    is_healthy = disease.lower() == "healthy"
    if is_healthy:
        disease = "Healthy"
    return crop, disease, is_healthy


def parse_flexible_label(label: str) -> tuple[str, str, bool]:
    if "___" in label or "__" in label:
        return parse_general_label(label)

    cleaned = _clean_fragment(label)

    explicit_prefixes = (
        "tomato leaf ",
        "tomato ",
        "potato leaf ",
        "potato ",
        "rice leaf ",
        "rice ",
        "cassava leaf ",
        "cassava ",
        "maize leaf ",
        "maize ",
        "corn leaf ",
        "corn ",
        "pepper leaf ",
        "pepper ",
    )
    for prefix in explicit_prefixes:
        if cleaned.startswith(prefix):
            crop = normalize_crop_name(prefix.strip())
            disease = normalize_disease_name(cleaned[len(prefix) :], crop=crop)
            is_healthy = disease.lower() == "healthy"
            if is_healthy:
                disease = "Healthy"
            return crop, disease, is_healthy

    if " leaf " in cleaned:
        crop_fragment, disease_fragment = cleaned.split(" leaf ", 1)
        crop = normalize_crop_name(crop_fragment)
        disease = normalize_disease_name(disease_fragment, crop=crop)
        is_healthy = disease.lower() == "healthy"
        if is_healthy:
            disease = "Healthy"
        return crop, disease, is_healthy

    return parse_general_label(label)
