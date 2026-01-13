import click
import os
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from PIL import Image
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.engine import console
from toolbox.core.io import get_input_path
from toolbox.core.utils import batch_process

class SecurityPlugin(BasePlugin):
    """Plugin for security tasks: Steganography and Secure Vault."""

    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="security",
            commands=["vault-encrypt", "vault-decrypt", "steg-hide", "steg-extract"],
            engine="cryptography/pillow"
        )

    def _get_fernet(self, password: str, salt: bytes = b"toolbox_salt_default") -> Fernet:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)

    def register_commands(self, group: click.Group) -> None:
        @group.group(name="security")
        def security_group():
            """Security and privacy tools."""
            pass

        @security_group.command(name="vault-encrypt")
        @click.argument("input_file")
        @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
        @click.option("-o", "--output", type=click.Path(), help="Output encrypted file")
        def vault_encrypt(input_file: str, password: str, output: Optional[str]):
            """Encrypt a file into a secure vault (.vault)."""
            input_path = Path(input_file)
            output_path = Path(output) if output else input_path.with_suffix(input_path.suffix + ".vault")
            
            fernet = self._get_fernet(password)
            with open(input_path, "rb") as f:
                data = f.read()
            
            encrypted_data = fernet.encrypt(data)
            with open(output_path, "wb") as f:
                f.write(encrypted_data)
            
            console.print(f"[green]✓ File encrypted to {output_path}[/green]")

        @security_group.command(name="vault-decrypt")
        @click.argument("input_file")
        @click.option("--password", prompt=True, hide_input=True)
        @click.option("-o", "--output", type=click.Path(), help="Output decrypted file")
        def vault_decrypt(input_file: str, password: str, output: Optional[str]):
            """Decrypt a .vault file."""
            input_path = Path(input_file)
            output_path = Path(output) if output else input_path.with_suffix("")
            
            fernet = self._get_fernet(password)
            with open(input_path, "rb") as f:
                encrypted_data = f.read()
            
            try:
                decrypted_data = fernet.decrypt(encrypted_data)
                with open(output_path, "wb") as f:
                    f.write(decrypted_data)
                console.print(f"[green]✓ File decrypted to {output_path}[/green]")
            except Exception:
                console.print("[bold red]Error:[/bold red] Invalid password or corrupted vault file.")

        @security_group.command(name="steg-hide")
        @click.argument("image_file")
        @click.argument("secret_file")
        @click.option("-o", "--output", type=click.Path(), help="Output image with hidden data")
        def steg_hide(image_file: str, secret_file: str, output: Optional[str]):
            """Hide a file inside an image using LSB steganography."""
            with get_input_path(image_file) as img_path:
                with Image.open(img_path) as img:
                    img = img.convert("RGBA")
                    pixels = img.load()
                    
                    with open(secret_file, "rb") as f:
                        secret_data = f.read()
                    
                    # Add a header: length of data (4 bytes) + data
                    data_to_hide = len(secret_data).to_bytes(4, "big") + secret_data
                    
                    # Check capacity
                    if len(data_to_hide) * 8 > img.size[0] * img.size[1] * 3:
                        console.print("[bold red]Error:[/bold red] Image too small to hide this file.")
                        return

                    binary_data = "".join(format(b, "08b") for b in data_to_hide)
                    data_idx = 0
                    
                    for y in range(img.size[1]):
                        for x in range(img.size[0]):
                            if data_idx < len(binary_data):
                                r, g, b, a = pixels[x, y]
                                
                                # Hide in R, G, B channels
                                if data_idx < len(binary_data):
                                    r = (r & ~1) | int(binary_data[data_idx])
                                    data_idx += 1
                                if data_idx < len(binary_data):
                                    g = (g & ~1) | int(binary_data[data_idx])
                                    data_idx += 1
                                if data_idx < len(binary_data):
                                    b = (b & ~1) | int(binary_data[data_idx])
                                    data_idx += 1
                                    
                                pixels[x, y] = (r, g, b, a)
                            else:
                                break
                        if data_idx >= len(binary_data):
                            break
                    
                    out_path = output or f"steg_{Path(img_path).name}"
                    img.save(out_path, format="PNG") # Use PNG to avoid compression artifacts
                    console.print(f"[green]✓ Data hidden in {out_path}[/green]")

        @security_group.command(name="steg-extract")
        @click.argument("image_file")
        @click.option("-o", "--output", type=click.Path(), help="Output file for extracted data")
        def steg_extract(image_file: str, output: Optional[str]):
            """Extract hidden data from an image."""
            with get_input_path(image_file) as img_path:
                with Image.open(img_path) as img:
                    img = img.convert("RGBA")
                    pixels = img.load()
                    
                    binary_data = []
                    for y in range(img.size[1]):
                        for x in range(img.size[0]):
                            r, g, b, a = pixels[x, y]
                            binary_data.append(str(r & 1))
                            binary_data.append(str(g & 1))
                            binary_data.append(str(b & 1))
                    
                    binary_str = "".join(binary_data)
                    
                    # Extract header (first 4 bytes / 32 bits)
                    length_bits = binary_str[:32]
                    data_len = int(length_bits, 2)
                    
                    # Extract data
                    data_bits = binary_str[32:32 + (data_len * 8)]
                    extracted_bytes = bytearray()
                    for i in range(0, len(data_bits), 8):
                        extracted_bytes.append(int(data_bits[i:i+8], 2))
                    
                    out_path = output or "extracted_secret"
                    with open(out_path, "wb") as f:
                        f.write(extracted_bytes)
                    
                    console.print(f"[green]✓ Extracted data saved to {out_path}[/green]")
