import click
import pytesseract
from pathlib import Path
from PIL import Image, ExifTags, ImageSequence, ImageOps
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry, console
from toolbox.core.io import get_input_path

class ImagePlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="image",
            commands=["convert", "resize", "crop", "metadata", "ocr", "to-sticker"],
            engine="pillow"
        )

    def register_commands(self, group):
        @group.group(name="image")
        def image_group():
            """Image processing tools."""
            pass

        @image_group.command(name="convert")
        @click.argument("input_file")
        @click.argument("output_file", type=click.Path())
        def convert(input_file, output_file):
            """Convert image format (e.g., photo.jpg photo.png). Supports local or URL."""
            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    if output_file.lower().endswith((".jpg", ".jpeg")) and img.mode == "RGBA":
                        img = img.convert("RGB")
                    img.save(output_file)
            click.echo(f"Converted {input_file} to {output_file}")

        @image_group.command(name="resize")
        @click.argument("input_file")
        @click.option("-w", "--width", type=int, help="Target width")
        @click.option("-h", "--height", type=int, help="Target height")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        def resize(input_file, width, height, output):
            """Resize an image. Supports local or URL."""
            if not width and not height:
                click.echo("Please provide at least width or height.")
                return

            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    original_width, original_height = img.size
                    
                    if width and not height:
                        height = int(original_height * (width / original_width))
                    elif height and not width:
                        width = int(original_width * (height / original_height))
                    
                    resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                    
                    out_path = output or f"resized_{Path(path).name}"
                    resized_img.save(out_path)
            
            click.echo(f"Resized and saved as {out_path}")

        @image_group.command(name="crop")
        @click.argument("input_file")
        @click.option("--left", type=int, required=True)
        @click.option("--top", type=int, required=True)
        @click.option("--right", type=int, required=True)
        @click.option("--bottom", type=int, required=True)
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        def crop(input_file, left, top, right, bottom, output):
            """Crop an image (left, top, right, bottom). Supports local or URL."""
            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    cropped_img = img.crop((left, top, right, bottom))
                    out_path = output or f"cropped_{Path(path).name}"
                    cropped_img.save(out_path)
            click.echo(f"Cropped image saved to {out_path}")

        @image_group.command(name="metadata")
        @click.argument("input_file")
        def metadata(input_file):
            """View image EXIF metadata. Supports local or URL."""
            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    exif = img.getexif()
                    if not exif:
                        click.echo("No EXIF metadata found.")
                    else:
                        for tag_id, value in exif.items():
                            tag = ExifTags.TAGS.get(tag_id, tag_id)
                            click.echo(f"{tag}: {value}")

        @image_group.command(name="exif-strip")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        def exif_strip(input_file, output):
            """Remove EXIF metadata from an image. Supports local or URL."""
            with get_input_path(input_file) as path:
                with Image.open(path) as img:
                    data = list(img.getdata())
                    img_without_exif = Image.new(img.mode, img.size)
                    img_without_exif.putdata(data)
                    
                    out_path = output or f"stripped_{Path(path).name}"
                    img_without_exif.save(out_path)
                    click.echo(f"Stripped metadata and saved to {out_path}")

        @image_group.command(name="ocr")
        @click.argument("input_file")
        @click.option("-l", "--lang", default="eng", help="OCR language (default: eng)")
        @click.option("-o", "--output", type=click.Path(), help="Output text file")
        @click.option("--preprocess", type=click.Choice(['none', 'grayscale', 'threshold']), default='none', help="Image preprocessing")
        @click.option("--scale", type=float, default=1.0, help="Scale factor for the image")
        def ocr(input_file, lang, output, preprocess, scale):
            """Perform OCR on an image. Supports local or URL."""
            tesseract = engine_registry.get("tesseract")
            if not tesseract.is_available:
                click.echo("Error: Tesseract engine not found. Please install Tesseract-OCR.")
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
                click.echo(f"OCR text saved to {output}")
            else:
                click.echo(text)

        @image_group.command(name="to-sticker")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename (must be .webp)")
        @click.option("--pack", default="Toolbox Stickers", help="Sticker pack name")
        @click.option("--author", default="Toolbox", help="Sticker author")
        def to_sticker(input_file, output, pack, author):
            """Convert an image or GIF to a sticker. Supports local or URL."""
            with get_input_path(input_file) as path:
                input_path = Path(path)
                out_path = Path(output) if output else Path(input_file.split("?")[0]).with_suffix(".webp")
                
                if out_path.suffix.lower() != ".webp":
                    out_path = out_path.with_suffix(".webp")

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

                    # Note: Full WhatsApp sticker metadata requires a specific EXIF format (webpmux)
                    # For now, we save basic WebP. Advanced metadata usually requires external tools like webpmux.
                    if is_animated:
                        frames = []
                        for frame in ImageSequence.Iterator(img):
                            frames.append(process_frame(frame))
                        
                        frames[0].save(
                            out_path,
                            save_all=True,
                            append_images=frames[1:],
                            format="WEBP",
                            loop=0,
                            duration=img.info.get("duration", 100),
                            lossless=False,
                            quality=80
                        )
                    else:
                        sticker = process_frame(img)
                        sticker.save(out_path, format="WEBP", lossless=False, quality=80)

            click.echo(f"Sticker created: {out_path} (Pack: {pack}, Author: {author})")
