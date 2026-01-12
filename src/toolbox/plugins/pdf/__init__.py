import click
import pytesseract
import contextlib
from pathlib import Path
from typing import List, Optional, Tuple
from pypdf import PdfWriter, PdfReader
from pdf2image import convert_from_path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry, console
from toolbox.core.io import get_input_path
from toolbox.core.utils import batch_process
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

class PdfPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="pdf",
            commands=["merge", "split", "rotate", "metadata", "extract-text", "ocr"],
            engine="pypdf"
        )

    def register_commands(self, group):
        @group.group(name="pdf")
        def pdf_group():
            """PDF management tools."""
            pass

        @pdf_group.command(name="merge")
        @click.argument("inputs", nargs=-1, required=True)
        @click.option("-o", "--output", type=click.Path(), default="merged.pdf", help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def merge(inputs: Tuple[str, ...], output: str, dry_run: bool):
            """Merge multiple PDF files into one. Supports local or URL."""
            if dry_run:
                console.print(f"[yellow][DRY RUN][/yellow] Would merge [cyan]{len(inputs)}[/cyan] files into [cyan]{output}[/cyan]")
                return

            merger = PdfWriter()
            
            try:
                with contextlib.ExitStack() as stack:
                    paths = [stack.enter_context(get_input_path(f)) for f in inputs]
                    for pdf in paths:
                        merger.append(pdf)

                    output_path = Path(output)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, "wb") as f:
                        merger.write(f)
                
                console.print(f"[green]✓[/green] Merged [cyan]{len(inputs)}[/cyan] files into [cyan]{output}[/cyan]")
            except Exception as e:
                raise click.ClickException(f"Error merging PDFs: {e}")

        @pdf_group.command(name="split")
        @click.argument("input_file", required=False)
        @click.option("-o", "--output-dir", type=click.Path(), default="split_pages", help="Output directory")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def split(input_file: Optional[str], output_dir: str, dry_run: bool):
            """Split a PDF into individual pages. Supports local or URL."""
            with get_input_path(input_file) as path:
                reader = PdfReader(path)
                num_pages = len(reader.pages)
                
                if dry_run:
                    console.print(f"[yellow][DRY RUN][/yellow] Would split [cyan]{input_file}[/cyan] into [cyan]{num_pages}[/cyan] pages in [cyan]{output_dir}/[/cyan]")
                    return

                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
                
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)
                    with open(output_path / f"page_{i+1}.pdf", "wb") as f:
                        writer.write(f)
            
            console.print(f"[green]✓[/green] Split [cyan]{num_pages}[/cyan] pages into [cyan]{output_dir}/[/cyan]")

        @pdf_group.command(name="rotate")
        @click.argument("input_file", required=False)
        @click.option("-r", "--rotation", type=int, default=90, help="Rotation angle (degrees clockwise)")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def rotate(input_file: Optional[str], rotation: int, output: Optional[str], dry_run: bool):
            """Rotate all pages in a PDF. Supports local or URL."""
            with get_input_path(input_file) as path:
                out_path = output or f"rotated_{Path(path).name}"
                
                if dry_run:
                    console.print(f"[yellow][DRY RUN][/yellow] Would rotate [cyan]{input_file}[/cyan] by [magenta]{rotation}[/magenta] degrees to [cyan]{out_path}[/cyan]")
                    return

                reader = PdfReader(path)
                writer = PdfWriter()
                
                for page in reader.pages:
                    page.rotate(rotation)
                    writer.add_page(page)
                
                with open(out_path, "wb") as f:
                    writer.write(f)
            
            console.print(f"[green]✓[/green] Rotated PDF saved to [cyan]{out_path}[/cyan]")

        @pdf_group.command(name="metadata")
        @click.argument("input_file", required=False)
        @click.option("--strip", is_flag=True, help="Remove all metadata")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def metadata(input_file: Optional[str], strip: bool, dry_run: bool):
            """View or strip PDF metadata. Supports local or URL."""
            with get_input_path(input_file) as path:
                reader = PdfReader(path)
                meta = reader.metadata
                
                if not strip:
                    table = Table(title=f"PDF Metadata: {input_file}")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="magenta")
                    
                    if not meta:
                        table.add_row("Status", "No metadata found")
                    else:
                        for key, value in meta.items():
                            table.add_row(str(key), str(value))
                    
                    console.print(table)
                    return

                out_path = f"stripped_{Path(path).name}"
                if dry_run:
                    console.print(f"[yellow][DRY RUN][/yellow] Would strip metadata from [cyan]{input_file}[/cyan] and save to [cyan]{out_path}[/cyan]")
                    return

                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                
                with open(out_path, "wb") as f:
                    writer.write(f)
            
            console.print(f"[green]✓[/green] Stripped metadata and saved to [cyan]{out_path}[/cyan]")

        @pdf_group.command(name="extract-text")
        @click.argument("input_file", required=False)
        @click.option("-o", "--output", type=click.Path(), help="Output text file")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def extract_text(input_file: Optional[str], output: Optional[str], dry_run: bool):
            """Extract text content from a PDF. Supports local or URL."""
            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[yellow][DRY RUN][/yellow] Would extract text from [cyan]{input_file}[/cyan]")
                    return

                reader = PdfReader(path)
                text_content = []
                
                for page in reader.pages:
                    text_content.append(page.extract_text() or "")
                
                full_text = "\n\n".join(text_content)
            
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(full_text)
                console.print(f"[green]✓[/green] Extracted text saved to [cyan]{output}[/cyan]")
            else:
                console.print(full_text)

        @pdf_group.command(name="ocr")
        @click.argument("input_file", required=False)
        @click.option("-l", "--lang", default="eng", help="OCR language (default: eng)")
        @click.option("-o", "--output", type=click.Path(), help="Output text file")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def ocr(input_file: Optional[str], lang: str, output: Optional[str], dry_run: bool):
            """Perform OCR on a PDF. Supports local or URL."""
            tesseract = engine_registry.get("tesseract")
            poppler = engine_registry.get("poppler")
            
            if not tesseract or not tesseract.is_available:
                raise click.ClickException("Tesseract engine not found. Please install Tesseract-OCR.")
            
            if not poppler or not poppler.is_available:
                raise click.ClickException("Poppler not found. Required for PDF to Image conversion.")

            pytesseract.pytesseract.tesseract_cmd = tesseract.path
            poppler_path = str(Path(poppler.path).parent)
            
            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[yellow][DRY RUN][/yellow] Would perform OCR on [cyan]{input_file}[/cyan] (lang: {lang})")
                    return

                console.print(f"Processing PDF for OCR: [cyan]{input_file}[/cyan]...")
                try:
                    images = convert_from_path(path, poppler_path=poppler_path)
                    full_text = []
                    
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TaskProgressColumn(),
                        console=console
                    ) as progress:
                        task = progress.add_task("Running OCR on pages...", total=len(images))
                        for img in images:
                            text = pytesseract.image_to_string(img, lang=lang)
                            full_text.append(text)
                            progress.update(task, advance=1)
                    
                    result = "\n\n".join(full_text)
                    
                    if output:
                        with open(output, "w", encoding="utf-8") as f:
                            f.write(result)
                        console.print(f"[green]✓[/green] OCR text saved to [cyan]{output}[/cyan]")
                    else:
                        console.print(result)
                        
                except Exception as e:
                    raise click.ClickException(f"Error during PDF OCR: {e}")
