import os
import shutil
import subprocess
import sys
from pathlib import Path

def clean():
    """Clean up build artifacts."""
    print("Cleaning up build artifacts...")
    dirs_to_remove = ['build', 'dist', '*.egg-info']
    for pattern in dirs_to_remove:
        for p in Path('.').rglob(pattern):
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()

def build():
    """Build the package."""
    print("Building package (sdist and wheel)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "build"])
    subprocess.check_call([sys.executable, "-m", "build"])

def verify():
    """Verify the package with twine."""
    print("Verifying package with twine...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "twine"])
    subprocess.check_call([sys.executable, "-m", "twine", "check", "dist/*"])

def upload(test_pypi=True):
    """Upload to PyPI."""
    if test_pypi:
        print("Uploading to TestPyPI...")
        subprocess.check_call([
            sys.executable, "-m", "twine", "upload", 
            "--repository", "testpypi", "dist/*"
        ])
    else:
        print("Uploading to PyPI...")
        subprocess.check_call([sys.executable, "-m", "twine", "upload", "dist/*"])

def main():
    if len(sys.argv) < 2:
        print("Usage: python publish.py [build|verify|upload-test|upload-prod|all]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "build":
        clean()
        build()
    elif command == "verify":
        verify()
    elif command == "upload-test":
        upload(test_pypi=True)
    elif command == "upload-prod":
        upload(test_pypi=False)
    elif command == "all":
        clean()
        build()
        verify()
        print("\nBuild and verification complete. Run 'python publish.py upload-test' to upload.")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
