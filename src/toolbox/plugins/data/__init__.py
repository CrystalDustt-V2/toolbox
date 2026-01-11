import click
import json
import csv
import yaml
from pathlib import Path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.io import get_input_path

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
        @click.argument("input_file")
        @click.option("--from-format", type=click.Choice(['json', 'csv', 'yaml']), help="Input format")
        @click.option("--to-format", type=click.Choice(['json', 'csv', 'yaml']), required=True, help="Output format")
        @click.option("-o", "--output", help="Output filename")
        def convert_data(input_file, from_format, to_format, output):
            """Convert between JSON, CSV, and YAML. Supports local or URL."""
            with get_input_path(input_file) as path:
                # Detect format if not provided
                if not from_format:
                    suffix = Path(input_file.split("?")[0]).suffix.lower()
                    if suffix == ".json": from_format = "json"
                    elif suffix == ".csv": from_format = "csv"
                    elif suffix in [".yaml", ".yml"]: from_format = "yaml"
                    else:
                        raise click.ClickException("Could not detect input format. Please specify --from-format.")

                # Load data
                with open(path, "r", encoding="utf-8") as f:
                    if from_format == "json":
                        data = json.load(f)
                    elif from_format == "csv":
                        reader = csv.DictReader(f)
                        data = list(reader)
                    elif from_format == "yaml":
                        data = yaml.safe_load(f)

                # Save data
                out_name = output or f"converted.{to_format}"
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
                
                click.echo(f"Converted {input_file} to {out_name}")

        @data_group.command(name="inspect")
        @click.argument("input_file")
        def inspect_data(input_file):
            """Inspect data structure and summary. Supports local or URL."""
            with get_input_path(input_file) as path:
                suffix = Path(input_file.split("?")[0]).suffix.lower()
                with open(path, "r", encoding="utf-8") as f:
                    if suffix == ".json":
                        data = json.load(f)
                    elif suffix == ".csv":
                        reader = csv.DictReader(f)
                        data = list(reader)
                    elif suffix in [".yaml", ".yml"]:
                        data = yaml.safe_load(f)
                    else:
                        click.echo("Unsupported format for inspection.")
                        return

                if isinstance(data, list):
                    click.echo(f"Type: List")
                    click.echo(f"Length: {len(data)}")
                    if data:
                        click.echo(f"Item Keys: {list(data[0].keys())}")
                elif isinstance(data, dict):
                    click.echo(f"Type: Object/Dictionary")
                    click.echo(f"Keys: {list(data.keys())}")
                else:
                    click.echo(f"Type: {type(data).__name__}")
