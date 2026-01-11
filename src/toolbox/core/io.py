import os
import urllib.request
import urllib.parse
import tempfile
import click
import time
import socket
from pathlib import Path
from contextlib import contextmanager
from typing import Generator, Optional

def is_safe_url(url: str) -> bool:
    """Basic SSRF protection - prevent access to private IP ranges."""
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
            
        hostname = parsed.hostname
        if not hostname:
            return False
            
        # Resolve hostname to IP
        ip = socket.gethostbyname(hostname)
        
        # Check for private/loopback IP ranges
        parts = list(map(int, ip.split('.')))
        if parts[0] == 127: return False # Loopback
        if parts[0] == 10: return False  # Class A private
        if parts[0] == 172 and 16 <= parts[1] <= 31: return False # Class B private
        if parts[0] == 192 and parts[1] == 168: return False # Class C private
        if parts[0] >= 224: return False # Multicast/Reserved
        
        return True
    except Exception:
        return False

@contextmanager
def get_input_path(input_source: str, show_progress: bool = True) -> Generator[str, None, None]:
    """
    A context manager that handles both local paths and web URLs.
    Includes basic SSRF protection for URLs.
    """
    is_url = input_source.startswith(("http://", "https://"))
    temp_file = None

    try:
        if is_url:
            if not is_safe_url(input_source):
                raise click.ClickException(f"URL security check failed: {input_source}. Access to local/private network is restricted.")
                
            suffix = Path(input_source.split("?")[0]).suffix
            fd, temp_path = tempfile.mkstemp(suffix=suffix)
            os.close(fd)
            
            if show_progress:
                click.echo(f"Downloading {input_source}...")
            
            # Download with basic progress and retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    def progress_hook(count, block_size, total_size):
                        if show_progress and total_size > 0:
                            percent = min(100, int(count * block_size * 100 / total_size))
                            # Using click.echo with \r for simple progress
                            # In a more complex app we'd use click.progressbar but this is cleaner for a utility
                            print(f"\rProgress: {percent}%", end="", flush=True)

                    urllib.request.urlretrieve(input_source, temp_path, reporthook=progress_hook if show_progress else None)
                    if show_progress:
                        print() # Newline after progress
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise click.ClickException(f"Failed to download after {max_retries} attempts: {e}")
                    time.sleep(1) # Wait before retry
            
            temp_file = temp_path
            yield temp_path
        else:
            if not os.path.exists(input_source):
                raise click.ClickException(f"Local file not found: {input_source}")
            yield input_source
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass
