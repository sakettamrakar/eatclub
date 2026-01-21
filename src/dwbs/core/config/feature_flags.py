import json
import os
from pydantic import BaseModel, ValidationError

class FeatureFlags(BaseModel):
    PASSIVE_INGEST: bool = False
    SMART_DEPLETION: bool = False
    VOICE: bool = False
    FAMILY: bool = False

class FeatureFlagManager:
    def __init__(self, config_path: str = "features.json"):
        self._config_path = config_path
        self._flags = FeatureFlags()
        self._load_flags()

    def _load_flags(self) -> None:
        if not os.path.exists(self._config_path):
            # No config file -> Defaults (False)
            self._flags = FeatureFlags()
            return

        try:
            with open(self._config_path, 'r') as f:
                data = json.load(f)
                self._flags = FeatureFlags(**data)
        except (json.JSONDecodeError, ValidationError, OSError):
            # Corrupt config -> Default to False (Safe)
            self._flags = FeatureFlags()

    @property
    def flags(self) -> FeatureFlags:
        return self._flags

    def reload(self) -> None:
        """Reloads the flags from the persistent store."""
        self._load_flags()
