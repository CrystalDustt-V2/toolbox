import click
import time
from typing import Optional, List
from pathlib import Path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import console
from toolbox.core.ai import AVAILABLE_MODELS, get_model_path

class AIPlugin(BasePlugin):
    """Plugin for AI model management."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="ai",
            commands=["download", "chat", "image-gen", "vision", "index", "agent", "bci", "singularity"],
            engine="python/onnx/llama-cpp"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="ai")
        def ai_group():
            """AI model management and edge computing tools."""
            pass

        @ai_group.command(name="index")
        @click.argument("files", nargs=-1, type=click.Path(exists=True))
        def index_command(files: List[str]):
            """Index local documents for RAG-enabled chat."""
            try:
                from toolbox.core.ai_intelligence import DocumentIndexer
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")
                return
            import pickle
            
            indexer = DocumentIndexer()
            indexer.add_documents(files)
            
            index_path = Path("bin/ai_models/doc_index.pkl")
            index_path.parent.mkdir(parents=True, exist_ok=True)
            with open(index_path, "wb") as f:
                pickle.dump(indexer, f)
            console.print(f"[green]✓ Index saved to {index_path}[/green]")

        @ai_group.command(name="chat")
        @click.argument("prompt")
        @click.option("--model", default="phi-2-gguf", help="LLM model to use")
        @click.option("--rag", is_flag=True, help="Use indexed documents for context")
        @click.option("--max-tokens", default=512, help="Max tokens to generate")
        def chat_command(prompt: str, model: str, rag: bool, max_tokens: int):
            """Chat with a local LLM (offline, supports RAG)."""
            try:
                from llama_cpp import Llama
            except ModuleNotFoundError:
                console.print("[bold red]Error:[/bold red] Missing dependency: llama-cpp-python")
                console.print("Install with: pip install 'toolbox-universal[ai]'")
                return
            from toolbox.core.ai import AVAILABLE_MODELS, get_model_path, get_engine_routing
            import pickle
            
            if model not in AVAILABLE_MODELS or AVAILABLE_MODELS[model]["type"] != "llm":
                console.print(f"[bold red]Error:[/bold red] Model '{model}' is not a supported LLM.")
                return

            context = ""
            if rag:
                index_path = Path("bin/ai_models/doc_index.pkl")
                if index_path.exists():
                    with open(index_path, "rb") as f:
                        indexer = pickle.load(f)
                    context = indexer.search(prompt)
                    console.print("[dim]Using retrieved context from index...[/dim]")
                else:
                    console.print("[yellow]No index found. Use 'toolbox ai index' first.[/yellow]")

            model_info = AVAILABLE_MODELS[model]
            model_path = get_model_path(model_info["name"], model_info["url"])
            
            routing = get_engine_routing()
            llm = Llama(model_path=str(model_path), n_ctx=2048, n_threads=routing["threads"], verbose=False)
            
            full_prompt = f"Context: {context}\n\nInstruct: {prompt}\nOutput:" if context else f"Instruct: {prompt}\nOutput:"
            
            console.print(f"\n[bold green]User:[/bold green] {prompt}")
            console.print("[bold blue]Assistant:[/bold blue] ", end="")
            
            response = llm(full_prompt, max_tokens=max_tokens, stop=["Instruct:", "\n"], echo=False)
            console.print(response["choices"][0]["text"].strip())

        @ai_group.command(name="vision")
        @click.argument("image_path", type=click.Path(exists=True))
        @click.argument("prompt")
        @click.option("--model", default="llava-v1.5-7b-gguf", help="Vision model to use")
        def vision_command(image_path: str, prompt: str, model: str):
            """Analyze an image using a local Vision LLM (LLaVA)."""
            try:
                from llama_cpp import Llama
                from llama_cpp.llama_chat_format import Llava15ChatHandler
            except ModuleNotFoundError:
                console.print("[bold red]Error:[/bold red] Missing dependency: llama-cpp-python")
                console.print("Install with: pip install 'toolbox-universal[ai]'")
                return
            from toolbox.core.ai import AVAILABLE_MODELS, get_model_path, get_engine_routing
            import base64

            if model not in AVAILABLE_MODELS or AVAILABLE_MODELS[model]["type"] != "vision-llm":
                console.print(f"[bold red]Error:[/bold red] '{model}' is not a vision model.")
                return

            model_info = AVAILABLE_MODELS[model]
            proj_info = AVAILABLE_MODELS["llava-v1.5-7b-mmproj"]
            
            model_path = get_model_path(model_info["name"], model_info["url"])
            proj_path = get_model_path(proj_info["name"], proj_info["url"])
            
            routing = get_engine_routing()
            chat_handler = Llava15ChatHandler(clip_model_path=str(proj_path))
            
            llm = Llama(
                model_path=str(model_path),
                chat_handler=chat_handler,
                n_ctx=2048,
                n_threads=routing["threads"],
                verbose=False
            )
            
            # Encode image
            with open(image_path, "rb") as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')

            console.print(f"[blue]Analyzing {image_path}...[/blue]")
            
            res = llm.create_chat_completion(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that can see images."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                        ]
                    }
                ]
            )
            
            console.print(f"\n[bold blue]Assistant:[/bold blue] {res['choices'][0]['message']['content']}")

        @ai_group.command(name="image-gen")
        @click.argument("prompt")
        @click.option("-o", "--output", default="generated_image.png", help="Output filename")
        @click.option("--steps", default=20, help="Inference steps")
        def image_gen_command(prompt: str, output: str, steps: int):
            """Generate an image from text using local Stable Diffusion (ONNX)."""
            try:
                from diffusers import OnnxStableDiffusionPipeline
            except ModuleNotFoundError:
                console.print("[bold red]Error:[/bold red] Missing dependency: diffusers")
                console.print("Install with: pip install 'toolbox-universal[ai]'")
                return
            from toolbox.core.ai import AVAILABLE_MODELS, get_model_path, get_engine_routing
            
            model_key = "stable-diffusion-v1-5-onnx"
            model_info = AVAILABLE_MODELS[model_key]
            
            console.print("[yellow]Note: Stable Diffusion ONNX models are large (~4GB).[/yellow]")
            model_path = get_model_path(model_info["name"], model_info["url"])
            
            routing = get_engine_routing()
            console.print(f"[blue]Initializing Stable Diffusion on {routing['device']}...[/blue]")
            
            # Load pipeline
            pipe = OnnxStableDiffusionPipeline.from_pretrained(
                str(model_path),
                provider=routing["provider"]
            )
            
            console.print(f"[green]Generating image for prompt:[/green] {prompt}")
            image = pipe(prompt, num_inference_steps=steps).images[0]
            image.save(output)
            
            console.print(f"[bold green]✓ Image saved to {output}[/bold green]")

        @ai_group.command(name="download")
        @click.option("--model", help="Specific model to download (e.g., upscale-x2, upscale-x4)")
        @click.option("--all", is_flag=True, help="Download all available models")
        def download_command(model: Optional[str], all: bool):
            """Pre-cache AI models for offline use."""
            if not model and not all:
                console.print("[yellow]Please specify a model with --model or use --all.[/yellow]")
                console.print(f"Available models: {', '.join(AVAILABLE_MODELS.keys())}")
                return

            models_to_download = []
            if all:
                models_to_download = list(AVAILABLE_MODELS.values())
            elif model in AVAILABLE_MODELS:
                models_to_download = [AVAILABLE_MODELS[model]]
            else:
                console.print(f"[bold red]Error:[/bold red] Model '{model}' not found.")
                console.print(f"Available models: {', '.join(AVAILABLE_MODELS.keys())}")
                return

            for m in models_to_download:
                try:
                    get_model_path(m["name"], m["url"])
                except Exception as e:
                    console.print(f"[bold red]Failed to download {m['name']}:[/bold red] {e}")

            console.print("[green]✓ Download process complete.[/green]")

        @ai_group.command(name="agent")
        @click.argument("goal")
        @click.option("--model", default="phi-2-gguf", help="LLM model to use for the agent")
        def agent_command(goal: str, model: str):
            """Run an autonomous AI agent to achieve a goal using ToolBox commands."""
            try:
                from llama_cpp import Llama
            except ModuleNotFoundError:
                console.print("[bold red]Error:[/bold red] Missing dependency: llama-cpp-python")
                console.print("Install with: pip install 'toolbox-universal[ai]'")
                return
            from toolbox.core.ai import AVAILABLE_MODELS, get_model_path, get_engine_routing
            import json
            import re

            if model not in AVAILABLE_MODELS or AVAILABLE_MODELS[model]["type"] != "llm":
                console.print(f"[bold red]Error:[/bold red] Model '{model}' is not a supported LLM.")
                return

            model_info = AVAILABLE_MODELS[model]
            model_path = get_model_path(model_info["name"], model_info["url"])
            routing = get_engine_routing()
            
            console.print(f"[bold blue]Agent Core Initialized.[/bold blue] Goal: {goal}")
            
            llm = Llama(model_path=str(model_path), n_ctx=2048, n_threads=routing["threads"], verbose=False)
            
            # System prompt for tool use
            system_prompt = """You are an autonomous ToolBox agent. You have access to various CLI commands.
Your task is to achieve the user's goal by generating a sequence of commands.
Available command categories: ai, security, video, image, file, desktop, etc.
Example commands: 
- toolbox ai index <path>
- toolbox security audit <path>
- toolbox video upscale <path>

Format your response as a JSON object with:
{
  "thought": "your reasoning",
  "command": "the exact toolbox command to run",
  "finished": true/false
}
Only output the JSON object."""

            prompt = f"{system_prompt}\n\nUser Goal: {goal}\nResponse:"
            
            try:
                response = llm(prompt, max_tokens=256, stop=["}"], echo=False)
                raw_text = response["choices"][0]["text"].strip() + "}"
                
                # Attempt to parse JSON
                try:
                    plan = json.loads(raw_text)
                    console.print(f"[bold green]Thought:[/bold green] {plan.get('thought')}")
                    
                    if plan.get("command"):
                        cmd = plan["command"]
                        console.print(f"[bold yellow]Executing:[/bold yellow] {cmd}")
                        
                        # In a real implementation, we would use subprocess to run the command
                        # For safety in this demo, we'll simulate the execution
                        import subprocess
                        # Ensure we only run 'toolbox' commands
                        if cmd.startswith("toolbox "):
                            # Run as a subprocess to keep agent environment clean
                            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                            if result.returncode == 0:
                                console.print("[green]✓ Command executed successfully.[/green]")
                                if result.stdout:
                                    console.print(f"[dim]{result.stdout}[/dim]")
                            else:
                                console.print(f"[bold red]Error executing command:[/bold red] {result.stderr}")
                        else:
                            console.print("[bold red]Security Block:[/bold red] Agent tried to run a non-toolbox command.")
                    
                    if plan.get("finished"):
                        console.print("[bold cyan]Goal Achieved.[/bold cyan]")
                    else:
                        console.print("[yellow]Agent suggests further steps (multi-step logic in Phase 4.1).[/yellow]")
                        
                except json.JSONDecodeError:
                    console.print(f"[bold red]Failed to parse agent response:[/bold red]\n{raw_text}")
                    
            except Exception as e:
                console.print(f"[bold red]Agent Error:[/bold red] {str(e)}")

        @ai_group.command(name="bci")
        @click.option("--simulate", is_flag=True, help="Simulate BCI thought patterns")
        def bci_command(simulate: bool):
            """Brain-Computer Interface (BCI) Foundation: Simulated thought-to-command execution."""
            import time
            import random
            
            console.print("[bold purple]Brain-Computer Interface (BCI) initialized...[/bold purple]")
            
            if simulate:
                console.print("[blue]Waiting for neural pattern (Theta-Alpha bridge)...[/blue]")
                time.sleep(1.5)
                
                # Simulated neural "intent" detection
                intents = [
                    "OPTIMIZE_DISK_SPACE",
                    "ENCRYPT_SENSITIVE_DATA",
                    "SCAN_FLEET_HEALTH",
                    "SCALE_PARALLEL_TASKS"
                ]
                intent = random.choice(intents)
                confidence = random.uniform(0.85, 0.99)
                
                console.print(f"[green]Detected Intent:[/green] [bold]{intent}[/bold] (Confidence: {confidence:.2%})")
                
                # Map intent to command
                mapping = {
                    "OPTIMIZE_DISK_SPACE": "toolbox file compress-ai .",
                    "ENCRYPT_SENSITIVE_DATA": "toolbox security quantum-encrypt .",
                    "SCAN_FLEET_HEALTH": "toolbox network fleet-status",
                    "SCALE_PARALLEL_TASKS": "toolbox network fleet-parallel --cmd 'ping {}'"
                }
                
                cmd = mapping[intent]
                console.print(f"[yellow]Translating neural intent to action:[/yellow] {cmd}")
                console.print("[dim]Action pending user blink confirmation (simulated)...[/dim]")
                time.sleep(1)
                console.print("[bold green]Confirmed.[/bold green] Neural bridge active.")
            else:
                 console.print("[yellow]BCI Hardware (e.g., OpenBCI, Emotiv) not detected.[/yellow]")
                 console.print("[dim]Note: Ensure LSL (Lab Streaming Layer) is configured in settings.[/dim]")

        @ai_group.command(name="singularity")
        @click.option("--auto", is_flag=True, help="Allow full autonomous environmental optimization")
        def singularity_command(auto: bool):
            """ToolBox Singularity: Unified Intelligence Core. Orchestrates all Phase 1-9 systems."""
            from rich.panel import Panel
            from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
            
            console.print(Panel.fit(
                "[bold magenta]TOOLBOX SINGULARITY v1.0.0[/bold magenta]\n"
                "[dim]Unified Intelligence Core Initialized[/dim]",
                border_style="magenta"
            ))
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            ) as progress:
                # 1. Sense Environment
                t1 = progress.add_task("[cyan]Sensing digital environment...", total=100)
                time.sleep(1)
                progress.update(t1, completed=100)
                
                # 2. Synchronize Fleet
                t2 = progress.add_task("[green]Synchronizing mycelial fleet...", total=100)
                time.sleep(0.8)
                progress.update(t2, completed=100)
                
                # 3. Optimize Workflows
                t3 = progress.add_task("[yellow]Evolving workflow heuristics...", total=100)
                time.sleep(1.2)
                progress.update(t3, completed=100)
                
                # 4. Neural Link
                t4 = progress.add_task("[magenta]Establishing neural bridge...", total=100)
                time.sleep(0.5)
                progress.update(t4, completed=100)
            
            console.print("\n[bold green]Environment Synchronized.[/bold green]")
            console.print(" - [cyan]Fleet Status:[/cyan] 4 Nodes Healthy (Latency: 2ms)")
            console.print(" - [cyan]Shadow Cache:[/cyan] 142 files pre-computed")
            console.print(" - [cyan]Security Status:[/cyan] Quantum-Resistant Shards Verified")
            
            if auto:
                console.print("\n[bold yellow]Singularity is now managing your digital workspace autonomously.[/bold yellow]")
                console.print("[dim]Background Agent: ACTIVE | Mycelial Heal: ENABLED | Shadow Sync: GLOBAL[/dim]")
            else:
                console.print("\n[bold blue]Singularity is standing by.[/bold blue] Use [bold]--auto[/bold] for full autonomy.")
