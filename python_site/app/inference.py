from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from PIL import Image

from .seed_data import build_disease_lookup
from .utils import normalize_crop_name, parse_general_label, parse_specialized_label

LOGGER = logging.getLogger(__name__)


@dataclass
class CandidatePrediction:
    crop_type: str
    disease_name: str
    confidence: float
    is_healthy: bool
    source: str
    weight: float


class HFModelBackend:
    def __init__(
        self,
        repo_id: str,
        source_name: str,
        fixed_crop: str | None = None,
        weight: float = 1.0,
        hf_token: str | None = None,
    ) -> None:
        self.repo_id = repo_id
        self.source_name = source_name
        self.fixed_crop = fixed_crop
        self.weight = weight
        self.hf_token = hf_token

        self._processor = None
        self._model = None
        self._loaded = False
        self._load_error: str | None = None

    def supports_crop(self, crop_hint: str | None) -> bool:
        if not crop_hint or crop_hint == "unknown":
            return True
        if not self.fixed_crop:
            return True
        return normalize_crop_name(self.fixed_crop) == crop_hint

    def _ensure_loaded(self) -> None:
        if self._loaded or self._load_error:
            return

        try:
            from transformers import AutoImageProcessor, AutoModelForImageClassification

            self._processor = AutoImageProcessor.from_pretrained(self.repo_id, token=self.hf_token)
            self._model = AutoModelForImageClassification.from_pretrained(self.repo_id, token=self.hf_token)
            self._model.eval()
            self._loaded = True
        except Exception as exc:  # pragma: no cover
            self._load_error = str(exc)
            LOGGER.warning("Could not load model %s: %s", self.repo_id, exc)

    def predict(self, image: Image.Image, top_k: int) -> list[CandidatePrediction]:
        self._ensure_loaded()
        if not self._loaded:
            return []

        try:
            inputs = self._processor(images=image, return_tensors="pt")
            with torch.no_grad():
                logits = self._model(**inputs).logits
                probs = torch.softmax(logits, dim=-1)[0]

            max_k = min(max(top_k, 1), probs.shape[0])
            top_probs, top_ids = torch.topk(probs, k=max_k)
            id2label = getattr(self._model.config, "id2label", {}) or {}

            candidates: list[CandidatePrediction] = []
            for prob, class_idx in zip(top_probs.tolist(), top_ids.tolist()):
                label = id2label.get(class_idx) or id2label.get(str(class_idx)) or str(class_idx)
                if self.fixed_crop:
                    crop, disease, healthy = parse_specialized_label(label, self.fixed_crop)
                else:
                    crop, disease, healthy = parse_general_label(label)
                candidates.append(
                    CandidatePrediction(
                        crop_type=crop,
                        disease_name=disease,
                        confidence=float(prob),
                        is_healthy=healthy,
                        source=self.source_name,
                        weight=self.weight,
                    )
                )
            return candidates
        except Exception as exc:  # pragma: no cover
            LOGGER.warning("Inference failed for model %s: %s", self.repo_id, exc)
            return []


class LocalCheckpointBackend:
    def __init__(self, checkpoint_path: Path, source_name: str = "local-finetuned", weight: float = 1.15) -> None:
        self.checkpoint_path = checkpoint_path
        self.source_name = source_name
        self.weight = weight

        self._model = None
        self._transform = None
        self._labels: list[str] = []
        self._loaded = False
        self._load_error: str | None = None

    def supports_crop(self, crop_hint: str | None) -> bool:
        return True

    def _build_model(self, architecture: str, num_classes: int):
        from torchvision import models

        if architecture == "resnet18":
            model = models.resnet18(weights=None)
            model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
            return model

        model = models.efficientnet_b0(weights=None)
        model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)
        return model

    def _ensure_loaded(self) -> None:
        if self._loaded or self._load_error:
            return

        if not self.checkpoint_path.exists():
            self._load_error = "checkpoint_missing"
            return

        try:
            from torchvision import transforms

            checkpoint = torch.load(self.checkpoint_path, map_location="cpu")
            labels = checkpoint.get("labels")
            if not labels and "idx_to_class" in checkpoint:
                idx_to_class = checkpoint["idx_to_class"]
                labels = [idx_to_class[str(i)] if str(i) in idx_to_class else idx_to_class[i] for i in range(len(idx_to_class))]

            if not labels:
                raise RuntimeError("No labels found in local checkpoint.")

            architecture = checkpoint.get("architecture", "efficientnet_b0")
            model = self._build_model(architecture, len(labels))
            model.load_state_dict(checkpoint["state_dict"])
            model.eval()

            self._labels = labels
            self._model = model
            self._transform = transforms.Compose(
                [
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                ]
            )
            self._loaded = True
        except Exception as exc:  # pragma: no cover
            self._load_error = str(exc)
            LOGGER.warning("Could not load local model checkpoint: %s", exc)

    def predict(self, image: Image.Image, top_k: int) -> list[CandidatePrediction]:
        self._ensure_loaded()
        if not self._loaded:
            return []

        tensor = self._transform(image).unsqueeze(0)
        with torch.no_grad():
            logits = self._model(tensor)
            probs = torch.softmax(logits, dim=-1)[0]

        max_k = min(max(top_k, 1), probs.shape[0])
        top_probs, top_ids = torch.topk(probs, k=max_k)
        predictions: list[CandidatePrediction] = []

        for prob, class_idx in zip(top_probs.tolist(), top_ids.tolist()):
            label = self._labels[class_idx]
            crop, disease, healthy = parse_general_label(label)
            predictions.append(
                CandidatePrediction(
                    crop_type=crop,
                    disease_name=disease,
                    confidence=float(prob),
                    is_healthy=healthy,
                    source=self.source_name,
                    weight=self.weight,
                )
            )
        return predictions


class PredictionEngine:
    def __init__(self, config: dict[str, Any]) -> None:
        self.top_k = int(config.get("TOP_K", 3))
        self.unknown_threshold = float(config.get("UNKNOWN_THRESHOLD", 0.25))
        self.hinted_top_k = int(config.get("HINTED_TOP_K", 12))
        self.hinted_unknown_threshold = float(config.get("HINTED_UNKNOWN_THRESHOLD", 0.10))
        self.disease_lookup = build_disease_lookup()

        local_model_path = Path(config.get("LOCAL_MODEL_PATH"))
        hf_token = config.get("HF_TOKEN")

        self.backends = [
            LocalCheckpointBackend(local_model_path),
            HFModelBackend(
                repo_id=config.get("PRIMARY_MODEL_ID"),
                source_name="global-multicrop",
                fixed_crop=None,
                weight=1.0,
                hf_token=hf_token,
            ),
            HFModelBackend(
                repo_id=config.get("CASSAVA_MODEL_ID"),
                source_name="cassava-specialist",
                fixed_crop="cassava",
                weight=1.05,
                hf_token=hf_token,
            ),
            HFModelBackend(
                repo_id=config.get("RICE_MODEL_ID"),
                source_name="rice-specialist",
                fixed_crop="rice",
                weight=1.05,
                hf_token=hf_token,
            ),
        ]

    def _build_unknown_response(self, crop_hint: str | None, top_candidates: list[dict]) -> dict:
        fallback_confidence = 0.0
        if top_candidates:
            fallback_confidence = float(top_candidates[0].get("confidence", 0.0) or 0.0)
        return {
            "crop_type": crop_hint or "unknown",
            "disease_name": "Unknown - Needs more data",
            "confidence": fallback_confidence,
            "is_healthy": False,
            "severity": "medium",
            "treatment": (
                "The model found only a low-confidence match. Capture a clearer close-up of a single leaf, "
                "use the correct crop hint, or improve training data for this crop/disease class."
            ),
            "top_candidates": top_candidates,
        }

    def _resolve_guidance(self, crop: str, disease: str, is_healthy: bool, confidence: float) -> tuple[str, str]:
        if is_healthy:
            return "low", "Plant appears healthy. Continue routine monitoring and balanced nutrient management."

        match = self.disease_lookup.get((crop, disease.lower()))
        if match:
            return match["severity"], match["treatment"]

        if confidence >= 0.80:
            severity = "high"
        elif confidence >= 0.60:
            severity = "medium"
        else:
            severity = "low"

        return severity, "Isolate affected plants, monitor disease progression, and consult a local agronomist for targeted treatment."

    def predict(self, image_path: Path, crop_hint: str | None = None) -> dict:
        image = Image.open(image_path).convert("RGB")
        normalized_hint = normalize_crop_name(crop_hint) if crop_hint else None
        backend_top_k = self.top_k
        if normalized_hint and normalized_hint != "unknown":
            backend_top_k = max(self.top_k, self.hinted_top_k)

        candidates: list[CandidatePrediction] = []
        for backend in self.backends:
            if not backend.supports_crop(normalized_hint):
                continue
            candidates.extend(backend.predict(image, backend_top_k))

        if not candidates:
            return self._build_unknown_response(crop_hint, top_candidates=[])

        all_ranked_preview: list[dict[str, Any]] = []
        grouped_all: dict[tuple[str, str, bool], dict[str, Any]] = {}
        for cand in candidates:
            key = (cand.crop_type, cand.disease_name, cand.is_healthy)
            bucket = grouped_all.setdefault(
                key,
                {
                    "weighted_sum": 0.0,
                    "total_weight": 0.0,
                    "sources": set(),
                },
            )
            bucket["weighted_sum"] += cand.confidence * cand.weight
            bucket["total_weight"] += cand.weight
            bucket["sources"].add(cand.source)

        for (crop, disease, healthy), stats in grouped_all.items():
            confidence = stats["weighted_sum"] / max(stats["total_weight"], 1e-8)
            all_ranked_preview.append(
                {
                    "cropType": crop,
                    "diseaseName": disease,
                    "confidence": round(float(confidence), 4),
                    "sources": sorted(stats["sources"]),
                    "isHealthy": healthy,
                }
            )
        all_ranked_preview.sort(key=lambda item: item["confidence"], reverse=True)

        if normalized_hint and normalized_hint != "unknown":
            hinted = [c for c in candidates if c.crop_type == normalized_hint]
            if hinted:
                candidates = hinted
            else:
                return self._build_unknown_response(
                    crop_hint=normalized_hint,
                    top_candidates=all_ranked_preview[: max(self.top_k, 3)],
                )

        grouped: dict[tuple[str, str, bool], dict[str, Any]] = {}
        for cand in candidates:
            key = (cand.crop_type, cand.disease_name, cand.is_healthy)
            bucket = grouped.setdefault(
                key,
                {
                    "weighted_sum": 0.0,
                    "total_weight": 0.0,
                    "sources": set(),
                },
            )
            bucket["weighted_sum"] += cand.confidence * cand.weight
            bucket["total_weight"] += cand.weight
            bucket["sources"].add(cand.source)

        ranked = []
        for (crop, disease, healthy), stats in grouped.items():
            confidence = stats["weighted_sum"] / max(stats["total_weight"], 1e-8)
            ranked.append(
                {
                    "crop_type": crop,
                    "disease_name": disease,
                    "is_healthy": healthy,
                    "confidence": float(confidence),
                    "sources": sorted(stats["sources"]),
                }
            )

        ranked.sort(key=lambda item: item["confidence"], reverse=True)
        top_candidates = ranked[: max(self.top_k, 3)]
        best = top_candidates[0]

        top_preview = [
            {
                "cropType": item["crop_type"],
                "diseaseName": item["disease_name"],
                "confidence": round(item["confidence"], 4),
                "sources": item["sources"],
            }
            for item in top_candidates
        ]

        effective_unknown_threshold = self.unknown_threshold
        if normalized_hint and normalized_hint != "unknown":
            effective_unknown_threshold = self.hinted_unknown_threshold

        if best["confidence"] < effective_unknown_threshold:
            return self._build_unknown_response(crop_hint, top_candidates=top_preview)

        severity, treatment = self._resolve_guidance(
            crop=best["crop_type"],
            disease=best["disease_name"],
            is_healthy=best["is_healthy"],
            confidence=best["confidence"],
        )

        return {
            "crop_type": best["crop_type"],
            "disease_name": best["disease_name"],
            "confidence": float(best["confidence"]),
            "is_healthy": bool(best["is_healthy"]),
            "severity": severity,
            "treatment": treatment,
            "top_candidates": top_preview,
        }
