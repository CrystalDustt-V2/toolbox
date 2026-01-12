# Getting Started

## Installation

### From Source
```bash
git clone https://github.com/CrystalDustt-V2/toolbox.git
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

### 3. Configure Engine Paths (Optional)

If your engines are not in your system PATH, you can tell ToolBox where to find them:

```bash
# Set path for a specific engine
toolbox config set engine_paths.ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"

# OR set a global bin directory to search in
toolbox config set global_bin_path "D:\portable_tools\bin"
```

## First Steps

### Batch Processing

ToolBox makes it easy to process multiple files:

```bash
toolbox image resize --glob "*.png" --width 1280
```

### Creating Workflows

Use the interactive builder to create automation:

```bash
toolbox workflow init my_automation.yaml
```
