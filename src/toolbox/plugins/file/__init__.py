import click
import hashlib
import os
import datetime
from pathlib import Path
from typing import Optional

from rich.table import Table
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.io import get_input_path, console

class FilePlugin(BasePlugin):
    """Plugin for file management utilities."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="file",
            commands=["hash", "rename", "batch-rename", "info", "secure-delete"],
            engine="python"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="file")
        def file_group():
            """File management utilities."""
            pass

        @file_group.command(name="hash")
        @click.argument("input_source")
        @click.option("-a", "--algorithm", type=click.Choice(['md5', 'sha1', 'sha256', 'sha512']), default='sha256')
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def calculate_hash(input_source: str, algorithm: str, dry_run: bool):
            """Calculate file checksum/hash. Supports local or URL."""
            with get_input_path(input_source) as path:
                if dry_run:
                    console.print(f"[bold yellow]Would calculate {algorithm.upper()} hash for {input_source}[/bold yellow]")
                    return

                hash_func = getattr(hashlib, algorithm)()
                with open(path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_func.update(chunk)
                
                console.print(f"[bold cyan]{algorithm.upper()}:[/bold cyan] [green]{hash_func.hexdigest()}[/green]")

        @file_group.command(name="secure-delete")
        @click.argument("file_path", type=click.Path(exists=True))
        @click.option("-p", "--passes", type=int, default=3, help="Number of overwrite passes")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def secure_delete(file_path: str, passes: int, dry_run: bool):
            """Securely delete a file by overwriting it multiple times."""
            path = Path(file_path)
            if not path.is_file():
                console.print(f"[bold red]Error:[/bold red] Secure delete only works on files.")
                return

            if dry_run:
                console.print(f"[bold yellow]Would securely delete {file_path} with {passes} passes[/bold yellow]")
                return

            size = path.stat().st_size
            console.print(f"[yellow]Securely deleting {file_path} ({passes} passes)...[/yellow]")
            
            with open(path, "ba+", buffering=0) as f:
                for i in range(passes):
                    f.seek(0)
                    f.write(os.urandom(size))
                    f.flush()
                    os.fsync(f.fileno())
            
            os.remove(path)
            console.print(f"[green]✓ File securely deleted.[/green]")

        @file_group.command(name="rename")
        @click.argument("src", type=click.Path(exists=True))
        @click.argument("dst")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def rename_file(src: str, dst: str, dry_run: bool):
            """Rename or move a file."""
            src_path = Path(src)
            dst_path = Path(dst)
            
            if dst_path.exists():
                if not click.confirm(f"Destination {dst} already exists. Overwrite?"):
                    return

            if dry_run:
                console.print(f"[bold yellow]Would rename {src} to {dst}[/bold yellow]")
                return

            src_path.rename(dst_path)
            console.print(f"[green]✓ Renamed {src} to {dst}[/green]")

        @file_group.command(name="batch-rename")
        @click.argument("directory", type=click.Path(exists=True))
        @click.option("-p", "--prefix", help="Prefix for new filenames")
        @click.option("-s", "--suffix", help="Suffix for new filenames")
        @click.option("-f", "--find", help="String to find")
        @click.option("-r", "--replace", help="String to replace with")
        @click.option("-e", "--ext", help="Filter by extension (e.g., .jpg)")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def batch_rename(directory: str, prefix: Optional[str], suffix: Optional[str], find: Optional[str], replace: Optional[str], ext: Optional[str], dry_run: bool):
            """Batch rename files in a directory."""
            dir_path = Path(directory)
            count = 0
            
            for file in dir_path.iterdir():
                if not file.is_file():
                    continue
                
                if ext and file.suffix.lower() != ext.lower():
                    continue
                
                new_name = file.stem
                if find and replace is not None:
                    new_name = new_name.replace(find, replace)
                
                if prefix:
                    new_name = f"{prefix}{new_name}"
                if suffix:
                    new_name = f"{new_name}{suffix}"
                
                new_filename = f"{new_name}{file.suffix}"
                new_path = dir_path / new_filename
                
                if new_path != file:
                    if dry_run:
                        console.print(f"[bold yellow]Would rename {file.name} to {new_filename}[/bold yellow]")
                        continue
                        
                    file.rename(new_path)
                    count += 1
            
            if not dry_run:
                console.print(f"[green]✓ Renamed {count} files.[/green]")

        @file_group.command(name="info")
        @click.argument("file_path", type=click.Path(exists=True))
        def file_info(file_path: str):
            """Get detailed file information."""
            p = Path(file_path)
            stats = p.stat()
            
            created = datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            table = Table(title=f"File Information: {p.name}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Name", p.name)
            table.add_row("Size", f"{stats.st_size} bytes ({stats.st_size / 1024:.2f} KB)")
            table.add_row("Absolute Path", str(p.absolute()))
            table.add_row("Extension", p.suffix)
            table.add_row("Created", created)
            table.add_row("Modified", modified)
            
            console.print(table)
