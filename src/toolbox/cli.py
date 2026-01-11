import click
import difflib
from rich.console import Console
from rich.table import Table
from toolbox.core.config import config_manager
from toolbox.core.plugin import plugin_manager
from toolbox.core.engine import engine_registry
from toolbox.core.workflow import WorkflowRunner

console = Console()

class FuzzyGroup(click.Group):
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
@click.version_option(version="0.1.0")
@click.option("--verbose", is_flag=True, help="Enable verbose output for engines")
def cli(verbose):
    """ToolBox: A universal offline CLI utility suite."""
    if verbose:
        for name, engine in engine_registry.engines.items():
            engine.verbose = True

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
                # Fallback for other potential future nested keys
                click.echo(f"Nested update for {main_key} not fully supported yet.")
                return
        else:
            config_manager.update(**{key: val})
            
        config_manager.save_config()
        click.echo(f"Successfully set {key} to {val}")
    except Exception as e:
        click.echo(f"Error setting {key}: {str(e)}")

@cli.group(name="plugins")
def plugins_group():
    """Manage and discover plugins."""
    pass

@plugins_group.command(name="list")
def plugins_list():
    """List all installed plugins."""
    table = Table(title="Installed Plugins")
    table.add_column("Plugin", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Commands", style="dim")
    
    for name, plugin in plugin_manager.plugins.items():
        metadata = plugin.get_metadata()
        table.add_row(name, "0.1.0", ", ".join(metadata.commands))
    
    console.print(table)

@plugins_group.command(name="search")
@click.argument("query", required=False)
def plugins_search(query):
    """Search for community plugins (Mock)."""
    # This is a mock implementation for the open-source release
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
        console.print(f"\n[dim]To install a community plugin, use: pip install <plugin-name>[/dim]")
    else:
        console.print(f"No community plugins found matching '{query}'.")

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
    
    # Check Python version
    import sys
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    console.print(f"Python Version: [green]{py_version}[/green]")
    
    # Check OS
    import platform
    console.print(f"Platform: [green]{platform.platform()}[/green]")
    
    # Check bin directory
    from pathlib import Path
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

    # Check internet connectivity
    import urllib.request
    console.print("\n[bold]Connectivity Check:[/bold]")
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        console.print("- Internet: [green]Connected[/green]")
    except Exception:
        console.print("- Internet: [red]Offline/Blocked[/red]")

    # Engine validation
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

@cli.command(name="run")
@click.argument("workflow_file", type=click.Path(exists=True))
@click.option("-v", "--var", multiple=True, help="Override workflow variables (key=value)")
def run_workflow(workflow_file, var):
    """Run a sequence of commands from a workflow YAML file."""
    overrides = {}
    for v in var:
        if "=" in v:
            key, value = v.split("=", 1)
            overrides[key] = value

    runner = WorkflowRunner(cli)
    try:
        runner.run(workflow_file, overrides=overrides)
    except Exception as e:
        console.print(f"[bold red]Workflow failed:[/bold red] {str(e)}")
        raise click.Abort()

@cli.group(name="plugin")
def plugin_group():
    """Manage ToolBox plugins."""
    pass

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

# Initialize plugins
plugin_manager.load_plugins()
for plugin in plugin_manager.plugins.values():
    plugin.register_commands(cli)

def main():
    cli()

if __name__ == "__main__":
    main()
