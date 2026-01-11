import os
import urllib.request
import tempfile
import click
import time
from pathlib import Path
from contextlib import contextmanager
from typing import Generator, Optional

@contextmanager
def get_input_path(input_source: str, show_progress: bool = True) -> Generator[str, None, None]:
    """
    A context manager that handles both local paths and web URLs.
    """
    is_url = input_source.startswith(("http://", "https://"))
    temp_file = None

    try:
        if is_url:
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
