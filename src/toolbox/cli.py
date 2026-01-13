import click
import difflib
import platform
import subprocess
import sys
import urllib.request
import yaml
import logging
from pathlib import Path
from rich.console import Console
from rich.table import Table

from toolbox.core.config import config_manager
from toolbox.core.plugin import plugin_manager
from toolbox.core.engine import engine_registry
from toolbox.core.workflow import WorkflowRunner
from toolbox.core.logging import setup_logging, logger
from toolbox import __version__

console = Console()

class FuzzyGroup(click.Group):
    """Click group with fuzzy command matching."""
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        
        # Fuzzy matching
        matches = difflib.get_close_matches(cmd_name, self.list_commands(ctx), cutoff=0.6)
        if matches:
            ctx.fail(f"'{cmd_name}' is not a toolbox command. Did you mean '{matches[0]}'?")
        return None

@click.group(cls=FuzzyGroup)
@click.version_option(version=__version__)
@click.option("--verbose", is_flag=True, help="Enable verbose output for engines")
@click.option("--gpu", is_flag=True, help="Enable GPU acceleration for AI tasks")
@click.option("--log-file", type=click.Path(), help="Path to log file")
def cli(verbose, gpu, log_file):
    """ToolBox: A universal offline CLI utility suite."""
    log_level = logging.DEBUG if verbose else logging.INFO
    setup_logging(level=log_level, log_file=Path(log_file) if log_file else None)
    
    if verbose:
        logger.debug("Verbose mode enabled")
    
    # Store GPU preference in config
    config_manager.set("gpu_enabled", gpu)
    
    for name, engine in engine_registry.engines.items():
        engine.verbose = verbose
        if hasattr(engine, "use_gpu"):
            engine.use_gpu = gpu

@cli.group(name="config")
def config_group():
    """Manage ToolBox configuration."""
    pass

@config_group.command(name="list")
def config_list():
    """List all current settings."""
    table = Table(title="ToolBox Settings")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    
    settings = config_manager.settings.model_dump()
    for key, value in settings.items():
        table.add_row(key, str(value))
    
    console.print(table)

@config_group.command(name="set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Update a setting (key value). Use dots for nested keys (e.g. engine_paths.ffmpeg)."""
    # Simple type conversion
    val: Any
    if value.lower() == "true":
        val = True
    elif value.lower() == "false":
        val = False
    elif value.isdigit():
        val = int(value)
    else:
        val = value

    try:
        if "." in key:
            # Handle nested keys like engine_paths.ffmpeg
            parts = key.split(".")
            main_key = parts[0]
            sub_key = parts[1]
            
            # Currently only engine_paths is a dict
            if main_key == "engine_paths":
                current_paths = config_manager.settings.engine_paths.copy()
                current_paths[sub_key] = val
                config_manager.update(engine_paths=current_paths)
            else:
                console.print(f"[yellow]Nested update for '{main_key}' not fully supported yet.[/yellow]")
                return
        else:
            config_manager.update(**{key: val})
            
        config_manager.save_config()
        console.print(f"[green]✓ Successfully set {key} to {val}[/green]")
    except Exception as e:
        console.print(f"[bold red]Error setting {key}:[/bold red] {str(e)}")

@cli.group(name="plugin")
def plugin_group():
    """Manage and discover ToolBox plugins."""
    pass

# Alias for backward compatibility
cli.add_command(plugin_group, name="plugins")

@plugin_group.command(name="list")
def plugin_list():
    """List all installed plugins."""
    table = Table(title="Installed Plugins")
    table.add_column("Plugin", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Commands", style="dim")
    
    for name, plugin in plugin_manager.plugins.items():
        metadata = plugin.get_metadata()
        table.add_row(name, metadata.version, ", ".join(metadata.commands))
    
    console.print(table)

@plugin_group.command(name="search")
@click.argument("query", required=False)
def plugin_search(query):
    """Search for community plugins."""
    community_plugins = [
        {"name": "toolbox-pdf-extra", "desc": "Advanced PDF merging and splitting", "author": "community"},
        {"name": "toolbox-crypto", "desc": "File encryption and decryption (AES/RSA)", "author": "community"},
        {"name": "toolbox-web-scrapper", "desc": "Extract data from websites to JSON/CSV", "author": "community"},
        {"name": "toolbox-image-ai", "desc": "AI-powered image upscaling and background removal", "author": "community"},
    ]
    
    table = Table(title="Community Plugins")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Author", style="dim")
    
    count = 0
    for p in community_plugins:
        if not query or query.lower() in p["name"].lower() or query.lower() in p["desc"].lower():
            table.add_row(p["name"], p["desc"], p["author"])
            count += 1
            
    if count > 0:
        console.print(table)
        console.print(f"\n[dim]To install a community plugin, use: toolbox plugin install <plugin-name>[/dim]")
    else:
        console.print(f"[yellow]No community plugins found matching '{query}'.[/yellow]")

@plugin_group.command(name="install")
@click.argument("plugin_name")
def plugin_install(plugin_name):
    """Install a community plugin (pip wrapper)."""
    console.print(f"[yellow]Attempting to install plugin: {plugin_name}...[/yellow]")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", plugin_name])
        console.print(f"[green]✓ Successfully installed {plugin_name}[/green]")
        console.print("[dim]Note: You may need to restart ToolBox to see the new plugin.[/dim]")
    except subprocess.CalledProcessError:
        console.print(f"[bold red]Error:[/bold red] Failed to install {plugin_name}. Ensure it exists on PyPI.")

@plugin_group.command(name="create")
@click.argument("name")
def plugin_create(name):
    """Create a new plugin scaffold."""
    try:
        path = plugin_manager.create_scaffold(name)
        console.print(f"[green]Successfully created plugin scaffold at: {path}[/green]")
        console.print(f"Restart ToolBox to see the new '{name}' command group.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@cli.command()
def update():
    """Self-update ToolBox from the official repository."""
    console.print("[cyan]Checking for updates...[/cyan]")
    try:
        # Check if we are in a git repository
        if not Path(".git").exists():
            console.print("[yellow]Not a git repository. Please update manually using pip.[/yellow]")
            return

        # Attempt to pull
        console.print("[yellow]Pulling latest changes from origin...[/yellow]")
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        
        if result.returncode == 0:
            if "Already up to date" in result.stdout:
                console.print("[green]✓ ToolBox is already up to date.[/green]")
            else:
                console.print("[green]✓ Successfully updated ToolBox![/green]")
                console.print("[yellow]Reinstalling dependencies...[/yellow]")
                subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."])
        else:
            console.print(f"[bold red]Update failed:[/bold red] {result.stderr}")
    except Exception as e:
        console.print(f"[bold red]Error during update:[/bold red] {str(e)}")

@cli.command()
@click.option("--show-paths", is_flag=True, help="Show absolute paths to engines")
def status(show_paths):
    """Check the status of engines and plugins."""
    # Engines status
    engine_table = Table(title="Execution Engines")
    engine_table.add_column("Engine", style="cyan")
    engine_table.add_column("Status", style="bold")
    if show_paths:
        engine_table.add_column("Path", style="dim")
    else:
        engine_table.add_column("Notes/Fix", style="dim")
    
    for name, available, hint in engine_registry.check_all():
        engine = engine_registry.get(name)
        if available:
            status_str = "[green]Available[/green]"
            note_str = engine.path if show_paths else "-"
        else:
            status_str = "[red]Not Found[/red]"
            note_str = hint
            
        engine_table.add_row(name, status_str, note_str)
    
    console.print(engine_table)

    # Plugins status
    plugin_table = Table(title="Installed Plugins")
    plugin_table.add_column("Plugin", style="magenta")
    plugin_table.add_column("Commands", style="yellow")
    
    for name, plugin in plugin_manager.plugins.items():
        cmds = ", ".join(plugin.metadata.commands)
        plugin_table.add_row(name, cmds)
    
    console.print(plugin_table)

@cli.command(name="check")
def check_system():
    """Thoroughly check system readiness and environment."""
    console.print("[bold cyan]System Intelligence Check[/bold cyan]\n")
    
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    console.print(f"Python Version: [green]{py_version}[/green]")
    console.print(f"Platform: [green]{platform.platform()}[/green]")
    
    bin_dir = Path("bin")
    if bin_dir.exists():
        bin_files = list(bin_dir.glob("*"))
        console.print(f"Bundled Binaries (bin/): [green]{len(bin_files)} files found[/green]")
    else:
        console.print("Bundled Binaries (bin/): [yellow]Not present[/yellow]")

    # Check dependencies
    dependencies = ["PIL", "pypdf", "yaml", "click", "rich", "pytesseract", "pdf2image"]
    console.print("\n[bold]Dependency Check:[/bold]")
    for dep in dependencies:
        try:
            __import__(dep if dep != "PIL" else "PIL")
            console.print(f"- {dep}: [green]Installed[/green]")
        except ImportError:
            console.print(f"- {dep}: [red]Missing[/red]")

    console.print("\n[bold]Connectivity Check:[/bold]")
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        console.print("- Internet: [green]Connected[/green]")
    except Exception:
        console.print("- Internet: [red]Offline/Blocked[/red]")

    console.print("\n[bold]Engine Validation:[/bold]")
    for name, available, hint in engine_registry.check_all():
        if available:
            engine = engine_registry.get(name)
            try:
                # Try a simple version check or help command for the engine
                if name == "ffmpeg":
                    engine.run(["-version"], check=True)
                elif name == "tesseract":
                    engine.run(["--version"], check=True)
                elif name == "libreoffice":
                    engine.run(["--version"], check=True)
                console.print(f"- {name}: [green]Functional[/green]")
            except Exception as e:
                console.print(f"- {name}: [yellow]Available but potentially broken ({str(e)})[/yellow]")
        else:
            console.print(f"- {name}: [red]Not found[/red]")

@cli.group(name="workflow")
def workflow_group():
    """Manage and run automated workflows."""
    pass

@workflow_group.command(name="run")
@click.argument("workflow_file", type=click.Path(exists=True))
@click.option("-v", "--var", multiple=True, help="Override workflow variables (key=value)")
@click.option("--dry-run", is_flag=True, help="Validate workflow without executing commands")
def run_workflow(workflow_file, var, dry_run):
    """Run a sequence of commands from a workflow YAML file."""
    overrides = {}
    for v in var:
        if "=" in v:
            key, value = v.split("=", 1)
            overrides[key] = value

    runner = WorkflowRunner(cli)
    try:
        runner.run(workflow_file, overrides=overrides, dry_run=dry_run)
    except Exception as e:
        console.print(f"[bold red]Workflow failed:[/bold red] {str(e)}")
        raise click.Abort()

@workflow_group.command(name="init")
@click.argument("filename", default="workflow.yaml")
def init_workflow(filename):
    """Interactively create a new workflow file."""
    console.print("[bold blue]Interactive Workflow Builder[/bold blue]")
    
    name = click.prompt("Workflow Name", default="My ToolBox Workflow")
    description = click.prompt("Description", default="A series of ToolBox commands")
    
    steps = []
    while True:
        console.print(f"\n[bold]Adding Step {len(steps) + 1}[/bold]")
        step_name = click.prompt("Step Name (e.g., 'Resize Images')")
        command = click.prompt("ToolBox Command (e.g., 'image resize input.jpg -w 800')")
        
        steps.append({
            "name": step_name,
            "command": command
        })
        
        if not click.confirm("Add another step?", default=True):
            break
            
    workflow_data = {
        "name": name,
        "description": description,
        "vars": {
            "input_file": "input.jpg"
        },
        "steps": steps
    }
    
    with open(filename, "w") as f:
        yaml.dump(workflow_data, f, sort_keys=False)
        
    console.print(f"\n[bold green]✓ Workflow saved to {filename}[/bold green]")
    console.print(f"Run it with: [cyan]toolbox workflow run {filename}[/cyan]")

@workflow_group.command(name="watch")
@click.argument("directory", type=click.Path(exists=True))
@click.argument("workflow_file", type=click.Path(exists=True))
@click.option("--ext", multiple=True, help="Extensions to watch for (e.g. .jpg)")
def watch_workflow(directory, workflow_file, ext):
    """Watch a directory for new files and auto-trigger a workflow."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import time

    class WorkflowHandler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            
            p = Path(event.src_path)
            if ext and p.suffix.lower() not in [e.lower() if e.startswith(".") else f".{e.lower()}" for e in ext]:
                return

            logger.info(f"New file detected: {p.name}. Triggering workflow...")
            runner = WorkflowRunner(cli)
            try:
                # Set the input_file variable to the new file
                runner.run(workflow_file, overrides={"input_file": str(p)})
            except Exception as e:
                logger.error(f"Auto-workflow failed: {e}")

    observer = Observer()
    handler = WorkflowHandler()
    observer.schedule(handler, directory, recursive=False)
    observer.start()
    
    console.print(f"[bold green]Watching {directory} for new files...[/bold green]")
    console.print("[dim]Press Ctrl+C to stop.[/dim]")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@workflow_group.command(name="schedule")
@click.argument("workflow_file", type=click.Path(exists=True))
@click.option("--interval", type=int, default=60, help="Interval in minutes")
@click.option("--immediate", is_flag=True, help="Run immediately before first interval")
def schedule_workflow(workflow_file, interval, immediate):
    """Schedule a workflow to run periodically."""
    import schedule
    import time

    def job():
        logger.info(f"Scheduled run for {workflow_file}...")
        runner = WorkflowRunner(cli)
        try:
            runner.run(workflow_file)
        except Exception as e:
            logger.error(f"Scheduled workflow failed: {e}")

    schedule.every(interval).minutes.do(job)
    
    if immediate:
        job()

    console.print(f"[bold green]Scheduled {workflow_file} every {interval} minutes.[/bold green]")
    console.print("[dim]Press Ctrl+C to stop.[/dim]")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

# Initialize plugins
plugin_manager.load_plugins()
for plugin in plugin_manager.plugins.values():
    plugin.register_commands(cli)

def main():
    cli()

if __name__ == "__main__":
    main()
