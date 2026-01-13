import os
import urllib.request
from pathlib import Path
from toolbox.core.config import config_manager
from toolbox.core.engine import console

AI_MODELS_DIR = Path(config_manager.settings.global_bin_path or "bin") / "ai_models"

def get_model_path(model_name: str, url: str) -> Path:
    """Ensure an AI model is downloaded and return its path."""
    AI_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = AI_MODELS_DIR / model_name
    
    if not model_path.exists():
        console.print(f"[bold blue]Downloading AI model: {model_name}...[/bold blue]")
        try:
            urllib.request.urlretrieve(url, model_path)
            console.print(f"[green]✓ Model downloaded to {model_path}[/green]")
        except Exception as e:
            console.print(f"[bold red]Error downloading model:[/bold red] {e}")
            raise
            
    return model_path

def is_gpu_available() -> bool:
    """Check if a GPU is available for acceleration."""
    # Check for ONNX Runtime GPU
    try:
        import onnxruntime as ort
        return "CUDAExecutionProvider" in ort.get_available_providers() or "ROCMExecutionProvider" in ort.get_available_providers()
    except ImportError:
        pass
        
    # Check for OpenCV GPU support
    try:
        import cv2
        return cv2.cuda.getCudaEnabledDeviceCount() > 0
    except (ImportError, AttributeError):
        pass
        
    return False
