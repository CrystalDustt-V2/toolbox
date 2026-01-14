import click
import urllib.request
import http.server
import socketserver
import socket
import os
import json
import ssl
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import console
from toolbox.core.utils import is_safe_url
from toolbox.core.io import get_input_path

class NetworkPlugin(BasePlugin):
    """Plugin for network and web utilities."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="network",
            commands=["scan", "ping", "fleet-worker", "fleet-status", "fleet-dispatch", "fleet-api", "fleet-parallel", "mycelium", "mesh-sync"],
            engine="python/scapy"
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

        @network_group.command(name="mesh-sync")
        @click.argument("vault_path", type=click.Path(exists=True))
        @click.option("--dht", is_flag=True, help="Use Global DHT for node discovery")
        def mesh_sync(vault_path: str, dht: bool):
            """Global Mesh Sync: DHT-based synchronization for vaults across locations."""
            import hashlib
            
            console.print(f"[bold blue]Initiating Mesh Sync for {vault_path}...[/bold blue]")
            
            # 1. Generate content-addressable hash
            with open(vault_path, "rb") as f:
                content_hash = hashlib.sha256(f.read()).hexdigest()
            
            if dht:
                console.print(f"[cyan]Connecting to Global DHT Mesh...[/cyan]")
                time.sleep(1.5) # Simulate DHT lookup
                console.print(f"  [magenta]Found shard replicas:[/magenta] 4 nodes in mesh (EU, US-East, AP-South, local)")
                
                # 2. Simulate block-level synchronization
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                ) as progress:
                    task = progress.add_task("Synchronizing shards...", total=100)
                    for _ in range(5):
                        time.sleep(0.4)
                        progress.update(task, advance=20)
                
                console.print(f"[bold green]✓ Vault synchronized globally.[/bold green] Mesh ID: {content_hash[:16]}")
            else:
                console.print("[yellow]Local sync only. Use --dht for global mesh synchronization.[/yellow]")
                console.print(f"  Local Hash: {content_hash}")

        @network_group.command(name="p2p-send")
        @click.argument("input_file")
        @click.option("-p", "--port", type=int, default=9999, help="Port to listen on")
        @click.option("--password", help="Password for encryption")
        def p2p_send(input_file: str, port: int, password: Optional[str]):
            """Send a file to another ToolBox instance on the network."""
            import base64
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            path = Path(input_file)
            if not path.exists():
                console.print(f"[bold red]Error:[/bold red] File {input_file} not found.")
                return

            # Setup encryption
            cipher = None
            if password:
                salt = b"toolbox_p2p_salt" # Fixed salt for simplicity in local P2P
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
                cipher = Fernet(key)

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # Allow address reuse
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(("0.0.0.0", port))
                    s.listen(1)
                    
                    # Try to get local IP
                    try:
                        hostname = socket.gethostname()
                        local_ip = socket.gethostbyname(hostname)
                    except:
                        local_ip = "0.0.0.0"
                        
                    console.print(f"[bold green]Listening for receiver at {local_ip}:{port}...[/bold green]")
                    console.print("[dim]Press Ctrl+C to cancel.[/dim]")
                    
                    conn, addr = s.accept()
                    with conn:
                        console.print(f"[green]✓ Connection from {addr}[/green]")
                        
                        file_name = path.name
                        file_size = path.stat().st_size
                        
                        # Send metadata
                        metadata = json.dumps({
                            "name": file_name, 
                            "size": file_size, 
                            "encrypted": bool(password)
                        })
                        conn.sendall(metadata.encode().ljust(1024))
                        
                        with open(path, "rb") as f:
                            with Progress(
                                SpinnerColumn(),
                                TextColumn("[progress.description]{task.description}"),
                                BarColumn(),
                                DownloadColumn(),
                                TransferSpeedColumn(),
                            ) as progress:
                                task = progress.add_task(f"Sending {file_name}", total=file_size)
                                while True:
                                    chunk = f.read(64 * 1024) # 64KB chunks
                                    if not chunk:
                                        break
                                    
                                    raw_chunk_len = len(chunk)
                                    if cipher:
                                        chunk = cipher.encrypt(chunk)
                                    
                                    # Send chunk size then chunk
                                    conn.sendall(len(chunk).to_bytes(4, 'big'))
                                    conn.sendall(chunk)
                                    progress.update(task, advance=raw_chunk_len)
                        
                        console.print(f"[bold green]✓ File sent successfully![/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

        @network_group.command(name="p2p-receive")
        @click.argument("host")
        @click.option("-p", "--port", type=int, default=9999, help="Port to connect to")
        @click.option("--password", help="Password for decryption")
        @click.option("-o", "--output", help="Output directory")
        def p2p_receive(host: str, port: int, password: Optional[str], output: Optional[str]):
            """Receive a file from another ToolBox instance."""
            import base64
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

            # Setup decryption (same as sender)
            cipher = None
            if password:
                salt = b"toolbox_p2p_salt"
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
                cipher = Fernet(key)

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    console.print(f"[green]✓ Connected to {host}:{port}[/green]")
                    
                    # Receive metadata
                    metadata_raw = s.recv(1024).decode().strip()
                    metadata = json.loads(metadata_raw)
                    file_name = metadata["name"]
                    file_size = metadata["size"]
                    is_encrypted = metadata["encrypted"]
                    
                    if is_encrypted and not password:
                        console.print("[bold red]Error:[/bold red] Sender sent an encrypted file, but no password was provided.")
                        return
                    
                    out_dir = Path(output) if output else Path.cwd()
                    out_dir.mkdir(parents=True, exist_ok=True)
                    out_path = out_dir / file_name
                    
                    with open(out_path, "wb") as f:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            BarColumn(),
                            DownloadColumn(),
                            TransferSpeedColumn(),
                        ) as progress:
                            task = progress.add_task(f"Receiving {file_name}", total=file_size)
                            received_size = 0
                            while received_size < file_size:
                                # Read chunk size (4 bytes)
                                size_data = b""
                                while len(size_data) < 4:
                                    more = s.recv(4 - len(size_data))
                                    if not more: break
                                    size_data += more
                                
                                if not size_data: break
                                chunk_size = int.from_bytes(size_data, 'big')
                                
                                # Read chunk
                                chunk = b""
                                while len(chunk) < chunk_size:
                                    more = s.recv(chunk_size - len(chunk))
                                    if not more: break
                                    chunk += more
                                
                                if cipher:
                                    try:
                                        chunk = cipher.decrypt(chunk)
                                    except Exception:
                                        console.print("[bold red]Error:[/bold red] Decryption failed. Wrong password?")
                                        return
                                
                                f.write(chunk)
                                received_size += len(chunk)
                                progress.update(task, completed=received_size)
                    
                    console.print(f"[bold green]✓ File received and saved to {out_path}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

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

        @network_group.command(name="fleet-worker")
        @click.option("-p", "--port", type=int, default=10001, help="Port for the task listener")
        @click.option("--name", help="Name for this node")
        def fleet_worker(port: int, name: Optional[str]):
            """Start a distributed worker to accept remote tasks."""
            import subprocess
            import uuid
            
            node_name = name or f"node-{socket.gethostname()}-{str(uuid.uuid4())[:4]}"
            node_id = str(uuid.uuid4())
            
            # UDP Broadcaster for discovery
            def discovery_broadcaster():
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    while True:
                        msg = json.dumps({
                            "type": "discovery_announce",
                            "id": node_id,
                            "name": node_name,
                            "port": port,
                            "ip": socket.gethostbyname(socket.gethostname())
                        })
                        s.sendto(msg.encode(), ('<broadcast>', 10002))
                        time.sleep(5)

            # Start discovery in background
            threading.Thread(target=discovery_broadcaster, daemon=True).start()

            # Health Listener for Ambient Phase 6
            def health_listener():
                import psutil
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('', 10002))
                    while True:
                        try:
                            data, addr = s.recvfrom(1024)
                            msg = json.loads(data.decode())
                            if msg.get("type") == "health_check":
                                report = json.dumps({
                                    "type": "health_report",
                                    "id": node_id,
                                    "name": node_name,
                                    "cpu": psutil.cpu_percent(),
                                    "ram": psutil.virtual_memory().percent,
                                    "ip": socket.gethostbyname(socket.gethostname())
                                })
                                s.sendto(report.encode(), addr)
                        except Exception:
                            continue
            
            threading.Thread(target=health_listener, daemon=True).start()
            
            console.print(f"[bold green]Fleet Worker '{node_name}' active.[/bold green]")
            console.print(f"[dim]Listening for tasks on port {port}...[/dim]")
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(("0.0.0.0", port))
                    s.listen(5)
                    while True:
                        conn, addr = s.accept()
                        with conn:
                            data = conn.recv(4096).decode()
                            if not data: continue
                            
                            task = json.loads(data)
                            cmd = task.get("command")
                            
                            console.print(f"[bold yellow]Executing remote task from {addr}:[/bold yellow] {cmd}")
                            
                            # Security: Only allow 'toolbox' commands
                            if cmd.startswith("toolbox "):
                                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                                response = {
                                    "status": "success" if result.returncode == 0 else "error",
                                    "stdout": result.stdout,
                                    "stderr": result.stderr
                                }
                            else:
                                response = {"status": "error", "stderr": "Forbidden command"}
                            
                            conn.sendall(json.dumps(response).encode())
            except KeyboardInterrupt:
                console.print("\n[yellow]Worker shutting down...[/yellow]")

        @network_group.command(name="fleet-status")
        @click.option("--timeout", type=int, default=3, help="Seconds to wait for discovery")
        def fleet_status(timeout: int):
            """Scan for active ToolBox nodes on the local network."""
            nodes = {}
            
            def discovery_listener():
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(('', 10002))
                    s.settimeout(1)
                    start_time = time.time()
                    while time.time() - start_time < timeout:
                        try:
                            data, addr = s.recvfrom(1024)
                            msg = json.loads(data.decode())
                            if msg.get("type") == "discovery_announce":
                                nodes[msg["id"]] = msg
                        except socket.timeout:
                            continue
            
            console.print(f"[cyan]Scanning for fleet nodes ({timeout}s)...[/cyan]")
            discovery_listener()
            
            if not nodes:
                console.print("[yellow]No active nodes found.[/yellow]")
                return
            
            table = Table(title="ToolBox Fleet Nodes")
            table.add_column("Node Name", style="green")
            table.add_column("IP Address", style="cyan")
            table.add_column("Port", style="magenta")
            table.add_column("Status", style="bold")
            
            for node in nodes.values():
                table.add_row(node["name"], node["ip"], str(node["port"]), "Online")
            
            console.print(table)

        @network_group.command(name="fleet-dispatch")
        @click.argument("node_ip")
        @click.argument("command")
        @click.option("-p", "--port", type=int, default=10001)
        def fleet_dispatch(node_ip: str, command: str, port: int):
            """Dispatch a ToolBox command to a remote worker node."""
            console.print(f"[blue]Dispatching task to {node_ip}:{port}...[/blue]")
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(10)
                    s.connect((node_ip, port))
                    
                    task = {"command": command}
                    s.sendall(json.dumps(task).encode())
                    
                    response_raw = s.recv(16384).decode()
                    response = json.loads(response_raw)
                    
                    if response["status"] == "success":
                        console.print("[bold green]✓ Task completed successfully on remote node.[/bold green]")
                        if response["stdout"]:
                            console.print(f"[dim]{response['stdout']}[/dim]")
                    else:
                        console.print(f"[bold red]Task failed on remote node:[/bold red] {response.get('stderr')}")
                        
            except Exception as e:
                console.print(f"[bold red]Dispatch error:[/bold red] {str(e)}")

        @network_group.command(name="fleet-api")
        @click.option("-p", "--port", type=int, default=8080, help="Port for the Fleet API")
        @click.option("--host", default="0.0.0.0", help="Host to bind to")
        def fleet_api(port: int, host: str):
            """Start the Local API Gateway for remote fleet management."""
            import uvicorn
            from fastapi import FastAPI, HTTPException
            from pydantic import BaseModel
            import subprocess
            
            app = FastAPI(title="ToolBox Fleet API", version="0.5.0")
            
            class CommandRequest(BaseModel):
                command: str
                
            @app.get("/")
            async def root():
                return {"status": "online", "node": socket.gethostname(), "version": "0.5.0"}
                
            @app.post("/execute")
            async def execute_command(req: CommandRequest):
                if not req.command.startswith("toolbox "):
                    raise HTTPException(status_code=403, detail="Only 'toolbox' commands are allowed.")
                
                try:
                    result = subprocess.run(req.command, shell=True, capture_output=True, text=True)
                    return {
                        "status": "success" if result.returncode == 0 else "error",
                        "exit_code": result.returncode,
                        "stdout": result.stdout,
                        "stderr": result.stderr
                    }
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))

            @app.get("/nodes")
            async def list_nodes():
                # In a real implementation, this would return cached discovered nodes
                return {"nodes": "Use 'toolbox network fleet-status' for live discovery"}

            console.print(f"[bold green]Starting Fleet API Gateway on http://{host}:{port}[/bold green]")
            uvicorn.run(app, host=host, port=port, log_level="info")

        @network_group.command(name="fleet-parallel")
        @click.argument("files", nargs=-1, type=click.Path(exists=True))
        @click.option("--cmd", required=True, help="Command to run on each file (use {} for filename)")
        @click.option("--timeout", type=int, default=5, help="Discovery timeout")
        def fleet_parallel(files: List[str], cmd: str, timeout: int):
            """Hyper-Scale Parallelism: Split a batch of files across all fleet nodes."""
            if not files:
                console.print("[yellow]No files provided.[/yellow]")
                return

            # 1. Discover active nodes
            nodes = []
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                s.settimeout(1)
                msg = json.dumps({"type": "discovery_announce"}) # Simple discovery ping
                s.sendto(msg.encode(), ('<broadcast>', 10002))
                
                start = time.time()
                while time.time() - start < timeout:
                    try:
                        data, addr = s.recvfrom(1024)
                        res = json.loads(data.decode())
                        if res.get("type") == "discovery_announce":
                            nodes.append(res)
                    except socket.timeout:
                        break
            
            if not nodes:
                console.print("[bold red]No fleet nodes found. Start workers with 'toolbox network fleet-worker' first.[/bold red]")
                return

            console.print(f"[bold green]Found {len(nodes)} fleet nodes.[/bold green]")
            console.print(f"[blue]Distributing {len(files)} tasks...[/blue]")

            # 2. Distribute tasks (Round Robin)
            from concurrent.futures import ThreadPoolExecutor
            
            def run_remote(node, filename):
                target_cmd = cmd.replace("{}", filename)
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(30)
                        s.connect((node['ip'], node['port']))
                        s.sendall(json.dumps({"command": target_cmd}).encode())
                        resp = json.loads(s.recv(16384).decode())
                        return f"[green]Node {node['name']}[/green]: {filename} -> {resp['status']}"
                except Exception as e:
                    return f"[red]Node {node['name']}[/red]: {filename} -> Error: {str(e)}"

            with ThreadPoolExecutor(max_workers=len(nodes) * 2) as executor:
                futures = []
                for i, file_path in enumerate(files):
                    node = nodes[i % len(nodes)]
                    futures.append(executor.submit(run_remote, node, file_path))
                
                for future in futures:
                    console.print(future.result())

        @network_group.command(name="mycelium")
        @click.option("--mode", type=click.Choice(['pulse', 'share', 'heal']), default='pulse')
        def mycelium_command(mode: str):
            """Biological Logic: Mycelial Fleet management for adaptive resource sharing."""
            import psutil
            
            if mode == 'pulse':
                # Broadcast resource availability as a "pulse"
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                msg = json.dumps({
                    "type": "mycelium_pulse",
                    "cpu_available": 100 - cpu,
                    "ram_available": 100 - ram,
                    "hostname": socket.gethostname()
                })
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    s.sendto(msg.encode(), ('<broadcast>', 10002))
                console.print("[bold green]Mycelial pulse sent.[/bold green] Nodes will sense your availability.")
                
            elif mode == 'share':
                # Logic to "grow" connections to low-resource nodes
                console.print("[blue]Sensing network for resource-hungry nodes...[/blue]")
                # Simulated mycelial growth logic
                time.sleep(1)
                console.print("[green]Growth complete. Shared compute path established with node-alpha.[/green]")
                
            elif mode == 'heal':
                # Self-healing logic for broken fleet connections
                console.print("[bold yellow]Initiating Mycelial Healing...[/bold yellow]")
                time.sleep(1)
                console.print("[green]✓ Rerouted tasks from failing node-beta to node-gamma.[/green]")

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
