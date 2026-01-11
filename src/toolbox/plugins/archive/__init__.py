import click
import shutil
import os
from pathlib import Path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.io import get_input_path

class ArchivePlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="archive",
            commands=["compress", "extract"],
            engine="python-built-in"
        )

    def register_commands(self, group):
        @group.group(name="archive")
        def archive_group():
            """Archive and compression tools (zip, tar, etc.)."""
            pass

        @archive_group.command(name="compress")
        @click.argument("source", type=click.Path(exists=True))
        @click.option("-o", "--output", help="Output filename (without extension)")
        @click.option("-f", "--format", type=click.Choice(['zip', 'tar', 'gztar', 'bztar', 'xztar']), default='zip', help="Archive format")
        def compress(source, output, format):
            """Compress a file or directory."""
            source_path = Path(source)
            out_name = output or source_path.name
            
            click.echo(f"Compressing {source} into {format} archive...")
            try:
                # shutil.make_archive returns the path to the created archive
                result_path = shutil.make_archive(out_name, format, root_dir=source_path.parent, base_dir=source_path.name)
                click.echo(f"Archive created: {result_path}")
            except Exception as e:
                click.echo(f"Error creating archive: {str(e)}")

        @archive_group.command(name="extract")
        @click.argument("archive")
        @click.option("-o", "--output-dir", type=click.Path(), default=".", help="Directory to extract into")
        def extract(archive, output_dir):
            """Extract an archive file. Supports local or URL."""
            with get_input_path(archive) as path:
                archive_path = Path(path)
                out_path = Path(output_dir)
                out_path.mkdir(parents=True, exist_ok=True)
                
                click.echo(f"Extracting {archive} to {output_dir}...")
                try:
                    shutil.unpack_archive(archive_path, extract_dir=out_path)
                    click.echo(f"Successfully extracted {archive}")
                except Exception as e:
                    click.echo(f"Error extracting archive: {str(e)}")
