# Getting Started

## Installation

### From Source
```bash
git clone https://github.com/user/toolbox.git
cd toolbox
pip install -e .
```

### Windows Binary
You can also download the pre-compiled binary from the Releases page.

## Engine Setup

Some features require external engines. ToolBox makes it easy to set them up:

### Windows
Run the built-in downloader:
```bash
python setup_engines.py
```
This will download portable versions of FFmpeg and Tesseract into the `bin/` directory.

### Linux/macOS
Install engines via your package manager:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg tesseract-ocr poppler-utils libreoffice

# macOS
brew install ffmpeg tesseract poppler libreoffice
```

## Basic Usage

ToolBox follows a consistent pattern: `toolbox <plugin> <command> [args]`.

- `toolbox image ocr my_image.png`
- `toolbox video to-gif my_video.mp4`
- `toolbox config list`
