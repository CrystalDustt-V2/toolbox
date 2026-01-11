import click
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry
from toolbox.core.io import get_input_path

class DocPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="doc",
            commands=["convert", "inspect"],
            engine="libreoffice"
        )

    def register_commands(self, group):
        @group.group(name="doc")
        def doc_group():
            """Document conversion and inspection tools."""
            pass

        @doc_group.command(name="convert")
        @click.argument("input_file")
        @click.option("--to", required=True, help="Target format (e.g., pdf, docx, html, txt)")
        @click.option("-o", "--output-dir", type=click.Path(), help="Output directory")
        def convert(input_file, to, output_dir):
            """Convert document format using LibreOffice. Supports local or URL."""
            libreoffice = engine_registry.get("libreoffice")
            out_dir = output_dir or "."
            
            with get_input_path(input_file) as path:
                args = ["--headless", "--convert-to", to, "--outdir", out_dir, path]
                click.echo(f"Converting {input_file} to {to}...")
                libreoffice.run(args)
            
            click.echo(f"Done. Output saved in {out_dir}")

        @doc_group.command(name="inspect")
        @click.argument("input_file")
        def inspect(input_file):
            """Get basic information about a document. Supports local or URL."""
            with get_input_path(input_file) as path:
                from pathlib import Path
                p = Path(path)
                click.echo(f"File: {input_file}")
                click.echo(f"Size: {p.stat().st_size / 1024:.2f} KB")
                click.echo(f"Extension: {p.suffix}")
