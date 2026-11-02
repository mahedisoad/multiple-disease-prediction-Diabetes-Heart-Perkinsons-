"""
Model loading service — loads trusted .sav model files once at startup.

SECURITY NOTE: Only loads models from the controlled project directory.
Pickle files can execute arbitrary code — never load untrusted artifacts.
"""
import pickle
from pathlib import Path
from typing import Any

from app.core.logging_config import logger


class ModelLoadError(Exception):
    """Raised when a model file cannot be loaded."""
    pass


class ModelStore:
    """Singleton-style store that holds all loaded ML models."""

    def __init__(self) -> None:
        self._models: dict[str, Any] = {}
        self._loaded: bool = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def load_all(self, model_dir: str) -> None:
        """Load all expected model files from the given directory.

        Expected files (derived from the original training notebooks):
          - diabetes_model.sav       → SVC(kernel='linear')
          - heart_disease_model.sav  → LogisticRegression()
          - parkinsons_model.sav     → SVC(kernel='linear')
        """
        model_dir_path = Path(model_dir)

        if not model_dir_path.exists():
            raise ModelLoadError(
                f"Model directory does not exist: {model_dir_path}"
            )

        expected_models = {
            "diabetes": "diabetes_model.sav",
            "heart": "heart_disease_model.sav",
            "parkinsons": "parkinsons_model.sav",
        }

        for key, filename in expected_models.items():
            filepath = model_dir_path / filename
            if not filepath.exists():
                logger.warning("Model file not found: %s — %s predictions will be unavailable", filepath, key)
                continue

            try:
                with open(filepath, "rb") as f:
                    model = pickle.load(f)
                self._models[key] = model
                logger.info("Loaded model: %s from %s", key, filepath.name)
            except Exception as e:
                logger.error("Failed to load model %s: %s", key, str(e))
                raise ModelLoadError(f"Failed to load {key} model: {e}") from e

        self._loaded = True
        logger.info(
            "Model loading complete — %d/%d models available: %s",
            len(self._models),
            len(expected_models),
            list(self._models.keys()),
        )

    def get_model(self, disease_key: str) -> Any:
        """Retrieve a loaded model by disease key.

        Args:
            disease_key: One of 'diabetes', 'heart', 'parkinsons'

        Returns:
            The sklearn model object.

        Raises:
            ModelLoadError: If the model is not available.
        """
        if disease_key not in self._models:
            raise ModelLoadError(
                f"Model '{disease_key}' is not loaded. "
                "The model file may be missing from the models directory."
            )
        return self._models[disease_key]

    def available_diseases(self) -> list[str]:
        """Return list of disease keys for which models are loaded."""
        return list(self._models.keys())


# Module-level singleton
model_store = ModelStore()
