# 🛠️ ToolBox CLI

A powerful, universal, and offline CLI utility suite for file processing, conversion, and management. Designed for engineers, researchers, and power users who need a robust toolset that works anywhere.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

## 🌟 Key Features

- **Universal Input**: Every command supports both **local files** and **direct web links** (URLs).
- **Modular Plugin Architecture**: Easily extendable with a clean plugin system.
- **Engine-Based Execution**: Leverages industry-standard tools like FFmpeg, Tesseract, and LibreOffice.
- **Workflow Automation**: Run complex sequences of commands from simple YAML files.
- **Privacy First**: Fully offline processing (except for initial URL downloads).

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

## 📖 Usage Examples

### Universal Input (Local or Web)
```bash
# Calculate hash from a remote file
toolbox file hash https://example.com/file.zip

# Convert a web image to a sticker
toolbox image to-sticker https://example.com/funny.gif
```

### Advanced Media
```bash
# Extract frames every 0.5 seconds
toolbox video extract-frames my_video.mp4 --interval 0.5

# Normalize audio volume
toolbox audio normalize recording.mp3 -o balanced.mp3
```

### Workflows
Create a `workflow.yaml`:
```yaml
name: Process Image
steps:
  - command: image resize {{input}} --width 800
  - command: image exif-strip {{output}}
```
Run it:
```bash
toolbox run workflow.yaml --var input=photo.jpg
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
