import click
import pytesseract
import os
from typing import Optional
from pathlib import Path
from PIL import Image, ExifTags, ImageSequence, ImageOps
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry, console
from toolbox.core.io import get_input_path
from toolbox.core.utils import batch_process

class ImagePlugin(BasePlugin):
    """Plugin for image processing using Pillow and Tesseract."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="image",
            commands=["convert", "resize", "crop", "metadata", "ocr", "to-sticker", "exif-strip", "remove-bg"],
            engine="pillow"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="image")
        def image_group():
            """Image processing tools."""
            pass

        @image_group.command(name="convert")
        @click.argument("input_file", required=False)
        @click.argument("output_file", type=click.Path(), required=False)
        @batch_process
        def convert(input_file: str, output_file: Optional[str]):
            """Convert image format (e.g., photo.jpg photo.png). Supports local or URL."""
            if not output_file and not input_file:
                raise click.UsageError("Missing output_file or --glob pattern.")
            
            if not output_file:
                output_file = f"{Path(input_file).stem}.png"

            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    if output_file.lower().endswith((".jpg", ".jpeg")) and img.mode == "RGBA":
                        img = img.convert("RGB")
                    img.save(output_file)
            console.print(f"[green]✓ Converted {input_file} to {output_file}[/green]")

        @image_group.command(name="resize")
        @click.argument("input_file", required=False)
        @click.option("-w", "--width", type=int, help="Target width")
        @click.option("-h", "--height", type=int, help="Target height")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen without actual resizing")
        @batch_process
        def resize(input_file: str, width: Optional[int], height: Optional[int], output: Optional[str], dry_run: bool):
            """Resize an image. Supports local or URL."""
            if not width and not height:
                console.print("[bold red]Error:[/bold red] Please provide at least width or height.")
                return

            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    original_width, original_height = img.size
                    
                    if width and not height:
                        height = int(original_height * (width / original_width))
                    elif height and not width:
                        width = int(original_width * (height / original_height))
                    
                    out_path = output or f"resized_{Path(path).name}"
                    
                    if dry_run:
                        console.print(f"[bold yellow]Would resize {input_file} to {width}x{height} and save as {out_path}[/bold yellow]")
                        return

                    resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                    resized_img.save(out_path)
                    console.print(f"[green]✓ Resized and saved as {out_path}[/green]")

        @image_group.command(name="crop")
        @click.argument("input_file")
        @click.option("--left", type=int, required=True)
        @click.option("--top", type=int, required=True)
        @click.option("--right", type=int, required=True)
        @click.option("--bottom", type=int, required=True)
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen without actual cropping")
        def crop(input_file: str, left: int, top: int, right: int, bottom: int, output: Optional[str], dry_run: bool):
            """Crop an image (left, top, right, bottom). Supports local or URL."""
            with get_input_path(input_file) as path:
                out_path = output or f"cropped_{Path(path).name}"
                
                if dry_run:
                    console.print(f"[bold yellow]Would crop {input_file} to ({left}, {top}, {right}, {bottom}) and save as {out_path}[/bold yellow]")
                    return

                with Image.open(path) as img:
                    cropped_img = img.crop((left, top, right, bottom))
                    cropped_img.save(out_path)
                console.print(f"[green]✓ Cropped image saved to {out_path}[/green]")

        @image_group.command(name="metadata")
        @click.argument("input_file")
        def metadata(input_file: str):
            """View image EXIF metadata. Supports local or URL."""
            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    exif = img.getexif()
                    if not exif:
                        console.print("[yellow]No EXIF metadata found.[/yellow]")
                    else:
                        from rich.table import Table
                        table = Table(title=f"Metadata for {os.path.basename(path)}")
                        table.add_column("Tag", style="cyan")
                        table.add_column("Value", style="green")
                        
                        for tag_id, value in exif.items():
                            tag = ExifTags.TAGS.get(tag_id, tag_id)
                            table.add_row(str(tag), str(value))
                        console.print(table)

        @image_group.command(name="exif-strip")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def exif_strip(input_file: str, output: Optional[str], dry_run: bool):
            """Remove EXIF metadata from an image. Supports local or URL."""
            with get_input_path(input_file) as path:
                out_path = output or f"stripped_{Path(path).name}"
                
                if dry_run:
                    console.print(f"[bold yellow]Would strip metadata from {input_file} and save as {out_path}[/bold yellow]")
                    return

                with Image.open(path) as img:
                    data = list(img.getdata())
                    img_without_exif = Image.new(img.mode, img.size)
                    img_without_exif.putdata(data)
                    img_without_exif.save(out_path)
                console.print(f"[green]✓ Stripped metadata and saved to {out_path}[/green]")

        @image_group.command(name="ocr")
        @click.argument("input_file")
        @click.option("-l", "--lang", default="eng", help="OCR language (default: eng)")
        @click.option("-o", "--output", type=click.Path(), help="Output text file")
        @click.option("--preprocess", type=click.Choice(['none', 'grayscale', 'threshold']), default='none', help="Image preprocessing")
        @click.option("--scale", type=float, default=1.0, help="Scale factor for the image")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def ocr(input_file: str, lang: str, output: Optional[str], preprocess: str, scale: float, dry_run: bool):
            """Perform OCR on an image. Supports local or URL."""
            tesseract = engine_registry.get("tesseract")
            if not tesseract.is_available:
                console.print("[bold red]Error:[/bold red] Tesseract engine not found. Please install Tesseract-OCR.")
                return

            if dry_run:
                console.print(f"[bold yellow]Would run OCR on {input_file} (lang={lang}, preprocess={preprocess}, scale={scale})[/bold yellow]")
                return

            import pytesseract
            from rich.progress import Progress, SpinnerColumn, TextColumn
            pytesseract.pytesseract.tesseract_cmd = tesseract.path

            with get_input_path(input_file) as path:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as progress:
                    task = progress.add_task(f"Running OCR on {os.path.basename(path)}...", total=None)
                    
                    with Image.open(path) as img:
                        if scale != 1.0:
                            new_size = (int(img.width * scale), int(img.height * scale))
                            img = img.resize(new_size, Image.Resampling.LANCZOS)

                        if preprocess == 'grayscale':
                            img = img.convert("L")
                        elif preprocess == 'threshold':
                            img = img.convert("L").point(lambda x: 0 if x < 128 else 255, '1')

                        text = pytesseract.image_to_string(img, lang=lang)
                        progress.update(task, completed=True)

            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(text)
                console.print(f"[green]✓ OCR text saved to {output}[/green]")
            else:
                console.print(text)

        @image_group.command(name="to-sticker")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename (must be .webp)")
        @click.option("--pack", default="Toolbox Stickers", help="Sticker pack name")
        @click.option("--author", default="Toolbox", help="Sticker author")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def to_sticker(input_file: str, output: Optional[str], pack: str, author: str, dry_run: bool):
            """Convert an image or GIF to a sticker. Supports local or URL."""
            with get_input_path(input_file) as path:
                input_path = Path(path)
                out_path = Path(output) if output else Path(input_file.split("?")[0]).with_suffix(".webp")
                
                if out_path.suffix.lower() != ".webp":
                    out_path = out_path.with_suffix(".webp")

                if dry_run:
                    console.print(f"[bold yellow]Would convert {input_file} to sticker and save as {out_path}[/bold yellow]")
                    return

                with Image.open(path) as img:
                    is_animated = getattr(img, "is_animated", False)
                    
                    def process_frame(frame):
                        frame = frame.convert("RGBA")
                        frame.thumbnail((512, 512), Image.Resampling.LANCZOS)
                        canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
                        x = (512 - frame.width) // 2
                        y = (512 - frame.height) // 2
                        canvas.paste(frame, (x, y))
                        return canvas

                    if is_animated:
                        from rich.progress import track
                        frames = []
                        durations = []
                        for frame in ImageSequence.Iterator(img):
                            frames.append(process_frame(frame))
                            durations.append(img.info.get('duration', 100))
                        
                        frames[0].save(
                            out_path,
                            save_all=True,
                            append_images=frames[1:],
                            duration=durations,
                            loop=0,
                            quality=80,
                            method=6,
                            format="WEBP"
                        )
                    else:
                        sticker = process_frame(img)
                        sticker.save(out_path, quality=80, method=6, format="WEBP")
                
                console.print(f"[green]✓ Sticker created: {out_path} (Pack: {pack}, Author: {author})[/green]")

        @image_group.command(name="remove-bg")
        @click.argument("input_file", required=False)
        @click.option("-o", "--output", help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def remove_bg(input_file: str, output: Optional[str], dry_run: bool):
            """Remove image background using rembg (AI-powered)."""
            from rembg import remove
            
            out_path = output or f"{Path(input_file).stem}_nobg.png"
            
            if dry_run:
                console.print(f"[bold yellow]Would remove background from {input_file} and save as {out_path}[/bold yellow]")
                return

            console.print(f"[cyan]Processing background removal for {input_file}...[/cyan]")
            try:
                with get_input_path(input_file) as path:
                    with Image.open(path) as img:
                        # Convert to RGBA if not already
                        img = img.convert("RGBA")
                        # Remove background
                        result = remove(img)
                        # Save result
                        result.save(out_path)
                console.print(f"[green]✓ Background removed: {out_path}[/green]")
            except Exception as e:
                console.print(f"[bold red]Error removing background:[/bold red] {str(e)}")

