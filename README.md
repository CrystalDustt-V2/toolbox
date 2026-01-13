# 🛠️ ToolBox CLI

A powerful, universal, and offline CLI utility suite for file processing, conversion, and management. Designed for engineers, researchers, and power users who need a robust toolset that works anywhere.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

## 🌟 Key Features

- **High-Performance Concurrency**: Built-in parallel processing for batch operations via `--parallel`.
- **AI-Powered Capabilities**: Integrated local AI for **Image Upscaling (ESRGAN)**, **Speech-to-Text (Whisper)**, and background removal.
- **Advanced Workflow Logic**: YAML-based automation with **conditional branching (if/then/else)** and dynamic variables.
- **GPU Acceleration**: Optional hardware acceleration via global `--gpu` flag.
- **Privacy & Security**: **Steganography**, **Secure Vaults**, file shredding, and metadata sanitization.
- **Universal Input**: Every command supports both **local files** and **direct web links** (URLs).

## 🧩 Plugins & Capabilities

### 📁 File & Security
- **`vault-encrypt` / `vault-decrypt`**: **New!** Create secure, password-protected vaults for files.
- **`steg-hide` / `steg-extract`**: **New!** Hide sensitive data inside images using steganography.
- **`shred`**: Securely overwrite files (DoD 5220.22-M) to prevent recovery.
- **`hash`**: Calculate MD5, SHA1, SHA256, or SHA512.
- **`encrypt` / `decrypt`**: AES-256-GCM file protection.
- **`batch-rename`**: Advanced renaming with parallel support.
- **`info`**: Detailed file statistics and metadata.

### 🖼️ Image Processing
- **`upscale`**: **New!** AI-powered super-resolution (2x, 4x) using ESRGAN.
- **`remove-bg`**: AI-powered background removal using `rembg`.
- **`convert` / `resize` / `crop`**: Standard image manipulations.
- **`ocr`**: Extract text with advanced preprocessing.

### 🎥 Video & Audio
- **`stt`**: **New!** Speech-to-Text transcription using OpenAI Whisper (Offline).
- **`watermark` / `remove-watermark`**: Add or remove logos/text from video.
- **`normalize`**: Level audio volume using `loudnorm`.
- **`trim` / `merge` / `compress`**: Core media editing tools.

### 📄 Document & PDF
- **`sanitize`**: Remove metadata and hidden information from PDFs.
- **`convert`**: Universal document conversion via LibreOffice.
- **`merge` / `split` / `rotate`**: Robust PDF management.
- **`extract-text`**: OCR-based text extraction from PDFs.

### 📊 Data & Utilities
- **`sql-export`**: Export JSON/CSV/YAML datasets to SQLite.
- **`convert`**: Seamlessly switch between JSON, CSV, and YAML.
- **`qr`**: Generate QR codes from any text or link.
- **`network info/scan`**: Connection diagnostics and port scanning.

## 🚀 Getting Started

### Prerequisites

ToolBox relies on specialized engines:
- **FFmpeg**: Video/Audio processing.
- **Tesseract**: OCR capabilities.
- **LibreOffice**: Document conversion.
- **Poppler**: PDF processing.

### Installation

#### 🚀 Recommended: Using pipx (Automatic PATH setup)
`pipx` is the best way to install ToolBox. It installs the tool in an isolated environment and **automatically handles your system PATH** so the `toolbox` command works immediately.

```bash
# If you don't have pipx yet:
python -m pip install --user pipx
python -m pipx ensurepath

# Install ToolBox:
pipx install toolbox-universal
```
*Note: You may need to restart your terminal after installing `pipx` for the first time.*

#### Alternative: Using pip
```bash
pip install toolbox-universal
```

#### Portable: Run via Python
If you don't want to install it:
```bash
python -m toolbox --help
```

2. **Setup Engines (Windows)**:
   ```bash
   toolbox check  # Check current status
   python setup_engines.py  # Auto-download portable engines
   ```

## 📖 Advanced Usage

### Parallel Batch Processing
```bash
# Resize all JPEGs in a folder using 8 worker threads
toolbox image resize --glob "*.jpg" -w 800 --parallel --workers 8
```

### Automation (Workflows)
```yaml
# Example 0.3.0 Workflow with Logic
name: Smart Media Processor
steps:
  - name: Check if image
    if: "{file.suffix} == .jpg"
    then:
      - name: Upscale Image
        command: "toolbox image upscale {input_file} -s 4"
    else:
      - name: Transcribe Audio
        command: "toolbox audio stt {input_file}"
```
```bash
# Run a sequence of commands
toolbox workflow run process_images.yaml

# Watch a directory for new files and auto-trigger a workflow
toolbox workflow watch ./incoming my_workflow.yaml --ext .pdf

# Schedule a workflow to run every 60 minutes
toolbox workflow schedule maintenance.yaml --interval 60 --immediate
```

### Logging
```bash
# Run a command and save detailed logs to a file
toolbox file hash large_file.iso --log-file ./logs/audit.log
```

### Workflow Automation
```bash
# Run a complex automation sequence
toolbox workflow run examples/universal_demo.yaml
```

### Advanced Media
```bash
# Extract frames every 0.5 seconds
toolbox video extract-frames my_video.mp4 --interval 0.5

# Normalize audio volume
toolbox audio normalize recording.mp3 -o balanced.mp3
```

### **Workflow Automation**
Automate complex tasks using YAML workflows:
```bash
# Interactively create a new workflow
toolbox workflow init my_tasks.yaml

# Run the workflow
toolbox workflow run my_tasks.yaml

# Run with variable overrides and dry-run
toolbox workflow run my_tasks.yaml -v input_file=photo.jpg --dry-run
```

### **Batch Processing**
Many commands now support processing multiple files at once using glob patterns:
```bash
# Resize all JPEGs in a folder
toolbox image resize --glob "*.jpg" -w 800

# Convert all videos in a folder to GIF
toolbox video to-gif --glob "videos/*.mp4"
```

### **Global Engine Path**
You can now set a global directory where ToolBox will look for engine binaries (ffmpeg, tesseract, etc.):
```bash
toolbox config set global_bin_path "C:\MyTools\bin"
```

## 🛠️ Configuration

Settings are stored in `config.yaml`. Manage them via CLI:
```bash
toolbox config list
toolbox config set engine_paths.ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
