import click
import glob
import os
import socket
import urllib.parse
import functools
from pathlib import Path
from typing import Callable, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from toolbox.core.engine import console

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

def batch_process(func: Callable):
    """
    Decorator to add --glob and --parallel support to a click command.
    """
    @click.option("--glob", "glob_pattern", help="Glob pattern to process multiple files (e.g. '*.jpg')")
    @click.option("--parallel", is_flag=True, help="Enable parallel processing for batch operations")
    @click.option("--workers", type=int, default=os.cpu_count(), help="Number of worker threads (default: CPU count)")
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx, glob_pattern, parallel, workers, *args, **kwargs):
        input_file = kwargs.get('input_file')
        
        if glob_pattern:
            files = [f for f in glob.glob(glob_pattern, recursive=True) if os.path.isfile(f)]
            if not files:
                console.print(f"[yellow]No files matched pattern: {glob_pattern}[/yellow]")
                return
            
            console.print(f"[cyan]Batch processing {len(files)} files (Parallel: {parallel})...[/cyan]")
            success_count = 0
            
            if parallel:
                with ThreadPoolExecutor(max_workers=workers) as executor:
                    futures = []
                    for file_path in files:
                        current_kwargs = kwargs.copy()
                        current_kwargs['input_file'] = file_path
                        # We use ctx.invoke but in a thread-safe-ish way for basic operations
                        futures.append(executor.submit(ctx.invoke, func, **current_kwargs))
                    
                    for future in as_completed(futures):
                        try:
                            future.result()
                            success_count += 1
                        except Exception as e:
                            console.print(f"[red]Parallel error: {e}[/red]")
            else:
                for file_path in files:
                    try:
                        current_kwargs = kwargs.copy()
                        current_kwargs['input_file'] = file_path
                        ctx.invoke(func, **current_kwargs)
                        success_count += 1
                    except Exception as e:
                        console.print(f"[red]Error processing {file_path}: {e}[/red]")
            
            console.print(f"[green]✓ Batch processing complete: {success_count}/{len(files)} successful.[/green]")
        else:
            if not input_file:
                raise click.UsageError("Missing argument 'INPUT_FILE' or '--glob' option.")
            return ctx.invoke(func, **kwargs)
            
    return wrapper
