import click
import pytesseract
from pathlib import Path
from typing import List
from pypdf import PdfWriter, PdfReader
from pdf2image import convert_from_path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry
from toolbox.core.io import get_input_path

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
        def merge(inputs, output):
            """Merge multiple PDF files into one. Supports local or URL."""
            import contextlib
            merger = PdfWriter()
            
            with contextlib.ExitStack() as stack:
                paths = [stack.enter_context(get_input_path(f)) for f in inputs]
                for pdf in paths:
                    merger.append(pdf)

                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, "wb") as f:
                    merger.write(f)
            
            click.echo(f"Merged {len(inputs)} files into {output}")

        @pdf_group.command(name="split")
        @click.argument("input_pdf")
        @click.option("-o", "--output-dir", type=click.Path(), default="split_pages", help="Output directory")
        def split(input_pdf, output_dir):
            """Split a PDF into individual pages. Supports local or URL."""
            with get_input_path(input_pdf) as path:
                reader = PdfReader(path)
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
                
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)
                    with open(output_path / f"page_{i+1}.pdf", "wb") as f:
                        writer.write(f)
            
            click.echo(f"Split {len(reader.pages)} pages into {output_dir}/")

        @pdf_group.command(name="rotate")
        @click.argument("input_pdf")
        @click.option("-r", "--rotation", type=int, default=90, help="Rotation angle (degrees clockwise)")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        def rotate(input_pdf, rotation, output):
            """Rotate all pages in a PDF. Supports local or URL."""
            with get_input_path(input_pdf) as path:
                reader = PdfReader(path)
                writer = PdfWriter()
                
                for page in reader.pages:
                    page.rotate(rotation)
                    writer.add_page(page)
                
                out_path = output or f"rotated_{Path(path).name}"
                with open(out_path, "wb") as f:
                    writer.write(f)
            
            click.echo(f"Rotated PDF saved to {out_path}")

        @pdf_group.command(name="metadata")
        @click.argument("input_pdf")
        @click.option("--strip", is_flag=True, help="Remove all metadata")
        def metadata(input_pdf, strip):
            """View or strip PDF metadata. Supports local or URL."""
            with get_input_path(input_pdf) as path:
                reader = PdfReader(path)
                meta = reader.metadata
                
                if not strip:
                    if not meta:
                        click.echo("No metadata found.")
                    else:
                        for key, value in meta.items():
                            click.echo(f"{key}: {value}")
                    return

                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                
                out_path = f"stripped_{Path(path).name}"
                with open(out_path, "wb") as f:
                    writer.write(f)
            
            click.echo(f"Stripped metadata and saved to {out_path}")

        @pdf_group.command(name="extract-text")
        @click.argument("input_pdf")
        @click.option("-o", "--output", type=click.Path(), help="Output text file")
        def extract_text(input_pdf, output):
            """Extract text content from a PDF. Supports local or URL."""
            with get_input_path(input_pdf) as path:
                reader = PdfReader(path)
                text_content = []
                
                for page in reader.pages:
                    text_content.append(page.extract_text())
                
                full_text = "\n\n".join(text_content)
            
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(full_text)
                click.echo(f"Extracted text saved to {output}")
            else:
                click.echo(full_text)

        @pdf_group.command(name="ocr")
        @click.argument("input_pdf")
        @click.option("-l", "--lang", default="eng", help="OCR language (default: eng)")
        @click.option("-o", "--output", type=click.Path(), help="Output text file")
        def ocr(input_pdf, lang, output):
            """Perform OCR on a PDF. Supports local or URL."""
            tesseract = engine_registry.get("tesseract")
            poppler = engine_registry.get("poppler")
            
            if not tesseract.is_available:
                click.echo("Error: Tesseract engine not found. Please install Tesseract-OCR.")
                return
            
            if not poppler.is_available:
                click.echo("Error: Poppler not found. Required for PDF to Image conversion.")
                return

            pytesseract.pytesseract.tesseract_cmd = tesseract.path
            poppler_path = str(Path(poppler.path).parent)
            
            with get_input_path(input_pdf) as path:
                click.echo(f"Processing PDF for OCR: {input_pdf}...")
                try:
                    images = convert_from_path(path, poppler_path=poppler_path)
                    full_text = []
                    
                    with click.progressbar(images, label="Running OCR on pages") as bar:
                        for img in bar:
                            text = pytesseract.image_to_string(img, lang=lang)
                            full_text.append(text)
                    
                    result = "\n\n".join(full_text)
                    
                    if output:
                        with open(output, "w", encoding="utf-8") as f:
                            f.write(result)
                        click.echo(f"OCR text saved to {output}")
                    else:
                        click.echo(result)
                        
                except Exception as e:
                    click.echo(f"Error during PDF OCR: {str(e)}")
