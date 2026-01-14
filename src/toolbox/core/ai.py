import os
import urllib.request
import psutil
from pathlib import Path
from typing import Dict, Any, Optional
from toolbox.core.config import config_manager
from toolbox.core.engine import console

AI_MODELS_DIR = Path(config_manager.settings.global_bin_path or "bin") / "ai_models"

# Model Registry
AVAILABLE_MODELS = {
    "upscale-x2": {
        "name": "ESRGAN_x2.onnx",
        "url": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x2plus.onnx",
        "type": "image-upscale"
    },
    "upscale-x4": {
        "name": "ESRGAN_x4.onnx",
        "url": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.onnx",
        "type": "image-upscale"
    },
    "whisper-tiny": {
        "name": "tiny.pt",
        "url": "https://openaipublic.azureedge.net/main/whisper/models/65147010a4e86fbddf13054109403d8d649e1509176313a0c444299b9e6f6a15/tiny.pt",
        "type": "audio-stt"
    },
    "whisper-base": {
        "name": "base.pt",
        "url": "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0fd87f352a775836c342f53448f86055d04589d985223000632598/base.pt",
        "type": "audio-stt"
    },
    "phi-2-gguf": {
        "name": "phi-2.Q4_K_M.gguf",
        "url": "https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q4_K_M.gguf",
        "type": "llm"
    },
    "llava-v1.5-7b-gguf": {
        "name": "llava-v1.5-7b-q4.gguf",
        "url": "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q4_k.gguf",
        "type": "vision-llm"
    },
    "llava-v1.5-7b-mmproj": {
        "name": "llava-v1.5-7b-mmproj.bin",
        "url": "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/mmproj-model-f16.pyit",
        "type": "vision-projector"
    },
    "stable-diffusion-v1-5-onnx": {
        "name": "sd-v1-5-onnx.zip",
        "url": "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/onnx.zip",
        "type": "image-gen"
    }
}

def get_engine_routing() -> Dict[str, Any]:
    """Analyze hardware and return optimal execution routing."""
    routing = {
        "device": "cpu",
        "provider": "CPUExecutionProvider",
        "vram_gb": 0,
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "threads": psutil.cpu_count(logical=False)
    }

    if is_gpu_available():
        routing["device"] = "cuda"
        routing["provider"] = "CUDAExecutionProvider"
        # In a real scenario, we'd use pynvml to get actual VRAM
        routing["vram_gb"] = 8 # Placeholder for 1.0.0 telemetry
    
    return routing

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
