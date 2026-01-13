import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build():
    # Define paths
    root = Path(__file__).parent
    src = root / "src"
    entry_point = src / "toolbox" / "cli.py"
    
    # Check if entry point exists
    if not entry_point.exists():
        print(f"Error: Entry point not found at {entry_point}")
        return

    # PyInstaller arguments
    args = [
        str(entry_point),
        "--name=toolbox",
        "--onefile",
        "--clean",
        # Include the plugins directory
        f"--add-data={src / 'toolbox' / 'plugins'}{os.pathsep}{os.path.join('toolbox', 'plugins')}",
        # Include the bin directory if it exists
        f"--add-data={root / 'bin'}{os.pathsep}bin" if (root / "bin").exists() else None,
        # Hidden imports that might not be detected due to dynamic loading
        "--hidden-import=toolbox.plugins.audio",
        "--hidden-import=toolbox.plugins.archive",
        "--hidden-import=toolbox.plugins.data",
        "--hidden-import=toolbox.plugins.doc",
        "--hidden-import=toolbox.plugins.file",
        "--hidden-import=toolbox.plugins.image",
        "--hidden-import=toolbox.plugins.network",
        "--hidden-import=toolbox.plugins.pdf",
        "--hidden-import=toolbox.plugins.security",
        "--hidden-import=toolbox.plugins.util",
        "--hidden-import=toolbox.plugins.video",
        # AI and Data dependencies
        "--hidden-import=onnxruntime",
        "--hidden-import=whisper",
        "--hidden-import=cv2",
        "--hidden-import=torch",
        "--hidden-import=numpy",
        "--hidden-import=cryptography",
        "--hidden-import=rembg",
        # Ensure common dependencies are bundled
        "--hidden-import=pyyaml",
        "--hidden-import=rich",
        "--hidden-import=click",
        "--hidden-import=pydantic",
        "--hidden-import=pypdf",
        "--hidden-import=qrcode",
        "--hidden-import=pytesseract",
        "--hidden-import=pdf2image",
    ]
    
    # Filter out None values
    args = [arg for arg in args if arg is not None]

    print(f"Building ToolBox binary with args: {' '.join(args)}")
    
    try:
        PyInstaller.__main__.run(args)
        print("\nBuild successful! Executable can be found in the 'dist' folder.")
    except Exception as e:
        print(f"\nBuild failed: {e}")

if __name__ == "__main__":
    # Create bin directory if it doesn't exist for the user to put binaries in
    os.makedirs("bin", exist_ok=True)
    build()
