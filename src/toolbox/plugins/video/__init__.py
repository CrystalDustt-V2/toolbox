import click
import os
from typing import Optional
from pathlib import Path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry, console
from toolbox.core.io import get_input_path
from toolbox.core.utils import batch_process

class VideoPlugin(BasePlugin):
    """Plugin for video processing using FFmpeg."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="video",
            commands=["trim", "extract-audio", "to-gif", "compress", "to-sticker", "extract-frames", "watermark", "remove-watermark"],
            engine="ffmpeg"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="video")
        def video_group():
            """Video processing tools (requires FFmpeg)."""
            pass

        @video_group.command(name="trim")
        @click.argument("input_file")
        @click.option("--start", help="Start time (HH:MM:SS)")
        @click.option("--end", help="End time (HH:MM:SS)")
        @click.option("-o", "--output", type=click.Path(), default="trimmed.mp4")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def trim(input_file: str, start: Optional[str], end: Optional[str], output: str, dry_run: bool):
            """Trim a video file. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                args = ["-i", path]
                if start:
                    args.extend(["-ss", start])
                if end:
                    args.extend(["-to", end])
                args.extend(["-c", "copy", output])
                
                if dry_run:
                    console.print(f"[bold yellow]Would trim {input_file} (start={start}, end={end}) and save as {output}[/bold yellow]")
                    return

                ffmpeg.run_with_progress(args, label=f"Trimming {os.path.basename(path)}")
                console.print(f"[green]✓ Trimmed video saved to {output}[/green]")

        @video_group.command(name="extract-audio")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), default="audio.mp3")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def extract_audio(input_file: str, output: str, dry_run: bool):
            """Extract audio from a video file. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                args = ["-i", path, "-q:a", "0", "-map", "a", output]
                
                if dry_run:
                    console.print(f"[bold yellow]Would extract audio from {input_file} and save as {output}[/bold yellow]")
                    return

                ffmpeg.run_with_progress(args, label=f"Extracting audio from {os.path.basename(path)}")
                console.print(f"[green]✓ Extracted audio to {output}[/green]")

        @video_group.command(name="to-gif")
        @click.argument("input_file", required=False)
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("-fps", "--fps", type=int, default=10, help="Frames per second")
        @click.option("-w", "--width", type=int, default=480, help="GIF width")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def to_gif(input_file: str, output: Optional[str], fps: int, width: int, dry_run: bool):
            """Convert video to GIF. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return
            
            out_path = output or f"{Path(input_file).stem}.gif"

            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[bold yellow]Would convert {input_file} to GIF (fps={fps}, width={width}) and save as {out_path}[/bold yellow]")
                    return

                # Use a high-quality GIF conversion filter palette
                filter_complex = f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
                args = ["-i", path, "-filter_complex", filter_complex, out_path]
                ffmpeg.run_with_progress(args, label=f"Converting {os.path.basename(path)} to GIF")
                console.print(f"[green]✓ Converted to GIF: {out_path}[/green]")

        @video_group.command(name="compress")
        @click.argument("input_file", required=False)
        @click.option("-crf", "--crf", type=int, default=28, help="Constant Rate Factor (lower is better quality, 0-51)")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def compress(input_file: str, crf: int, output: Optional[str], dry_run: bool):
            """Compress video using H.264. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                out_path = output or f"compressed_{os.path.basename(path)}"
                
                if dry_run:
                    console.print(f"[bold yellow]Would compress {input_file} (crf={crf}) and save as {out_path}[/bold yellow]")
                    return

                args = ["-i", path, "-vcodec", "libx264", "-crf", str(crf), out_path]
                ffmpeg.run_with_progress(args, label=f"Compressing {os.path.basename(path)}")
                console.print(f"[green]✓ Compressed video saved to {out_path}[/green]")

        @video_group.command(name="to-sticker")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--fps", type=int, default=15, help="Sticker FPS")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def to_sticker(input_file: str, output: Optional[str], fps: int, dry_run: bool):
            """Convert a video to a sticker. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                out_path = output or f"{input_file.split('?')[0].rsplit('.', 1)[0]}.webp"
                
                if dry_run:
                    console.print(f"[bold yellow]Would convert {input_file} to sticker (fps={fps}) and save as {out_path}[/bold yellow]")
                    return
                
                # WhatsApp sticker filter: 
                # 1. Resize to fit 512x512 while maintaining aspect ratio
                # 2. Pad to exactly 512x512 with transparent background
                # 3. Set FPS
                filter_str = f"scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2:color=#00000000,fps={fps}"
                
                args = [
                    "-i", path,
                    "-vf", filter_str,
                    "-loop", "0",
                    "-vcodec", "libwebp",
                    "-lossless", "0",
                    "-compression_level", "6",
                    "-q:v", "50",
                    out_path
                ]
                
                ffmpeg.run_with_progress(args, label=f"Converting {os.path.basename(path)} to sticker")
                console.print(f"[green]✓ Video converted to sticker: {out_path}[/green]")
                console.print("[yellow]Note: WhatsApp stickers should be < 1MB and usually < 6 seconds.[/yellow]")

        @video_group.command(name="extract-frames")
        @click.argument("input_file")
        @click.option("-i", "--interval", type=float, default=1.0, help="Interval in seconds between frames")
        @click.option("-o", "--output-dir", type=click.Path(), default="frames", help="Output directory")
        @click.option("-f", "--format", type=click.Choice(['jpg', 'png']), default='jpg')
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def extract_frames(input_file: str, interval: float, output_dir: str, format: str, dry_run: bool):
            """Extract frames from video at intervals. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                out_dir = Path(output_dir)
                
                if dry_run:
                    console.print(f"[bold yellow]Would extract frames from {input_file} (interval={interval}, format={format}) to {output_dir}[/bold yellow]")
                    return

                out_dir.mkdir(parents=True, exist_ok=True)
                
                args = [
                    "-i", path,
                    "-vf", f"fps=1/{interval}",
                    str(out_dir / f"frame_%04d.{format}")
                ]
                ffmpeg.run_with_progress(args, label=f"Extracting frames from {os.path.basename(path)}")
                console.print(f"[green]✓ Frames extracted to {output_dir}[/green]")

        @video_group.command(name="watermark")
        @click.argument("input_file")
        @click.option("-t", "--text", help="Text watermark to add")
        @click.option("-i", "--image", type=click.Path(exists=True), help="Image watermark to add")
        @click.option("-o", "--output", default="watermarked.mp4", help="Output filename")
        @click.option("--pos", default="bottom-right", type=click.Choice(['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']), help="Watermark position")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def watermark(input_file: str, text: Optional[str], image: Optional[str], output: str, pos: str, dry_run: bool):
            """Add text or image watermark to a video."""
            if not text and not image:
                console.print("[bold red]Error:[/bold red] Either --text or --image must be provided.")
                return

            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found.")
                return

            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[bold yellow]Would add watermark to {input_file} at {pos} and save as {output}[/bold yellow]")
                    return

                # Map positions to FFmpeg overlay/drawtext coordinates
                pos_map = {
                    'top-left': "10:10",
                    'top-right': "main_w-overlay_w-10:10",
                    'bottom-left': "10:main_h-overlay_h-10",
                    'bottom-right': "main_w-overlay_w-10:main_h-overlay_h-10",
                    'center': "(main_w-overlay_w)/2:(main_h-overlay_h)/2"
                }
                
                text_pos_map = {
                    'top-left': "x=10:y=10",
                    'top-right': "x=w-tw-10:y=10",
                    'bottom-left': "x=10:y=h-th-10",
                    'bottom-right': "x=w-tw-10:y=h-th-10",
                    'center': "x=(w-tw)/2:y=(h-th)/2"
                }

                if image:
                    args = [
                        "-i", path,
                        "-i", image,
                        "-filter_complex", f"overlay={pos_map[pos]}",
                        "-codec:a", "copy",
                        output
                    ]
                else:
                    # Basic drawtext filter
                    args = [
                        "-i", path,
                        "-vf", f"drawtext=text='{text}':{text_pos_map[pos]}:fontsize=24:fontcolor=white@0.8:shadowcolor=black:shadowx=2:shadowy=2",
                        "-codec:a", "copy",
                        output
                    ]

                ffmpeg.run_with_progress(args, label=f"Adding watermark to {os.path.basename(path)}")
                console.print(f"[green]✓ Watermark added: {output}[/green]")

        @video_group.command(name="remove-watermark")
        @click.argument("input_file")
        @click.option("-x", type=int, required=True, help="X coordinate of the watermark")
        @click.option("-y", type=int, required=True, help="Y coordinate of the watermark")
        @click.option("-w", "--width", type=int, required=True, help="Width of the watermark")
        @click.option("-h", "--height", type=int, required=True, help="Height of the watermark")
        @click.option("-o", "--output", default="cleaned.mp4", help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def remove_watermark(input_file: str, x: int, y: int, width: int, height: int, output: str, dry_run: bool):
            """Remove a watermark from a specific area using the delogo filter."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found.")
                return

            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[bold yellow]Would remove watermark from {input_file} at ({x},{y}) size {width}x{height} and save as {output}[/bold yellow]")
                    return

                # delogo filter: x:y:w:h
                args = [
                    "-i", path,
                    "-vf", f"delogo=x={x}:y={y}:w={width}:h={height}",
                    "-codec:a", "copy",
                    output
                ]

                ffmpeg.run_with_progress(args, label=f"Removing watermark from {os.path.basename(path)}")
                console.print(f"[green]✓ Watermark removed (blurred): {output}[/green]")
                console.print("[yellow]Note: Watermark removal uses a blur/interpolation effect on the specified area.[/yellow]")
