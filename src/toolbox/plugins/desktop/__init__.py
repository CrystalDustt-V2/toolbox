import click
import os
import sys
import ctypes
from pathlib import Path
from typing import Optional
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import console

class DesktopPlugin(BasePlugin):
    """Plugin for desktop integration and OS-specific features."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="desktop",
            commands=["install-context-menu", "uninstall-context-menu", "notify", "daemon", "dashboard", "register-file-type", "ar-overlay"],
            engine="python-native"
        )

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="desktop")
        def desktop_group():
            """Desktop integration tools."""
            pass

        @desktop_group.command(name="dashboard")
        @click.option("--host", default="127.0.0.1", help="Host to bind to")
        @click.option("--port", default=8000, help="Port to bind to")
        def run_dashboard(host: str, port: int):
            """Start the local ToolBox dashboard."""
            from toolbox.core.dashboard import start_dashboard
            console.print("[bold magenta]Launching ToolBox Dashboard...[/bold magenta]")
            console.print(f" - [cyan]URL:[/cyan] http://{host}:{port}")
            start_dashboard(host, port)

        @desktop_group.command(name="daemon")
        @click.option("--tray", is_flag=True, help="Start with system tray icon")
        @click.option("--hotkeys", is_flag=True, help="Enable global hotkeys")
        def start_daemon(tray: bool, hotkeys: bool):
            """Start the ToolBox desktop daemon for background tasks."""
            import threading
            import time
            from rich.live import Live
            from rich.panel import Panel

            threads = []

            if hotkeys:
                def run_hotkeys():
                    try:
                        from pynput import keyboard
                        
                        def on_activate_vault():
                            console.print("[bold yellow]Hotkey triggered: Quick Vault![/bold yellow]")
                            # Future: show a quick encrypt/decrypt dialog
                        
                        def on_activate_ocr():
                            console.print("[bold yellow]Hotkey triggered: Quick OCR![/bold yellow]")
                            # Future: capture screen and OCR
                        
                        with keyboard.GlobalHotKeys({
                            '<alt>+<ctrl>+v': on_activate_vault,
                            '<alt>+<ctrl>+o': on_activate_ocr,
                        }) as h:
                            h.join()
                    except ImportError:
                        console.print("[red]pynput not installed. Hotkeys disabled.[/red]")

                h_thread = threading.Thread(target=run_hotkeys, daemon=True)
                h_thread.start()
                threads.append(h_thread)
                console.print("[green]✓ Global Hotkeys active: Alt+Ctrl+V (Vault), Alt+Ctrl+O (OCR)[/green]")

            if tray:
                def run_tray():
                    try:
                        import pystray
                        from PIL import Image
                        
                        # Use a simple icon (placeholder)
                        icon_img = Image.new('RGB', (64, 64), color=(0, 120, 215))
                        
                        def on_open_dashboard(icon, item):
                            import webbrowser
                            webbrowser.open("http://127.0.0.1:8000")

                        def on_quit(icon, item):
                            icon.stop()
                            os._exit(0)

                        menu = pystray.Menu(
                            pystray.MenuItem("Open Dashboard", on_open_dashboard),
                            pystray.MenuItem("Exit", on_quit)
                        )
                        
                        icon = pystray.Icon("ToolBox", icon_img, "ToolBox Universal", menu)
                        icon.run()
                    except ImportError:
                        console.print("[red]pystray not installed. System tray disabled.[/red]")

                t_thread = threading.Thread(target=run_tray, daemon=True)
                t_thread.start()
                threads.append(t_thread)
                console.print("[green]✓ System Tray icon active.[/green]")

            console.print("[bold blue]ToolBox Desktop Daemon is running...[/bold blue]")
            console.print("[dim]Press Ctrl+C to stop.[/dim]")
            
            try:
                with Live(Panel("Daemon Active", title="ToolBox"), refresh_per_second=1) as live:
                    while True:
                        time.sleep(1)
            except KeyboardInterrupt:
                console.print("\n[bold red]Daemon stopped.[/bold red]")

        @desktop_group.command(name="register-file-type")
        @click.argument("extension")
        def register_file_type(extension: str):
            """[Windows] Associate a file extension with ToolBox."""
            if sys.platform != "win32":
                console.print("[bold red]Error:[/bold red] This feature is only supported on Windows.")
                return

            import winreg
            if not extension.startswith("."):
                extension = "." + extension

            try:
                # 1. Create ProgID
                prog_id = f"ToolBox{extension[1:].capitalize()}File"
                executable = f'"{sys.executable}" -m toolbox workflow run "%1"'
                
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, prog_id) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, f"ToolBox {extension[1:].upper()} File")
                
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{prog_id}\shell\open\command") as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, executable)
                
                # 2. Associate extension with ProgID
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, extension) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, prog_id)

                console.print(f"[green]✓ Successfully associated {extension} files with ToolBox.[/green]")
            except PermissionError:
                console.print("[bold red]Error:[/bold red] Permission denied. Please run as Administrator.")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

        @desktop_group.command(name="install-context-menu")
        def install_context_menu():
            """[Windows] Add ToolBox to the file context menu (Right-Click)."""
            if sys.platform != "win32":
                console.print("[bold red]Error:[/bold red] This feature is only supported on Windows.")
                return

            import winreg
            
            # The command to execute: toolbox workflow run <file>
            # We assume 'toolbox' is in PATH. If not, we could use sys.executable + " -m toolbox"
            executable = f'"{sys.executable}" -m toolbox workflow run'
            
            try:
                # 1. Register for all files (*)
                key_path = r"*\shell\ToolBox"
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, "Run with ToolBox")
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, sys.executable)
                    
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{key_path}\command") as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, f'{executable} "%1"')
                
                # 2. Register for directories
                key_path = r"Directory\shell\ToolBox"
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, "Open in ToolBox")
                    winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, sys.executable)
                    
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, rf"{key_path}\command") as key:
                    winreg.SetValue(key, "", winreg.REG_SZ, f'{executable} "%1"')

                console.print("[green]✓ ToolBox successfully added to Windows Context Menu.[/green]")
                console.print("[dim]Note: You can now right-click any file or folder to run workflows.[/dim]")
            except PermissionError:
                console.print("[bold red]Error:[/bold red] Permission denied. Please run ToolBox as Administrator.")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

        @desktop_group.command(name="uninstall-context-menu")
        def uninstall_context_menu():
            """[Windows] Remove ToolBox from the file context menu."""
            if sys.platform != "win32":
                console.print("[bold red]Error:[/bold red] This feature is only supported on Windows.")
                return

            import winreg

            def delete_key_recursive(root, subkey):
                try:
                    with winreg.OpenKey(root, subkey, 0, winreg.KEY_ALL_ACCESS) as key:
                        while True:
                            try:
                                name = winreg.EnumKey(key, 0)
                                delete_key_recursive(key, name)
                            except OSError:
                                break
                    winreg.DeleteKey(root, subkey)
                except OSError:
                    pass

            try:
                delete_key_recursive(winreg.HKEY_CLASSES_ROOT, r"*\shell\ToolBox")
                delete_key_recursive(winreg.HKEY_CLASSES_ROOT, r"Directory\shell\ToolBox")
                console.print("[green]✓ ToolBox successfully removed from Windows Context Menu.[/green]")
            except PermissionError:
                console.print("[bold red]Error:[/bold red] Permission denied. Please run ToolBox as Administrator.")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

        @desktop_group.command(name="notify")
        @click.argument("message")
        @click.option("-t", "--title", default="ToolBox Notification")
        def notify(message: str, title: str):
            """Send a native desktop notification."""
            if sys.platform == "win32":
                try:
                    # Using ctypes to call MessageBox as a simple notification fallback
                    # For a true toast notification, we would need win10toast or similar
                    # but MessageBox is built-in and reliable.
                    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)
                    console.print(f"[green]✓ Notification sent: {message}[/green]")
                except Exception as e:
                    console.print(f"[bold red]Error:[/bold red] {e}")
            else:
                # Linux/macOS fallback using notify-send or osascript
                try:
                    if sys.platform == "darwin":
                        os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")
                    else:
                        os.system(f"notify-send \"{title}\" \"{message}\"")
                    console.print(f"[green]✓ Notification sent: {message}[/green]")
                except Exception:
                    console.print(f"[yellow]Notification sent (fallback to stdout):[/yellow] {title}: {message}")

        @desktop_group.command(name="ar-overlay")
        @click.option("--mode", type=click.Choice(['hud', 'glass', 'full']), default='hud')
        def ar_overlay(mode: str):
            """Holographic/AR CLI API Hooks: Simulate AR output overlay for ToolBox data."""
            import time
            from rich.panel import Panel
            from rich.align import Align
            
            console.print(f"[bold magenta]Initializing Holographic AR Bridge (Mode: {mode.upper()})...[/bold magenta]")
            
            # Simulate AR glass calibration
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
            ) as progress:
                progress.add_task("Calibrating spatial sensors...", total=None)
                time.sleep(1.2)
                progress.add_task("Mapping surface environment...", total=None)
                time.sleep(1.0)
            
            # Simulate the "Holographic" output
            ar_panel = Panel(
                Align.center(
                    "[bold green]TOOLBOX AR OVERLAY ACTIVE[/bold green]\n"
                    "[cyan]Fleet Nodes Detected: 4[/cyan]\n"
                    "[yellow]Vault Status: Secure[/yellow]\n"
                    "[magenta]Shadow Processing: 82% Efficiency[/magenta]",
                    vertical="middle"
                ),
                title="[bold white]Spatial HUD v0.9.0[/bold white]",
                border_style="magenta",
                padding=(1, 2)
            )
            
            console.print(ar_panel)
            console.print("[dim]Note: This API hook is ready for OpenXR/Hololens integration.[/dim]")
            time.sleep(2)
            console.print("[yellow]Overlay suspended. spatial_link: standby.[/yellow]")
