# Getting Started

## Installation

### 🚀 Recommended: Using `pipx`
`pipx` is the standard for installing Python CLI applications. It ensures that ToolBox is isolated from other packages and, most importantly, **it handles your system PATH automatically**.

#### 1. Install `pipx` (if you haven't)
If you don't have `pipx` installed, run these commands:
```bash
python -m pip install --user pipx
python -m pipx ensurepath
```
*Restart your terminal after this step.*

#### 2. Install ToolBox
```bash
pipx install toolbox-universal
```

### Using `pip` (Advanced)
If you prefer using standard `pip`:
```bash
pip install toolbox-universal
```
> **Note**: On Windows, you might need to manually add the Python `Scripts` folder to your PATH for the `toolbox` command to work.

### Portable: Running via Python
You can always run ToolBox without a direct command by using the module execution:
```bash
python -m toolbox [command]
```

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

## Sanity Checks

```bash
toolbox status
toolbox check
toolbox plugin list
```

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

### Running Workflows

```bash
toolbox workflow run my_automation.yaml
toolbox workflow run my_automation.yaml -v input_file=photo.jpg
toolbox workflow watch ./incoming my_automation.yaml --ext .pdf --ext .png
toolbox workflow schedule my_automation.yaml --interval 60 --immediate
```

### Common Tasks

```bash
toolbox pdf sanitize report.pdf -o report_sanitized.pdf
toolbox file encrypt secret.zip --password "your-password"
toolbox image ocr screenshot.png
toolbox video compress input.mp4 -o out.mp4
```
