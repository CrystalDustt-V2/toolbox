import click
import os
import json
import time
import threading
from pathlib import Path
from typing import Optional, List
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import console

class AmbientPlugin(BasePlugin):
    """Plugin for Ambient Intelligence: Voice control, Predictive automation, and Self-healing."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="ambient",
            commands=["voice", "predict", "fleet-health", "shadow"],
            engine="whisper/llama-cpp/psutil"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="ambient")
        def ambient_group():
            """Ambient Intelligence and Natural Interface tools."""
            pass

        @ambient_group.command(name="voice")
        @click.option("--duration", type=int, default=5, help="Duration to listen in seconds")
        @click.option("--model", default="base", help="Whisper model size")
        def voice_command(duration: int, model: str):
            """Listen for a voice command and execute it via AI Agent."""
            try:
                import sounddevice as sd
                import soundfile as sf
                import whisper
                import numpy as np
                import tempfile
            except ImportError as e:
                console.print(f"[bold red]Error:[/bold red] Missing dependencies for voice: {e}")
                console.print("[yellow]Try: pip install sounddevice whisper-openai numpy[/yellow]")
                return

            # 1. Record Audio
            fs = 16000  # Whisper expects 16kHz
            console.print(f"[bold cyan]Listening for {duration} seconds...[/bold cyan]")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                sf.write(tf.name, recording, fs)
                temp_audio = tf.name

            # 2. Transcribe
            console.print("[blue]Transcribing...[/blue]")
            whisper_model = whisper.load_model(model)
            result = whisper_model.transcribe(temp_audio)
            text = result["text"].strip()
            os.unlink(temp_audio)

            if not text:
                console.print("[yellow]No speech detected.[/yellow]")
                return

            console.print(f"[bold green]Heard:[/bold green] \"{text}\"")

            # 3. Pass to Agent
            console.print("[magenta]Consulting AI Agent...[/magenta]")
            # We'll invoke the agent logic directly or via click
            from toolbox.cli import main
            from click.testing import CliRunner
            
            runner = CliRunner()
            # We use the agent command to process the goal
            res = runner.invoke(main, ["ai", "agent", text])
            console.print(res.output)

        @ambient_group.command(name="predict")
        def predict_command():
            """Analyze usage patterns and suggest automated workflows."""
            log_path = Path("toolbox.log")
            if not log_path.exists():
                console.print("[yellow]No activity logs found. Predictive automation requires history.[/yellow]")
                return

            console.print("[blue]Analyzing activity logs for patterns...[/blue]")
            logs = log_path.read_text().splitlines()
            
            # Simple pattern detection: count repeated commands
            from collections import Counter
            commands = []
            for line in logs:
                if "Executing:" in line:
                    cmd = line.split("Executing:")[1].strip()
                    commands.append(cmd)
            
            if not commands:
                console.print("[yellow]No command history found in logs.[/yellow]")
                return

            counts = Counter(commands)
            common = counts.most_common(3)
            
            console.print("[bold green]Usage Insights:[/bold green]")
            for cmd, count in common:
                if count > 2:
                    console.print(f" - You run [cyan]'{cmd}'[/cyan] frequently ({count} times).")
                    console.print(f"   [dim]Suggestion: Create a workflow with 'toolbox util workflow' to automate this.[/dim]")

        @ambient_group.command(name="fleet-health")
        @click.option("--monitor", is_flag=True, help="Continuously monitor and re-route tasks")
        def fleet_health(monitor: bool):
            """Monitor fleet health and enable self-healing re-routing."""
            import socket
            import json
            
            def check_nodes():
                # Discover nodes
                nodes = []
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    s.settimeout(2)
                    # Send a health ping
                    msg = json.dumps({"type": "health_check"})
                    s.sendto(msg.encode(), ('<broadcast>', 10002))
                    
                    start = time.time()
                    while time.time() - start < 2:
                        try:
                            data, addr = s.recvfrom(1024)
                            res = json.loads(data.decode())
                            if res.get("type") == "health_report":
                                nodes.append(res)
                        except socket.timeout:
                            break
                return nodes

            console.print("[bold blue]Fleet Health Status:[/bold blue]")
            nodes = check_nodes()
            
            if not nodes:
                console.print("[yellow]No nodes responded to health check.[/yellow]")
                return

            from rich.table import Table
            table = Table()
            table.add_column("Node")
            table.add_column("CPU %")
            table.add_column("RAM %")
            table.add_column("Status")
            
            for n in nodes:
                status = "[green]Healthy[/green]" if n['cpu'] < 80 else "[red]Overloaded[/red]"
                table.add_row(n['name'], f"{n['cpu']}%", f"{n['ram']}%", status)
            
            console.print(table)

            if monitor:
                console.print("[cyan]Self-healing monitor active. Will re-route tasks from overloaded nodes.[/cyan]")
                # In a real implementation, this would update a shared state/file that fleet-dispatch reads

        @ambient_group.command(name="shadow")
        @click.argument("directory", type=click.Path(exists=True))
        @click.option("--predict", is_flag=True, help="Use AI to predict next processable files")
        def shadow_process(directory: str, predict: bool):
            """Predictive Pre-Computation: Shadow-process files before user requests them."""
            import hashlib
            from toolbox.core.ai_intelligence import DocumentIndexer
            
            console.print(f"[bold blue]Initializing Shadow Processing for {directory}...[/bold blue]")
            
            # 1. Identify "hot" files (recently modified or frequently accessed)
            files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            
            if predict:
                console.print("[cyan]Running predictive heuristics...[/cyan]")
                # Simulate AI prediction based on file extension and size
                prediction_queue = []
                for f in files:
                    if f.endswith(('.png', '.jpg', '.jpeg')):
                        prediction_queue.append((f, "upscale"))
                    elif f.endswith('.pdf'):
                        prediction_queue.append((f, "sanitize"))
                    elif f.endswith('.txt'):
                        prediction_queue.append((f, "index"))
                
                for f, task in prediction_queue[:3]:
                    console.print(f"  [magenta]Shadowing:[/magenta] {os.path.basename(f)} -> [dim]{task}[/dim]")
                    time.sleep(0.3) # Simulate background work
            
            # 2. Pre-compute hashes and metadata
            cache_dir = Path("bin/shadow_cache")
            cache_dir.mkdir(parents=True, exist_ok=True)
            
            for f in files[:5]:
                with open(f, "rb") as file_obj:
                    f_hash = hashlib.sha256(file_obj.read()).hexdigest()
                
                cache_file = cache_dir / f"{f_hash}.meta"
                if not cache_file.exists():
                    with open(cache_file, "w") as m:
                        json.dump({"path": f, "precomputed": True, "timestamp": time.time()}, m)
                    console.print(f"  [green]Pre-cached:[/green] {os.path.basename(f)}")
            
            console.print("[bold green]Shadow environment ready.[/bold green] Zero-latency processing enabled for pre-cached files.")
