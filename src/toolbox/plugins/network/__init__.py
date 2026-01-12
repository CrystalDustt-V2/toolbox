import click
import urllib.request
import http.server
import socketserver
import socket
import os
import json
import ssl
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from rich.table import Table
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import console
from toolbox.core.utils import is_safe_url

class NetworkPlugin(BasePlugin):
    """Plugin for network and web utilities."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="network",
            commands=["download", "serve", "info", "ping", "scan", "whois", "cert-check"],
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

        @network_group.command(name="whois")
        @click.argument("domain")
        def whois(domain: str):
            """Get WHOIS information for a domain (via RDAP)."""
            console.print(f"[cyan]Querying RDAP for domain: {domain}...[/cyan]")
            
            # Use RDAP (Registration Data Access Protocol) - modern alternative to WHOIS
            rdap_url = f"https://rdap.org/domain/{domain}"
            
            try:
                req = urllib.request.Request(rdap_url)
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                
                table = Table(title=f"RDAP/WHOIS: {domain}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="green")
                
                table.add_row("Handle", data.get("handle", "N/A"))
                table.add_row("Status", ", ".join(data.get("status", [])))
                
                # Extract registration/expiry dates
                events = data.get("events", [])
                for event in events:
                    action = event.get("eventAction", "Unknown")
                    date = event.get("eventDate", "Unknown")
                    if action in ["registration", "expiration", "last changed"]:
                        table.add_row(action.capitalize(), date)
                
                # Extract nameservers
                nameservers = [ns.get("ldhName") for ns in data.get("nameservers", [])]
                if nameservers:
                    table.add_row("Nameservers", ", ".join(nameservers))
                
                console.print(table)
            except Exception as e:
                console.print(f"[bold red]Error querying RDAP:[/bold red] {str(e)}")
                console.print("[dim]Note: RDAP might not be supported by all TLDs or may require direct WHOIS protocol.[/dim]")

        @network_group.command(name="cert-check")
        @click.argument("host")
        @click.option("-p", "--port", type=int, default=443)
        def cert_check(host: str, port: int):
            """Check SSL certificate information."""
            console.print(f"[cyan]Retrieving SSL certificate for {host}:{port}...[/cyan]")
            
            context = ssl.create_default_context()
            try:
                with socket.create_connection((host, port), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=host) as ssock:
                        cert = ssock.getpeercert()
                
                if not cert:
                    console.print("[bold red]Error:[/bold red] Could not retrieve peer certificate.")
                    return
                
                table = Table(title=f"SSL Certificate: {host}")
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="green")
                
                # Subject information
                subject = dict(x[0] for x in cert.get('subject', []))
                table.add_row("Common Name", subject.get('commonName', 'N/A'))
                table.add_row("Organization", subject.get('organizationName', 'N/A'))
                
                # Issuer information
                issuer = dict(x[0] for x in cert.get('issuer', []))
                table.add_row("Issuer CN", issuer.get('commonName', 'N/A'))
                
                # Validity
                not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (not_after - datetime.utcnow()).days
                
                table.add_row("Valid From", not_before.strftime('%Y-%m-%d'))
                table.add_row("Expires On", not_after.strftime('%Y-%m-%d'))
                
                status_color = "green" if days_left > 30 else "yellow" if days_left > 0 else "bold red"
                table.add_row("Days Remaining", f"[{status_color}]{days_left}[/{status_color}]")
                
                # SANs
                sans = [alt[1] for alt in cert.get('subjectAltName', [])]
                if sans:
                    table.add_row("Alt Names", ", ".join(sans[:5]) + ("..." if len(sans) > 5 else ""))
                
                console.print(table)
                
            except Exception as e:
                console.print(f"[bold red]Error retrieving SSL certificate:[/bold red] {str(e)}")

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
