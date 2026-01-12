import click
import shutil
import os
from pathlib import Path
from typing import Optional

from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.io import get_input_path, console

class ArchivePlugin(BasePlugin):
    """Plugin for archive and compression tools."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="archive",
            commands=["compress", "extract"],
            engine="python-built-in"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="archive")
        def archive_group():
            """Archive and compression tools (zip, tar, etc.)."""
            pass

        @archive_group.command(name="compress")
        @click.argument("source", type=click.Path(exists=True))
        @click.option("-o", "--output", help="Output filename (without extension)")
        @click.option("-f", "--format", type=click.Choice(['zip', 'tar', 'gztar', 'bztar', 'xztar']), default='zip', help="Archive format")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def compress(source: str, output: Optional[str], format: str, dry_run: bool):
            """Compress a file or directory."""
            source_path = Path(source)
            out_name = output or source_path.name
            
            if dry_run:
                console.print(f"[bold yellow]Would compress {source} into {format} archive as {out_name}.{format}[/bold yellow]")
                return

            console.print(f"[cyan]Compressing {source} into {format} archive...[/cyan]")
            try:
                # shutil.make_archive returns the path to the created archive
                result_path = shutil.make_archive(out_name, format, root_dir=source_path.parent, base_dir=source_path.name)
                console.print(f"[green]✓ Archive created: {result_path}[/green]")
            except Exception as e:
                console.print(f"[bold red]Error creating archive:[/bold red] {str(e)}")

        @archive_group.command(name="extract")
        @click.argument("archive")
        @click.option("-o", "--output-dir", type=click.Path(), default=".", help="Directory to extract into")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def extract(archive: str, output_dir: str, dry_run: bool):
            """Extract an archive file. Supports local or URL."""
            with get_input_path(archive) as path:
                archive_path = Path(path)
                out_path = Path(output_dir)
                
                if dry_run:
                    console.print(f"[bold yellow]Would extract {archive} to {output_dir}[/bold yellow]")
                    return

                out_path.mkdir(parents=True, exist_ok=True)
                console.print(f"[cyan]Extracting {archive} to {output_dir}...[/cyan]")
                try:
                    shutil.unpack_archive(archive_path, extract_dir=out_path)
                    console.print(f"[green]✓ Successfully extracted {archive}[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error extracting archive:[/bold red] {str(e)}")
