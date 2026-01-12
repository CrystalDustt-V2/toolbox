# 🛠️ ToolBox CLI

A powerful, universal, and offline CLI utility suite for file processing, conversion, and management. Designed for engineers, researchers, and power users who need a robust toolset that works anywhere.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

## 🌟 Key Features

- **Universal Input**: Every command supports both **local files** and **direct web links** (URLs).
- **Modular Plugin Architecture**: Easily extendable with a clean plugin system.
- **Engine-Based Execution**: Leverages industry-standard tools like FFmpeg, Tesseract, and LibreOffice.
- **Workflow Automation**: Run complex sequences of commands from simple YAML files with parallel execution support.
- **Dry-Run Mode**: Every command supports `--dry-run` to validate operations without making changes.
- **Privacy First**: Fully offline processing (except for initial URL downloads) with built-in SSRF protection.

## 🧩 Plugins & Capabilities

### 📁 File & Security
- **`hash`**: Calculate MD5, SHA1, SHA256, or SHA512 (local or URL).
- **`secure-delete`**: Securely overwrite files to prevent recovery.
- **`batch-rename`**: Advanced renaming with prefixes, suffixes, and pattern replacement.
- **`info`**: Detailed file statistics and metadata.

### 🖼️ Image Processing
- **`convert` / `resize` / `crop`**: Standard image manipulations.
- **`ocr`**: Extract text with advanced preprocessing (thresholding, scaling).
- **`to-sticker`**: Create WhatsApp-ready stickers from images or GIFs.
- **`exif-strip`**: Remove privacy-sensitive metadata from images.

### 🎥 Video & Audio
- **`to-sticker`**: Convert videos directly to WhatsApp stickers.
- **`extract-frames`**: Pull high-quality frames from video at specific intervals.
- **`normalize`**: Level audio volume using the `loudnorm` filter.
- **`trim` / `merge` / `compress`**: Core media editing tools.

### 📄 Document & PDF
- **`convert`**: Universal document conversion via LibreOffice (Docx, PDF, HTML, etc.).
- **`merge` / `split` / `rotate`**: Robust PDF management.
- **`extract-text`**: Extract text from PDFs or scanned documents via OCR.

### 📊 Data & Utilities
- **`convert`**: Seamlessly switch between **JSON, CSV, and YAML**.
- **`qr`**: Generate QR codes from any text or link.
- **`network info`**: Check local/public IP and connection details.
- **`network scan`**: Basic port scanner for host diagnostics.

## 🚀 Getting Started

### Prerequisites

ToolBox relies on several external engines for specialized tasks:
- **FFmpeg**: Video/Audio processing.
- **Tesseract**: OCR capabilities.
- **LibreOffice**: Document conversion.
- **Poppler**: PDF processing.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CrystalDustt-V2/toolbox.git
   cd toolbox
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Verify Engines**:
   ```bash
   toolbox status --show-paths
   ```
   Or use the intelligence check:
   ```bash
   toolbox check
   ```

4. **Setup Engines (Windows)**:
   If you don't have FFmpeg or Tesseract installed, you can use the built-in helper:
   ```bash
   python setup_engines.py
   ```
   This will download portable versions into the `bin/` folder for immediate use.

## 📖 Usage Examples

### Universal Input (Local or Web)
```bash
# Calculate hash from a remote file
toolbox file hash https://example.com/file.zip

# Convert a web image to a sticker
toolbox image to-sticker https://example.com/funny.gif
```

### Dry-Run Verification
```bash
# See what would be renamed without actually doing it
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
