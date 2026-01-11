import os
import sys
import zipfile
import urllib.request
from pathlib import Path

# ToolBox Engine Downloader (Windows)
# Helps users get FFmpeg and Tesseract quickly.

BIN_DIR = Path(__file__).parent / "bin"

ENGINES = {
    "ffmpeg": {
        "url": "https://github.com/GyanD/codexffmpeg/releases/download/7.1/ffmpeg-7.1-essentials_build.zip",
        "extract_path": "ffmpeg-7.1-essentials_build/bin/ffmpeg.exe",
        "target": "ffmpeg.exe"
    },
    "tesseract": {
        "url": "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe",
        "is_installer": True,
        "note": "Tesseract requires a manual installation. Please run the downloaded installer."
    }
}

def download_file(url, target_path):
    print(f"Downloading {url}...")
    def progress(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\rProgress: {percent}%")
        sys.stdout.flush()
    
    urllib.request.urlretrieve(url, target_path, reporthook=progress)
    print("\nDownload complete.")

def setup_ffmpeg():
    temp_zip = BIN_DIR / "ffmpeg.zip"
    download_file(ENGINES["ffmpeg"]["url"], temp_zip)
    
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
        # Only extract the binary
        for member in zip_ref.namelist():
            if member.endswith("ffmpeg.exe"):
                content = zip_ref.read(member)
                with open(BIN_DIR / "ffmpeg.exe", "wb") as f:
                    f.write(content)
                break
    
    os.remove(temp_zip)
    print("FFmpeg setup complete in 'bin/' folder.")

def main():
    if os.name != "nt":
        print("This script is intended for Windows users.")
        return

    os.makedirs(BIN_DIR, exist_ok=True)
    
    print("--- ToolBox Engine Downloader ---")
    print("1. Download FFmpeg (Portable)")
    print("2. Download Tesseract (Installer)")
    print("3. Exit")
    
    choice = input("Select an option: ")
    
    if choice == "1":
        setup_ffmpeg()
    elif choice == "2":
        target = BIN_DIR / "tesseract_installer.exe"
        download_file(ENGINES["tesseract"]["url"], target)
        print(f"\n{ENGINES['tesseract']['note']}")
        print(f"Installer saved to: {target}")
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()
