import pytest
from toolbox.core.engine import EngineRegistry, BaseEngine, EngineError

def test_engine_registry_get():
    registry = EngineRegistry()
    ffmpeg = registry.get("ffmpeg")
    assert isinstance(ffmpeg, BaseEngine)
    assert ffmpeg.name == "FFmpeg"

def test_engine_registry_invalid():
    registry = EngineRegistry()
    with pytest.raises(EngineError):
        registry.get("nonexistent")

def test_base_engine_availability():
    # This might depend on the environment, but we can mock it
    engine = BaseEngine("Test", "nonexistent_binary")
    assert engine.is_available is False
