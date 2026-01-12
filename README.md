# 🛠️ ToolBox CLI

A powerful, universal, and offline CLI utility suite for file processing, conversion, and management. Designed for engineers, researchers, and power users who need a robust toolset that works anywhere.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

## 🌟 Key Features

- **Universal Input**: Every command supports both **local files** and **direct web links** (URLs).
- **High-Performance Concurrency**: Built-in parallel processing for batch operations via `--parallel`.
- **AI-Powered Capabilities**: Integrated AI tools for background removal and advanced OCR.
- **Privacy & Security**: Secure file shredding, metadata sanitization, and AES-256-GCM encryption.
- **Modular Plugin Architecture**: Easily extendable with a clean plugin system.
- **Workflow Automation**: Run, watch, or schedule complex sequences of commands via YAML.
- **Dry-Run Mode**: Every command supports `--dry-run` to validate operations without making changes.

## 🧩 Plugins & Capabilities

### 📁 File & Security
- **`hash`**: Calculate MD5, SHA1, SHA256, or SHA512.
- **`shred`**: Securely overwrite files (DoD 5220.22-M) to prevent recovery.
- **`encrypt` / `decrypt`**: AES-256-GCM file protection.
- **`batch-rename`**: Advanced renaming with parallel support.
- **`info`**: Detailed file statistics and metadata.

### 🖼️ Image Processing
- **`remove-bg`**: **AI-powered** background removal using `rembg`.
- **`convert` / `resize` / `crop`**: Standard image manipulations.
- **`ocr`**: Extract text with advanced preprocessing.
- **`to-sticker`**: Create WhatsApp-ready stickers.
- **`exif-strip`**: Remove privacy-sensitive metadata.

### 🎥 Video & Audio
- **`watermark` / `remove-watermark`**: Add or remove logos/text from video.
- **`to-sticker`**: Convert videos directly to WhatsApp stickers.
- **`extract-frames`**: Pull high-quality frames from video.
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

1. **Clone & Install**:
   ```bash
   git clone https://github.com/CrystalDustt-V2/toolbox.git
   cd toolbox
   pip install .
   ```

   *Alternatively, once published to PyPI:*
   ```bash
   pip install toolbox-universal
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
toolbox file batch-rename ./docs --prefix "v1_" --dry-run
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
