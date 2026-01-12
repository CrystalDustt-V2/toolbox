import click
from typing import Optional
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry
from toolbox.core.io import get_input_path
from toolbox.core.utils import console, batch_process
from rich.table import Table
from pathlib import Path

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
        @click.argument("input_file", required=False)
        @click.option("--to", required=True, help="Target format (e.g., pdf, docx, html, txt)")
        @click.option("-o", "--output-dir", type=click.Path(), help="Output directory")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def convert(input_file: Optional[str], to: str, output_dir: Optional[str], dry_run: bool):
            """Convert document format using LibreOffice. Supports local or URL."""
            libreoffice = engine_registry.get("libreoffice")
            if not libreoffice:
                raise click.ClickException("LibreOffice engine not found. Please ensure it is installed and in your PATH.")

            out_dir = output_dir or "."
            
            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[yellow][DRY RUN][/yellow] Would convert [cyan]{input_file}[/cyan] to [magenta]{to}[/magenta] using LibreOffice")
                    return

                args = ["--headless", "--convert-to", to, "--outdir", out_dir, path]
                console.print(f"Converting [cyan]{input_file}[/cyan] to [magenta]{to}[/magenta]...")
                result = libreoffice.run(args)
                
                if result.returncode == 0:
                    console.print(f"[green]✓[/green] Done. Output saved in [cyan]{out_dir}[/cyan]")
                else:
                    raise click.ClickException(f"LibreOffice conversion failed: {result.stderr}")

        @doc_group.command(name="inspect")
        @click.argument("input_file", required=False)
        @batch_process
        def inspect(input_file: Optional[str]):
            """Get basic information about a document. Supports local or URL."""
            with get_input_path(input_file) as path:
                p = Path(path)
                
                table = Table(title=f"Document Info: {input_file}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="magenta")
                
                table.add_row("File", input_file)
                table.add_row("Size", f"{p.stat().st_size / 1024:.2f} KB")
                table.add_row("Extension", p.suffix)
                
                console.print(table)
