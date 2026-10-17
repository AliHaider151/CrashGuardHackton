from __future__ import annotations

from pathlib import Path

from ultralytics import YOLO

from app.config import get_config

_model: YOLO | None = None


def load_model(model_path: str | None = None) -> YOLO:
    global _model

    config = get_config()
    target = model_path or config.model_path
    candidate = Path(target)
    if not candidate.is_absolute():
        candidate = config.resolve_path(target)

    if not candidate.exists():
        raise FileNotFoundError(f"Model file not found: {candidate}")

    _model = YOLO(str(candidate))
    return _model


def get_model() -> YOLO:
    global _model
    if _model is None:
        _model = load_model()
    return _model
