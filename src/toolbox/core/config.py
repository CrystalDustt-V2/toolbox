import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class ToolBoxConfig(BaseModel):
    default_output: str = Field(default="./output")
    language: str = Field(default="en")
    ocr_engine: str = Field(default="tesseract")
    video_engine: str = Field(default="ffmpeg")
    image_engine: str = Field(default="imagemagick")
    auto_overwrite: bool = Field(default=False)
    plugins_dir: Optional[str] = Field(default=None)
    global_bin_path: Optional[str] = Field(default=None)
    engine_paths: Dict[str, str] = Field(default_factory=dict)

class ConfigManager:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".toolbox" / "config.yaml"
        self.settings = self._load_config()

    def _load_config(self) -> ToolBoxConfig:
        if not self.config_path.exists():
            return ToolBoxConfig()
        
        try:
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f) or {}
                return ToolBoxConfig(**data)
        except Exception:
            # Fallback to defaults if config is corrupted
            return ToolBoxConfig()

    def save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(self.settings.model_dump(), f)

    def update(self, **kwargs):
        new_settings = self.settings.model_dump()
        new_settings.update({k: v for k, v in kwargs.items() if v is not None})
        self.settings = ToolBoxConfig(**new_settings)

config_manager = ConfigManager()
