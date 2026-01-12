import click
import urllib.request
import http.server
import socketserver
import socket
import os
import json
from pathlib import Path
from typing import Optional

from rich.table import Table
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import console
from toolbox.core.utils import is_safe_url

class NetworkPlugin(BasePlugin):
    """Plugin for network and web utilities."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="network",
            commands=["download", "serve", "info", "ping", "scan"],
            engine="python-built-in"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="network")
        def network_group():
            """Network and web utilities."""
            pass

        @network_group.command(name="download")
        @click.argument("url")
        @click.option("-o", "--output", help="Output filename")
        @click.option("--dry-run", is_flag=True, help="Show what would happen")
        def download(url: str, output: Optional[str], dry_run: bool):
            """Download a file from a URL."""
            if not is_safe_url(url):
                console.print(f"[bold red]Error:[/bold red] URL '{url}' is not safe or is blocked.")
                return

            out_name = output or url.split("/")[-1] or "downloaded_file"
            
            if dry_run:
                console.print(f"[bold yellow]Would download {url} to {out_name}[/bold yellow]")
                return

            console.print(f"[cyan]Downloading {url} to {out_name}...[/cyan]")
            try:
                urllib.request.urlretrieve(url, out_name)
                console.print(f"[green]✓ Download complete: {out_name}[/green]")
            except Exception as e:
                console.print(f"[bold red]Error downloading file:[/bold red] {str(e)}")

        @network_group.command(name="serve")
        @click.option("-p", "--port", type=int, default=8000, help="Port to serve on")
        @click.option("-d", "--directory", type=click.Path(exists=True), default=".", help="Directory to serve")
        def serve(port: int, directory: str):
            """Start a simple HTTP server for a directory."""
            os_dir = os.path.abspath(directory)
            
            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=os_dir, **kwargs)

            console.print(f"[green]Serving directory {os_dir} on http://localhost:{port}[/green]")
            console.print("[yellow]Press Ctrl+C to stop.[/yellow]")
            
            try:
                with socketserver.TCPServer(("", port), Handler) as httpd:
                    httpd.serve_forever()
            except KeyboardInterrupt:
                console.print("\n[yellow]Stopping server...[/yellow]")
            except Exception as e:
                console.print(f"[bold red]Error starting server:[/bold red] {str(e)}")

        @network_group.command(name="info")
        def network_info():
            """Get local and public network information."""
            # Local IP
            hostname = socket.gethostname()
            try:
                local_ip = socket.gethostbyname(hostname)
            except Exception:
                local_ip = "Unknown"
            
            table = Table(title="Network Information")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Hostname", hostname)
            table.add_row("Local IP", local_ip)
            
            # Public IP
            try:
                with urllib.request.urlopen("https://ipapi.co/json/", timeout=5) as response:
                    data = json.loads(response.read().decode())
                    table.add_row("Public IP", data.get('ip', 'Unknown'))
                    table.add_row("ISP", data.get('org', 'Unknown'))
                    location = f"{data.get('city')}, {data.get('region')}, {data.get('country_name')}"
                    table.add_row("Location", location)
            except Exception:
                table.add_row("Public IP", "[yellow]Could not retrieve[/yellow]")

            console.print(table)

        @network_group.command(name="ping")
        @click.argument("host")
        def ping(host: str):
            """Basic host availability check."""
            try:
                ip = socket.gethostbyname(host)
                console.print(f"[green]✓ Host {host} is reachable (resolved to {ip}).[/green]")
            except socket.gaierror:
                console.print(f"[bold red]Error:[/bold red] Host {host} could not be resolved.")

        @network_group.command(name="scan")
        @click.argument("host")
        @click.option("-p", "--ports", default="22,80,443,3389,8000,8080", help="Comma-separated ports to scan")
        def port_scan(host: str, ports: str):
            """Simple port scanner."""
            port_list = [int(p.strip()) for p in ports.split(",")]
            
            table = Table(title=f"Port Scan for {host}")
            table.add_column("Port", style="cyan")
            table.add_column("Status", style="bold")
            
            console.print(f"[cyan]Scanning {host} for ports: {ports}...[/cyan]")
            
            for port in port_list:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((host, port))
                    if result == 0:
                        table.add_row(str(port), "[green]OPEN[/green]")
                    else:
                        table.add_row(str(port), "[red]CLOSED[/red]")
            
            console.print(table)
