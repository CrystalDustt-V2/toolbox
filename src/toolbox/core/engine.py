import shutil
import subprocess
import sys
import os
import re
from pathlib import Path
from typing import List, Optional, Tuple, Dict
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from toolbox.core.config import config_manager

console = Console()

def get_bundled_bin_path() -> Optional[Path]:
    """Get the path to bundled binaries if they exist."""
    # If running as a PyInstaller bundle
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_bin = Path(sys._MEIPASS) / "bin"
    else:
        # If running in development, look for a 'bin' folder in the project root
        # Project root is two levels up from this file: src/toolbox/core/engine.py
        bundle_bin = Path(__file__).parent.parent.parent.parent / "bin"
    
    return bundle_bin if bundle_bin.exists() else None

class EngineError(Exception):
    """Base class for engine related errors."""
    pass

class BaseEngine:
    def __init__(self, name: str, binary_name: str):
        self.name = name
        self.binary_name = binary_name
        self._path: Optional[str] = None
        self.verbose = False

    def get_install_hint(self) -> str:
        """Return a string with instructions on how to install this engine."""
        return f"Install {self.name} and add it to your PATH, or place '{self.binary_name}' in the 'bin/' folder."

    @property
    def is_available(self) -> bool:
        return self.path is not None

    @property
    def path(self) -> Optional[str]:
        if self._path is None:
            # 1. Check user configuration first
            config_path = config_manager.settings.engine_paths.get(self.name.lower())
            if config_path and os.path.exists(config_path):
                self._path = config_path
                return self._path

            # 2. Check bundled binaries
            bin_dir = get_bundled_bin_path()
            if bin_dir:
                # On Windows, binaries usually end in .exe
                exts = [".exe", ""] if os.name == "nt" else [""]
                for ext in exts:
                    bundled_binary = bin_dir / f"{self.binary_name}{ext}"
                    if bundled_binary.exists():
                        self._path = str(bundled_binary)
                        break
            
            # 2. If not found in bundle, check system PATH
            if self._path is None:
                self._path = shutil.which(self.binary_name)
        return self._path

    def run(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        if not self.is_available:
            hint = self.get_install_hint()
            raise EngineError(f"Engine '{self.name}' ({self.binary_name}) not found.\nHint: {hint}")
        
        full_command = [self.path] + args
        if self.verbose:
            console.print(f"[dim]Running: {' '.join(full_command)}[/dim]")

        try:
            # Use shell=True on Windows for better binary discovery if needed, 
            # but generally not recommended for security unless necessary.
            # Here we use the direct path found by shutil.which.
            result = subprocess.run(full_command, capture_output=True, text=True, check=check)
            
            if self.verbose and result.stdout:
                console.print(f"[dim]Output:\n{result.stdout}[/dim]")
            
            return result
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr or e.stdout or str(e)
            console.print(f"[bold red]Error running {self.name}:[/bold red]\n{error_msg}")
            raise EngineError(f"{self.name} failed with exit code {e.returncode}") from e
        except Exception as e:
            console.print(f"[bold red]Unexpected error running {self.name}:[/bold red] {str(e)}")
            raise EngineError(f"Failed to execute {self.name}") from e

class FFmpegEngine(BaseEngine):
    def __init__(self):
        super().__init__("FFmpeg", "ffmpeg")

    def get_install_hint(self) -> str:
        return "Download from ffmpeg.org and add to PATH, or place 'ffmpeg.exe' in 'bin/'."

    def run_with_progress(self, args: List[str], label: str = "Processing") -> subprocess.CompletedProcess:
        """Run FFmpeg with a progress bar."""
        if not self.is_available:
            hint = self.get_install_hint()
            raise EngineError(f"Engine 'FFmpeg' not found.\nHint: {hint}")

        # Add -progress - to get machine-readable output on stdout
        # But we also need to keep the original args.
        # It's better to parse stderr for 'time=' if we don't want to mess with stdout.
        full_command = [self.path] + args
        
        if self.verbose:
            console.print(f"[dim]Running with progress: {' '.join(full_command)}[/dim]")

        duration = None
        duration_re = re.compile(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})")
        time_re = re.compile(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})")

        def to_seconds(h, m, s, ms):
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 100

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(label, total=100)
            
            # Use Popen to read stderr line by line
            process = subprocess.Popen(
                full_command,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )

            stdout_content = []
            stderr_content = []

            # FFmpeg writes progress info to stderr
            while True:
                line = process.stderr.readline()
                if not line and process.poll() is not None:
                    break
                
                if line:
                    stderr_content.append(line)
                    # Parse duration
                    if duration is None:
                        match = duration_re.search(line)
                        if match:
                            duration = to_seconds(*match.groups())
                    
                    # Parse current time
                    match = time_re.search(line)
                    if match and duration:
                        current_time = to_seconds(*match.groups())
                        percent = min(100, (current_time / duration) * 100)
                        progress.update(task, completed=percent)

            process.wait()
            
            if process.returncode != 0:
                error_msg = "".join(stderr_content[-10:]) # last 10 lines
                raise EngineError(f"FFmpeg failed with exit code {process.returncode}\n{error_msg}")

            return subprocess.CompletedProcess(
                args=full_command,
                returncode=process.returncode,
                stdout="".join(stdout_content),
                stderr="".join(stderr_content)
            )

class ImageMagickEngine(BaseEngine):
    def __init__(self):
        # On Windows it's often 'magick', on Linux 'convert' or 'magick'
        binary = "magick" if shutil.which("magick") else "convert"
        super().__init__("ImageMagick", binary)

    def get_install_hint(self) -> str:
        return "Install from imagemagick.org. Ensure 'magick' or 'convert' is in PATH."

class PopplerEngine(BaseEngine):
    def __init__(self):
        super().__init__("Poppler", "pdftotext") # Using pdftotext as a probe

    def get_install_hint(self) -> str:
        return "Install Poppler (via conda, brew, or download for Windows) and add 'bin/' to PATH."

    @property
    def path(self) -> Optional[str]:
        if self._path is None:
            self._path = shutil.which(self.binary_name)
            # Common Windows installation paths (if extracted to C:\poppler or similar)
            if self._path is None and shutil.os.name == "nt":
                common_paths = [
                    r"C:\poppler\bin\pdftotext.exe",
                    r"C:\Program Files\poppler\bin\pdftotext.exe",
                    r"C:\Program Files (x86)\poppler\bin\pdftotext.exe"
                ]
                for p in common_paths:
                    if shutil.os.path.exists(p):
                        self._path = p
                        break
        return self._path

class TesseractEngine(BaseEngine):
    def __init__(self):
        super().__init__("Tesseract", "tesseract")

    def get_install_hint(self) -> str:
        return "Install Tesseract-OCR from GitHub/UB-Mannheim and add to PATH."

    @property
    def path(self) -> Optional[str]:
        if self._path is None:
            self._path = shutil.which(self.binary_name)
            # Common Windows installation path
            if self._path is None and shutil.os.name == "nt":
                common_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                if shutil.os.path.exists(common_path):
                    self._path = common_path
        return self._path

class LibreOfficeEngine(BaseEngine):
    def __init__(self):
        # Common binary names: soffice, libreoffice
        binary = "soffice" if shutil.which("soffice") else "libreoffice"
        super().__init__("LibreOffice", binary)

    def get_install_hint(self) -> str:
        return "Install LibreOffice and ensure 'soffice' or 'libreoffice' is in PATH."

    @property
    def path(self) -> Optional[str]:
        if self._path is None:
            self._path = shutil.which(self.binary_name)
            # Common Windows installation path fallback
            if self._path is None and shutil.os.name == "nt":
                # LibreOffice usually installs to C:\Program Files\LibreOffice\program\soffice.exe
                common_paths = [
                    r"C:\Program Files\LibreOffice\program\soffice.exe",
                    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
                ]
                for p in common_paths:
                    if shutil.os.path.exists(p):
                        self._path = p
                        break
        return self._path

class EngineRegistry:
    def __init__(self):
        self.engines = {
            "ffmpeg": FFmpegEngine(),
            "imagemagick": ImageMagickEngine(),
            "poppler": PopplerEngine(),
            "tesseract": TesseractEngine(),
            "libreoffice": LibreOfficeEngine(),
        }

    def get(self, name: str) -> BaseEngine:
        engine = self.engines.get(name.lower())
        if not engine:
            raise EngineError(f"Unknown engine: {name}")
        return engine

    def check_all(self) -> List[Tuple[str, bool, str]]:
        return [(name, eng.is_available, eng.get_install_hint()) for name, eng in self.engines.items()]

engine_registry = EngineRegistry()
