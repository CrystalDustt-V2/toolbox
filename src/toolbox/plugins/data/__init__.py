import click
import json
import csv
import yaml
from pathlib import Path
from typing import Optional, List, Any, Dict
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.io import get_input_path
from toolbox.core.utils import console, batch_process
from rich.table import Table

class DataPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="data",
            commands=["convert", "inspect"],
            engine="python"
        )

    def register_commands(self, group):
        @group.group(name="data")
        def data_group():
            """Data format conversion and inspection."""
            pass

        @data_group.command(name="convert")
        @click.argument("input_file", required=False)
        @click.option("--from-format", type=click.Choice(['json', 'csv', 'yaml']), help="Input format")
        @click.option("--to-format", type=click.Choice(['json', 'csv', 'yaml']), required=True, help="Output format")
        @click.option("-o", "--output", help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        @batch_process
        def convert_data(input_file: Optional[str], from_format: Optional[str], to_format: str, output: Optional[str], dry_run: bool):
            """Convert between JSON, CSV, and YAML. Supports local or URL."""
            with get_input_path(input_file) as path:
                # Detect format if not provided
                if not from_format:
                    suffix = Path(input_file.split("?")[0]).suffix.lower()
                    if suffix == ".json": from_format = "json"
                    elif suffix == ".csv": from_format = "csv"
                    elif suffix in [".yaml", ".yml"]: from_format = "yaml"
                    else:
                        raise click.ClickException(f"Could not detect input format for {input_file}. Please specify --from-format.")

                if dry_run:
                    out_name = output or f"converted.{to_format}"
                    console.print(f"[yellow][DRY RUN][/yellow] Would convert [cyan]{input_file}[/cyan] ({from_format}) to [cyan]{out_name}[/cyan] ({to_format})")
                    return

                # Load data
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        if from_format == "json":
                            data = json.load(f)
                        elif from_format == "csv":
                            reader = csv.DictReader(f)
                            data = list(reader)
                        elif from_format == "yaml":
                            data = yaml.safe_load(f)
                except Exception as e:
                    raise click.ClickException(f"Error loading {from_format} data: {e}")

                # Save data
                out_name = output or f"{Path(input_file).stem}_converted.{to_format}"
                try:
                    with open(out_name, "w", encoding="utf-8") as f:
                        if to_format == "json":
                            json.dump(data, f, indent=4)
                        elif to_format == "yaml":
                            yaml.dump(data, f, sort_keys=False)
                        elif to_format == "csv":
                            if not isinstance(data, list) or not data:
                                raise click.ClickException("Data must be a list of objects to convert to CSV.")
                            writer = csv.DictWriter(f, fieldnames=data[0].keys())
                            writer.writeheader()
                            writer.writerows(data)
                    
                    console.print(f"[green]✓[/green] Converted [cyan]{input_file}[/cyan] to [cyan]{out_name}[/cyan]")
                except Exception as e:
                    raise click.ClickException(f"Error saving {to_format} data: {e}")

        @data_group.command(name="inspect")
        @click.argument("input_file", required=False)
        @batch_process
        def inspect_data(input_file: Optional[str]):
            """Inspect data structure and summary. Supports local or URL."""
            with get_input_path(input_file) as path:
                suffix = Path(input_file.split("?")[0]).suffix.lower()
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        if suffix == ".json":
                            data = json.load(f)
                            fmt = "JSON"
                        elif suffix == ".csv":
                            reader = csv.DictReader(f)
                            data = list(reader)
                            fmt = "CSV"
                        elif suffix in [".yaml", ".yml"]:
                            data = yaml.safe_load(f)
                            fmt = "YAML"
                        else:
                            console.print(f"[yellow]Unsupported format for inspection: {suffix}[/yellow]")
                            return
                except Exception as e:
                    raise click.ClickException(f"Error reading data: {e}")

                table = Table(title=f"Data Inspection: {input_file} ({fmt})")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="magenta")

                if isinstance(data, list):
                    table.add_row("Type", "List")
                    table.add_row("Length", str(len(data)))
                    if data and isinstance(data[0], dict):
                        table.add_row("Item Keys", ", ".join(data[0].keys()))
                elif isinstance(data, dict):
                    table.add_row("Type", "Object/Dictionary")
                    table.add_row("Keys", ", ".join(data.keys()))
                else:
                    table.add_row("Type", type(data).__name__)
                    table.add_row("Value (Preview)", str(data)[:100])

                console.print(table)
