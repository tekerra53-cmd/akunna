from __future__ import annotations

import argparse
import math
import sys
from collections import defaultdict
from pathlib import Path

from datasets import load_dataset
from PIL import Image
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.utils import (
    normalize_crop_name,
    normalize_disease_name,
    parse_flexible_label,
    parse_general_label,
)

DEFAULT_HF_SOURCES = (
    {
        "name": "plantvillage",
        "repo_id": "mohanty/PlantVillage",
        "config": "color",
    },
    {
        "name": "plantdoc-realworld",
        "repo_id": "avinashhm/plant-disease-classification-complete",
        "only_crops": {"tomato"},
    },
)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def slugify_label(raw: str) -> str:
    return raw.strip().replace(" ", "_").replace("/", "_")


def ensure_rgb(image: Image.Image) -> Image.Image:
    return image if image.mode == "RGB" else image.convert("RGB")


def resolve_target_split(split_name: str) -> str:
    normalized = split_name.strip().lower()
    if normalized in {"train", "training"}:
        return "train"
    if normalized in {"validation", "valid", "val", "dev"}:
        return "val"
    if normalized in {"test", "testing"}:
        return "test"
    return "train"


def infer_label_from_row(row: dict, dataset_split) -> tuple[str, str, bool] | None:
    if "crop" in row and "disease" in row:
        crop = normalize_crop_name(str(row["crop"]))
        disease = normalize_disease_name(str(row["disease"]), crop=crop)
        is_healthy = disease.lower() == "healthy"
        return crop, ("Healthy" if is_healthy else disease), is_healthy

    if "label" in row:
        label_feature = dataset_split.features.get("label")
        if hasattr(label_feature, "int2str"):
            class_name = label_feature.int2str(int(row["label"]))
        else:
            class_name = str(row["label"])
        return parse_flexible_label(class_name)

    for key in ("class", "disease", "category", "name"):
        value = row.get(key)
        if value:
            return parse_flexible_label(str(value))

    path_value = row.get("image_file_path") or row.get("path") or row.get("file_name") or row.get("filename")
    if path_value:
        parent_name = Path(str(path_value)).parent.name
        if parent_name:
            return parse_flexible_label(parent_name)

    return None


def save_image_to_class_dir(
    image: Image.Image,
    split_name: str,
    output_dir: Path,
    class_key: str,
    counters: dict[str, int],
    max_per_class: int,
) -> bool:
    if max_per_class > 0 and counters[class_key] >= max_per_class:
        return False

    class_dir = output_dir / split_name / slugify_label(class_key)
    class_dir.mkdir(parents=True, exist_ok=True)
    file_path = class_dir / f"{counters[class_key]:06d}.jpg"
    ensure_rgb(image).save(file_path, format="JPEG", quality=95)
    counters[class_key] += 1
    return True


def export_hf_source(source: dict, output_dir: Path, max_per_class: int = 0) -> dict[str, dict[str, int]]:
    load_kwargs = {}
    if source.get("config"):
        load_kwargs["name"] = source["config"]

    dataset = load_dataset(source["repo_id"], **load_kwargs)
    split_counters: dict[str, defaultdict[str, int]] = {
        "train": defaultdict(int),
        "val": defaultdict(int),
        "test": defaultdict(int),
    }

    only_crops = {normalize_crop_name(crop) for crop in source.get("only_crops", set())}

    for hf_split_name, dataset_split in dataset.items():
        default_split = resolve_target_split(hf_split_name)
        for row in tqdm(dataset_split, desc=f"{source['name']}:{hf_split_name}", unit="img"):
            parsed = infer_label_from_row(row, dataset_split)
            image = row.get("image")
            if not parsed or image is None:
                continue

            crop, disease, _ = parsed
            if only_crops and crop not in only_crops:
                continue

            class_key = f"{crop}___{disease}"
            row_split = row.get("split")
            target_split = resolve_target_split(str(row_split)) if row_split else default_split
            save_image_to_class_dir(
                image=image,
                split_name=target_split,
                output_dir=output_dir,
                class_key=class_key,
                counters=split_counters[target_split],
                max_per_class=max_per_class,
            )

    return {split_name: dict(counter) for split_name, counter in split_counters.items()}


def export_local_imagefolder(local_dir: Path, output_dir: Path, max_per_class: int = 0) -> dict[str, dict[str, int]]:
    split_counters: dict[str, defaultdict[str, int]] = {
        "train": defaultdict(int),
        "val": defaultdict(int),
        "test": defaultdict(int),
    }

    candidate_splits = [child for child in local_dir.iterdir() if child.is_dir()]
    has_named_splits = any(resolve_target_split(child.name) != "train" or child.name.lower() == "train" for child in candidate_splits)

    split_dirs = candidate_splits if has_named_splits else [local_dir]

    for split_dir in split_dirs:
        auto_split_unsplit_root = split_dir == local_dir and not has_named_splits
        split_name = resolve_target_split(split_dir.name if split_dir != local_dir else "train")
        for class_dir in sorted(path for path in split_dir.iterdir() if path.is_dir()):
            crop, disease, _ = parse_flexible_label(class_dir.name)
            class_key = f"{crop}___{disease}"
            images = sorted(path for path in class_dir.rglob("*") if path.suffix.lower() in IMAGE_EXTENSIONS)
            total_images = len(images)
            train_cutoff = math.floor(total_images * 0.8)
            val_cutoff = math.floor(total_images * 0.9)

            for index, image_path in enumerate(
                tqdm(images, desc=f"local:{split_dir.name}:{class_dir.name}", unit="img")
            ):
                target_split = split_name
                if auto_split_unsplit_root:
                    if index < train_cutoff:
                        target_split = "train"
                    elif index < val_cutoff:
                        target_split = "val"
                    else:
                        target_split = "test"

                with Image.open(image_path) as image:
                    save_image_to_class_dir(
                        image=image,
                        split_name=target_split,
                        output_dir=output_dir,
                        class_key=class_key,
                        counters=split_counters[target_split],
                        max_per_class=max_per_class,
                    )

    return {split_name: dict(counter) for split_name, counter in split_counters.items()}


def print_summary(title: str, counts: dict[str, dict[str, int]]) -> None:
    print(f"\n{title}")
    for split_name in ("train", "val", "test"):
        split_counts = counts.get(split_name, {})
        total_images = sum(split_counts.values())
        print(f"  {split_name}: {len(split_counts)} classes, {total_images} images")


def main():
    parser = argparse.ArgumentParser(description="Build a crop disease dataset for local training.")
    parser.add_argument("--output", type=Path, default=Path("dataset/combined"), help="Output dataset directory.")
    parser.add_argument(
        "--max-per-class",
        type=int,
        default=0,
        help="Optional cap per class per split (0 means no cap). Useful for quick experiments.",
    )
    parser.add_argument(
        "--skip-default-sources",
        action="store_true",
        help="Do not download the built-in Hugging Face sources.",
    )
    parser.add_argument(
        "--local-image-folder",
        action="append",
        default=[],
        help=(
            "Optional local dataset folder to merge. Accepts ImageFolder layout like "
            "'train/Tomato___Late_Blight/*.jpg' or a single class-folder root. "
            "Single-root datasets are auto-split into train/val/test using an 80/10/10 ratio."
        ),
    )
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)

    if not args.skip_default_sources:
        print("Downloading default sources: PlantVillage + extra real-world tomato images...")
        for source in DEFAULT_HF_SOURCES:
            counts = export_hf_source(source, output_dir=args.output, max_per_class=args.max_per_class)
            print_summary(f"Source: {source['name']}", counts)

    for local_folder in args.local_image_folder:
        local_path = Path(local_folder)
        if not local_path.exists():
            raise FileNotFoundError(f"Local dataset folder not found: {local_path}")
        counts = export_local_imagefolder(local_path, output_dir=args.output, max_per_class=args.max_per_class)
        print_summary(f"Local source: {local_path}", counts)

    train_dir = args.output / "train"
    val_dir = args.output / "val"
    test_dir = args.output / "test"

    print("\nDataset export complete.")
    print(f"Train folder: {train_dir.resolve()}")
    print(f"Validation folder: {val_dir.resolve()}")
    print(f"Test folder: {test_dir.resolve()}")
    print(
        "\nClass folder format stays the same: crop___Disease Name\n"
        "Examples: tomato___Late Blight, tomato___Tomato Yellow Leaf Curl Virus, tomato___Healthy"
    )


if __name__ == "__main__":
    main()
