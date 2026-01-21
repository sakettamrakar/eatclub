import pytest
import json
import os
from src.dwbs.core.config.feature_flags import FeatureFlagManager

def test_defaults_are_false(tmp_path):
    # Point to a non-existent file
    config_path = tmp_path / "non_existent.json"
    manager = FeatureFlagManager(config_path=str(config_path))

    assert manager.flags.PASSIVE_INGEST is False
    assert manager.flags.SMART_DEPLETION is False
    assert manager.flags.VOICE is False
    assert manager.flags.FAMILY is False

def test_load_valid_config(tmp_path):
    config_path = tmp_path / "features.json"
    data = {
        "PASSIVE_INGEST": True,
        "SMART_DEPLETION": True,
        "VOICE": False,
        "FAMILY": False
    }
    config_path.write_text(json.dumps(data))

    manager = FeatureFlagManager(config_path=str(config_path))

    assert manager.flags.PASSIVE_INGEST is True
    assert manager.flags.SMART_DEPLETION is True
    assert manager.flags.VOICE is False
    assert manager.flags.FAMILY is False

def test_corrupt_json_defaults_to_false(tmp_path):
    config_path = tmp_path / "corrupt.json"
    config_path.write_text("{ this is not json }")

    manager = FeatureFlagManager(config_path=str(config_path))

    # Should default to False safely
    assert manager.flags.PASSIVE_INGEST is False
    assert manager.flags.SMART_DEPLETION is False

def test_invalid_types_trigger_default(tmp_path):
    # Pydantic validation error should trigger fallback to defaults
    config_path = tmp_path / "bad_types.json"
    data = {
        "PASSIVE_INGEST": "not a boolean"
    }
    config_path.write_text(json.dumps(data))

    manager = FeatureFlagManager(config_path=str(config_path))

    # Should revert to default (False) because of ValidationError
    assert manager.flags.PASSIVE_INGEST is False

def test_reload(tmp_path):
    config_path = tmp_path / "reload.json"
    data = {"PASSIVE_INGEST": False}
    config_path.write_text(json.dumps(data))

    manager = FeatureFlagManager(config_path=str(config_path))
    assert manager.flags.PASSIVE_INGEST is False

    # Update file
    data["PASSIVE_INGEST"] = True
    config_path.write_text(json.dumps(data))

    manager.reload()
    assert manager.flags.PASSIVE_INGEST is True
