import click
import hashlib
import os
from pathlib import Path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.io import get_input_path

class FilePlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="file",
            commands=["hash", "rename", "batch-rename", "info", "secure-delete"],
            engine="python"
        )

    def register_commands(self, group):
        @group.group(name="file")
        def file_group():
            """File management utilities."""
            pass

        @file_group.command(name="hash")
        @click.argument("input_source")
        @click.option("-a", "--algorithm", type=click.Choice(['md5', 'sha1', 'sha256', 'sha512']), default='sha256')
        def calculate_hash(input_source, algorithm):
            """Calculate file checksum/hash. Supports local or URL."""
            with get_input_path(input_source) as path:
                hash_func = getattr(hashlib, algorithm)()
                with open(path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_func.update(chunk)
                
                click.echo(f"{algorithm.upper()}: {hash_func.hexdigest()}")

        @file_group.command(name="secure-delete")
        @click.argument("file_path", type=click.Path(exists=True))
        @click.option("-p", "--passes", type=int, default=3, help="Number of overwrite passes")
        def secure_delete(file_path, passes):
            """Securely delete a file by overwriting it multiple times."""
            path = Path(file_path)
            if not path.is_file():
                click.echo("Error: Secure delete only works on files.")
                return

            size = path.stat().st_size
            click.echo(f"Securely deleting {file_path} ({passes} passes)...")
            
            with open(path, "ba+", buffering=0) as f:
                for i in range(passes):
                    f.seek(0)
                    f.write(os.urandom(size))
                    f.flush()
                    os.fsync(f.fileno())
            
            os.remove(path)
            click.echo("File securely deleted.")

        @file_group.command(name="rename")
        @click.argument("src", type=click.Path(exists=True))
        @click.argument("dst")
        def rename_file(src, dst):
            """Rename or move a file."""
            src_path = Path(src)
            dst_path = Path(dst)
            
            if dst_path.exists():
                if not click.confirm(f"Destination {dst} already exists. Overwrite?"):
                    return

            src_path.rename(dst_path)
            click.echo(f"Renamed {src} to {dst}")

        @file_group.command(name="batch-rename")
        @click.argument("directory", type=click.Path(exists=True))
        @click.option("-p", "--prefix", help="Prefix for new filenames")
        @click.option("-s", "--suffix", help="Suffix for new filenames")
        @click.option("-f", "--find", help="String to find")
        @click.option("-r", "--replace", help="String to replace with")
        @click.option("-e", "--ext", help="Filter by extension (e.g., .jpg)")
        def batch_rename(directory, prefix, suffix, find, replace, ext):
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
                    file.rename(new_path)
                    count += 1
            
            click.echo(f"Renamed {count} files.")

        @file_group.command(name="info")
        @click.argument("file_path", type=click.Path(exists=True))
        def file_info(file_path):
            """Get detailed file information."""
            p = Path(file_path)
            stats = p.stat()
            
            import datetime
            created = datetime.datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            click.echo(f"Name: {p.name}")
            click.echo(f"Size: {stats.st_size} bytes ({stats.st_size / 1024:.2f} KB)")
            click.echo(f"Absolute Path: {p.absolute()}")
            click.echo(f"Extension: {p.suffix}")
            click.echo(f"Created: {created}")
            click.echo(f"Modified: {modified}")
