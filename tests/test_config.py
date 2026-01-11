import os
from pathlib import Path
from toolbox.core.config import ConfigManager, ToolBoxConfig

def test_config_default_values():
    config = ConfigManager(config_path=Path("nonexistent.yaml"))
    assert config.settings.default_output == "./output"
    assert config.settings.language == "en"

def test_config_update():
    config = ConfigManager(config_path=Path("nonexistent.yaml"))
    config.update(default_output="./new_output", language="fr")
    assert config.settings.default_output == "./new_output"
    assert config.settings.language == "fr"

def test_engine_paths_config():
    config = ConfigManager(config_path=Path("nonexistent.yaml"))
    config.update(engine_paths={"ffmpeg": "/usr/bin/ffmpeg"})
    assert config.settings.engine_paths["ffmpeg"] == "/usr/bin/ffmpeg"
