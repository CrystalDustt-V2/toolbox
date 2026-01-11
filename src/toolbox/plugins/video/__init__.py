import click
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry
from toolbox.core.io import get_input_path

class VideoPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="video",
            commands=["trim", "extract-audio", "to-gif", "compress", "to-sticker"],
            engine="ffmpeg"
        )

    def register_commands(self, group):
        @group.group(name="video")
        def video_group():
            """Video processing tools (requires FFmpeg)."""
            pass

        @video_group.command(name="trim")
        @click.argument("input_file")
        @click.option("--start", help="Start time (HH:MM:SS)")
        @click.option("--end", help="End time (HH:MM:SS)")
        @click.option("-o", "--output", type=click.Path(), default="trimmed.mp4")
        def trim(input_file, start, end, output):
            """Trim a video file. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                args = ["-i", path]
                if start:
                    args.extend(["-ss", start])
                if end:
                    args.extend(["-to", end])
                args.extend(["-c", "copy", output])
                
                ffmpeg.run_with_progress(args, label=f"Trimming {os.path.basename(path)}")
            click.echo(f"Trimmed video saved to {output}")

        @video_group.command(name="extract-audio")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), default="audio.mp3")
        def extract_audio(input_file, output):
            """Extract audio from a video file. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                args = ["-i", path, "-q:a", "0", "-map", "a", output]
                ffmpeg.run(args)
            click.echo(f"Extracted audio to {output}")

        @video_group.command(name="to-gif")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), default="output.gif")
        @click.option("-fps", "--fps", type=int, default=10, help="Frames per second")
        @click.option("-w", "--width", type=int, default=480, help="GIF width")
        def to_gif(input_file, output, fps, width):
            """Convert video to GIF. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                # Use a high-quality GIF conversion filter palette
                filter_complex = f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"
                args = ["-i", path, "-filter_complex", filter_complex, output]
                ffmpeg.run_with_progress(args, label=f"Converting {os.path.basename(path)} to GIF")
            click.echo(f"Converted to GIF: {output}")

        @video_group.command(name="compress")
        @click.argument("input_file")
        @click.option("-crf", "--crf", type=int, default=28, help="Constant Rate Factor (lower is better quality, 0-51)")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        def compress(input_file, crf, output):
            """Compress video using H.264. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                out_path = output or f"compressed_{os.path.basename(path)}"
                args = ["-i", path, "-vcodec", "libx264", "-crf", str(crf), out_path]
                ffmpeg.run_with_progress(args, label=f"Compressing {os.path.basename(path)}")
            click.echo(f"Compressed video saved to {out_path}")

        @video_group.command(name="to-sticker")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--fps", type=int, default=15, help="Sticker FPS")
        def to_sticker(input_file, output, fps):
            """Convert a video to a sticker. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                out_path = output or f"{input_file.split('?')[0].rsplit('.', 1)[0]}.webp"
                
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
                
                ffmpeg.run_with_progress(args, label="Generating sticker")
            click.echo(f"Video converted to sticker: {out_path}")
            click.echo("Note: WhatsApp stickers should be < 1MB and usually < 6 seconds.")

        @video_group.command(name="extract-frames")
        @click.argument("input_file")
        @click.option("-i", "--interval", type=float, default=1.0, help="Interval in seconds between frames")
        @click.option("-o", "--output-dir", type=click.Path(), default="frames", help="Output directory")
        @click.option("-f", "--format", type=click.Choice(['jpg', 'png']), default='jpg')
        def extract_frames(input_file, interval, output_dir, format):
            """Extract frames from video at intervals. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                out_path = Path(output_dir)
                out_path.mkdir(parents=True, exist_ok=True)
                
                # ffmpeg -i input.mp4 -vf fps=1/interval out_%03d.jpg
                args = [
                    "-i", path,
                    "-vf", f"fps=1/{interval}",
                    str(out_path / f"frame_%04d.{format}")
                ]
                ffmpeg.run(args)
            click.echo(f"Frames extracted to {output_dir}")
