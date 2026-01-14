import click
import os
import contextlib
from typing import Optional, List
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import engine_registry, console
from toolbox.core.io import get_input_path

class AudioPlugin(BasePlugin):
    """Plugin for audio processing using FFmpeg and Whisper."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="audio",
            commands=["convert", "trim", "merge", "normalize", "stt"],
            engine="ffmpeg/whisper"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="audio")
        def audio_group():
            """Audio processing tools (requires FFmpeg)."""
            pass

        @audio_group.command(name="stt")
        @click.argument("input_file")
        @click.option("-m", "--model", default="base", help="Whisper model size (tiny, base, small, medium, large)")
        @click.option("-o", "--output", type=click.Path(), help="Output text file")
        @click.option("--gpu", is_flag=True, help="Use GPU for inference")
        def stt(input_file: str, model: str, output: Optional[str], gpu: bool):
            """Transcribe audio to text using OpenAI Whisper."""
            try:
                import whisper
                import torch
            except ModuleNotFoundError:
                console.print("[bold red]Error:[/bold red] Speech-to-text dependencies are missing.")
                console.print("Install with: pip install 'toolbox-universal[ai]'")
                return
            
            device = "cuda" if (gpu or torch.cuda.is_available()) else "cpu"
            console.print(f"[blue]Loading Whisper model '{model}' on {device}...[/blue]")
            
            try:
                model_instance = whisper.load_model(model, device=device)
            except Exception as e:
                console.print(f"[bold red]Error loading model:[/bold red] {e}")
                return

            with get_input_path(input_file) as path:
                console.print(f"[blue]Transcribing {input_file}...[/blue]")
                result = model_instance.transcribe(str(path))
                
                text = result["text"].strip()
                out_path = output or f"{Path(path).stem}.txt"
                
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(text)
                
                console.print(f"[green]✓ Transcription saved to {out_path}[/green]")
                console.print(f"\n[bold]Preview:[/bold]\n{text[:200]}...")

        @audio_group.command(name="convert")
        @click.argument("input_file")
        @click.argument("output_file", type=click.Path())
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def convert(input_file: str, output_file: str, dry_run: bool):
            """Convert audio format (e.g., audio.wav audio.mp3). Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[bold yellow]Would convert {input_file} to {output_file}[/bold yellow]")
                    return

                args = ["-i", path, output_file]
                ffmpeg.run_with_progress(args, label=f"Converting {os.path.basename(path)}")
                console.print(f"[green]✓ Converted {input_file} to {output_file}[/green]")

        @audio_group.command(name="trim")
        @click.argument("input_file")
        @click.option("--start", help="Start time (HH:MM:SS or seconds)")
        @click.option("--end", help="End time (HH:MM:SS or seconds)")
        @click.option("-o", "--output", type=click.Path(), default="trimmed.mp3")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def trim(input_file: str, start: Optional[str], end: Optional[str], output: str, dry_run: bool):
            """Trim an audio file. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                if dry_run:
                    console.print(f"[bold yellow]Would trim {input_file} (start={start}, end={end}) and save as {output}[/bold yellow]")
                    return

                args = ["-i", path]
                if start:
                    args.extend(["-ss", start])
                if end:
                    args.extend(["-to", end])
                args.extend(["-c", "copy", output])
                
                ffmpeg.run(args)
                console.print(f"[green]✓ Trimmed audio saved to {output}[/green]")

        @audio_group.command(name="merge")
        @click.argument("input_files", nargs=-1, required=True)
        @click.option("-o", "--output", type=click.Path(), default="merged.mp3")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def merge(input_files: List[str], output: str, dry_run: bool):
            """Merge multiple audio files into one. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return
            
            if dry_run:
                console.print(f"[bold yellow]Would merge {len(input_files)} files into {output}[/bold yellow]")
                return

            with contextlib.ExitStack() as stack:
                paths = [stack.enter_context(get_input_path(f)) for f in input_files]
                
                # FFmpeg concat filter for multiple inputs
                filter_str = "".join([f"[{i}:a]" for i in range(len(paths))]) + f"concat=n={len(paths)}:v=0:a=1[a]"
                args = []
                for p in paths:
                    args.extend(["-i", p])
                args.extend(["-filter_complex", filter_str, "-map", "[a]", output])
                
                ffmpeg.run_with_progress(args, label=f"Merging {len(input_files)} files")
            
            console.print(f"[green]✓ Merged {len(input_files)} files into {output}[/green]")

        @audio_group.command(name="normalize")
        @click.argument("input_file")
        @click.option("-o", "--output", type=click.Path(), help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def normalize(input_file: str, output: Optional[str], dry_run: bool):
            """Normalize audio volume using loudnorm filter. Supports local or URL."""
            ffmpeg = engine_registry.get("ffmpeg")
            if not ffmpeg.is_available:
                console.print("[bold red]Error:[/bold red] FFmpeg engine not found. Please install FFmpeg.")
                return

            with get_input_path(input_file) as path:
                out_path = output or f"normalized_{os.path.basename(path)}"
                
                if dry_run:
                    console.print(f"[bold yellow]Would normalize {input_file} and save as {out_path}[/bold yellow]")
                    return

                args = ["-i", path, "-af", "loudnorm", out_path]
                ffmpeg.run(args)
                console.print(f"[green]✓ Normalized audio saved to {out_path}[/green]")
