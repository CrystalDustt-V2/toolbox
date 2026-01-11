import click
import urllib.request
import http.server
import socketserver
import socket
import os
import json
from pathlib import Path
from toolbox.core.plugin import BasePlugin, PluginMetadata

class NetworkPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="network",
            commands=["download", "serve", "info", "ping", "scan"],
            engine="python-built-in"
        )

    def register_commands(self, group):
        @group.group(name="network")
        def network_group():
            """Network and web utilities."""
            pass

        @network_group.command(name="download")
        @click.argument("url")
        @click.option("-o", "--output", help="Output filename")
        def download(url, output):
            """Download a file from a URL."""
            out_name = output or url.split("/")[-1] or "downloaded_file"
            
            click.echo(f"Downloading {url} to {out_name}...")
            try:
                urllib.request.urlretrieve(url, out_name)
                click.echo(f"Download complete: {out_name}")
            except Exception as e:
                click.echo(f"Error downloading file: {str(e)}")

        @network_group.command(name="serve")
        @click.option("-p", "--port", type=int, default=8000, help="Port to serve on")
        @click.option("-d", "--directory", type=click.Path(exists=True), default=".", help="Directory to serve")
        def serve(port, directory):
            """Start a simple HTTP server for a directory."""
            os_dir = os.path.abspath(directory)
            
            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=os_dir, **kwargs)

            click.echo(f"Serving directory {os_dir} on http://localhost:{port}")
            click.echo("Press Ctrl+C to stop.")
            
            try:
                with socketserver.TCPServer(("", port), Handler) as httpd:
                    httpd.serve_forever()
            except KeyboardInterrupt:
                click.echo("\nStopping server...")
            except Exception as e:
                click.echo(f"Error starting server: {str(e)}")

        @network_group.command(name="info")
        def network_info():
            """Get local and public network information."""
            # Local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            click.echo(f"Hostname: {hostname}")
            click.echo(f"Local IP: {local_ip}")
            
            # Public IP
            try:
                with urllib.request.urlopen("https://ipapi.co/json/", timeout=5) as response:
                    data = json.loads(response.read().decode())
                    click.echo(f"Public IP: {data.get('ip')}")
                    click.echo(f"ISP: {data.get('org')}")
                    click.echo(f"Location: {data.get('city')}, {data.get('region')}, {data.get('country_name')}")
            except Exception:
                click.echo("Public IP: Could not retrieve")

        @network_group.command(name="ping")
        @click.argument("host")
        def ping(host):
            """Basic host availability check."""
            try:
                socket.gethostbyname(host)
                click.echo(f"Host {host} is reachable (resolved).")
            except socket.gaierror:
                click.echo(f"Host {host} could not be resolved.")

        @network_group.command(name="scan")
        @click.argument("host")
        @click.option("-p", "--ports", default="22,80,443,3389,8000,8080", help="Comma-separated ports to scan")
        def port_scan(host, ports):
            """Simple port scanner."""
            port_list = [int(p.strip()) for p in ports.split(",")]
            click.echo(f"Scanning {host} for ports: {ports}...")
            
            for port in port_list:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((host, port))
                    if result == 0:
                        click.echo(f"Port {port}: OPEN")
                    else:
                        click.echo(f"Port {port}: CLOSED")
