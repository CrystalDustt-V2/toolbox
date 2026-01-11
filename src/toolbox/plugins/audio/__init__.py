import click
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry
from toolbox.core.io import get_input_path

class AudioPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="audio",
            commands=["convert", "trim", "merge"],
            engine="ffmpeg"
        )

    def register_commands(self, group):
        @group.group(name="audio")
        def audio_group():
            """Audio processing tools (requires FFmpeg)."""
            pass

        @audio_group.command(name="convert")
        @click.argument("input_file")
        @click.argument("output_file", type=click.Path())
        def convert(input_file, output_file):
            """Convert audio format (e.g., audio.wav audio.mp3). Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                args = ["-i", path, output_file]
                ffmpeg.run(args)
            click.echo(f"Converted {input_file} to {output_file}")

        @audio_group.command(name="trim")
        @click.argument("input_file")
        @click.option("--start", help="Start time (HH:MM:SS or seconds)")
        @click.option("--end", help="End time (HH:MM:SS or seconds)")
        @click.option("-o", "--output", type=click.Path(), default="trimmed.mp3")
        def trim(input_file, start, end, output):
            """Trim an audio file. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                args = ["-i", path]
                if start:
                    args.extend(["-ss", start])
                if end:
                    args.extend(["-to", end])
                args.extend(["-c", "copy", output])
                
                ffmpeg.run(args)
            click.echo(f"Trimmed audio saved to {output}")

        @audio_group.command(name="merge")
        @click.argument("input_files", nargs=-1, required=True)
        @click.option("-o", "--output", type=click.Path(), default="merged.mp3")
        def merge(input_files, output):
            """Merge multiple audio files into one. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            
            import contextlib
            
            with contextlib.ExitStack() as stack:
                paths = [stack.enter_context(get_input_path(f)) for f in input_files]
                
                # FFmpeg concat filter for multiple inputs
                filter_str = "".join([f"[{i}:a]" for i in range(len(paths))]) + f"concat=n={len(paths)}:v=0:a=1[a]"
                args = []
                for p in paths:
                    args.extend(["-i", p])
                args.extend(["-filter_complex", filter_str, "-map", "[a]", output])
                
                ffmpeg.run(args)
            
            click.echo(f"Merged {len(input_files)} files into {output}")

        @audio_group.command(name="normalize")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        def normalize(input_file, output):
            """Normalize audio volume using loudnorm filter. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            with get_input_path(input_file) as path:
                import os
                out_path = output or f"normalized_{os.path.basename(path)}"
                args = ["-i", path, "-af", "loudnorm", out_path]
                ffmpeg.run(args)
            click.echo(f"Normalized audio saved to {out_path}")
