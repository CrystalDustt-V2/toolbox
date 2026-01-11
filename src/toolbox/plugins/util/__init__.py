import click
import qrcode
import base64
import urllib.parse
import secrets
import string
import re
from pathlib import Path
from toolbox.core.plugin import BasePlugin, PluginMetadata
from toolbox.core.io import get_input_path

class UtilPlugin(BasePlugin):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="util",
            commands=["qr", "base64", "url", "password", "case", "count", "regex", "sort", "replace"],
            engine="python"
        )

    def register_commands(self, group):
        @group.group(name="util")
        def util_group():
            """General utility tools."""
            pass

        @util_group.command(name="qr")
        @click.argument("text")
        @click.option("-o", "--output", default="qrcode.png", help="Output filename")
        def generate_qr(text, output):
            """Generate a QR code from text."""
            img = qrcode.make(text)
            img.save(output)
            click.echo(f"QR code saved to {output}")

        @util_group.group(name="base64")
        def b64_group():
            """Base64 encoding/decoding."""
            pass

        @b64_group.command(name="encode")
        @click.argument("text")
        def b64_encode(text):
            """Encode text to Base64."""
            encoded = base64.b64encode(text.encode()).decode()
            click.echo(encoded)

        @b64_group.command(name="decode")
        @click.argument("encoded_text")
        def b64_decode(encoded_text):
            """Decode Base64 text."""
            try:
                decoded = base64.b64decode(encoded_text.encode()).decode()
                click.echo(decoded)
            except Exception as e:
                click.echo(f"Error decoding: {e}")

        @util_group.group(name="url")
        def url_group():
            """URL encoding/decoding."""
            pass

        @url_group.command(name="encode")
        @click.argument("text")
        def url_encode(text):
            """URL encode text."""
            click.echo(urllib.parse.quote(text))

        @url_group.command(name="decode")
        @click.argument("text")
        def url_decode(text):
            """URL decode text."""
            click.echo(urllib.parse.unquote(text))

        @util_group.command(name="password")
        @click.option("-l", "--length", type=int, default=16, help="Password length")
        @click.option("--no-symbols", is_flag=True, help="Exclude symbols")
        def gen_password(length, no_symbols):
            """Generate a secure random password."""
            chars = string.ascii_letters + string.digits
            if not no_symbols:
                chars += string.punctuation
            
            password = "".join(secrets.choice(chars) for _ in range(length))
            click.echo(password)

        @util_group.command(name="case")
        @click.argument("text")
        @click.option("--to", type=click.Choice(["upper", "lower", "title"]), default="upper")
        def change_case(text, to):
            """Change text case."""
            if to == "upper":
                click.echo(text.upper())
            elif to == "lower":
                click.echo(text.lower())
            elif to == "title":
                click.echo(text.title())

        @util_group.command(name="count")
        @click.argument("text", required=False)
        @click.option("-f", "--file", help="Input file (Local or URL)")
        def count_text(text, file):
            """Count words, characters, and lines."""
            content = ""
            if file:
                with get_input_path(file) as path:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
            elif text:
                content = text
            else:
                click.echo("Please provide text or a file.")
                return

            chars = len(content)
            words = len(content.split())
            lines = len(content.splitlines())
            
            click.echo(f"Lines: {lines}")
            click.echo(f"Words: {words}")
            click.echo(f"Characters: {chars}")

        @util_group.command(name="regex")
        @click.argument("pattern")
        @click.argument("input_file")
        def regex_extract(pattern, input_file):
            """Extract text using regex pattern. Supports local or URL."""
            with get_input_path(input_file) as path:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            
            matches = re.findall(pattern, content)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        click.echo("\t".join(match))
                    else:
                        click.echo(match)
            else:
                click.echo("No matches found.")

        @util_group.command(name="sort")
        @click.argument("input_file")
        @click.option("-o", "--output", help="Output file (default: overwrite if local)")
        @click.option("-u", "--unique", is_flag=True, help="Remove duplicates")
        @click.option("-r", "--reverse", is_flag=True, help="Reverse sort order")
        def sort_lines(input_file, output, unique, reverse):
            """Sort lines in a text file. Supports local or URL."""
            with get_input_path(input_file) as path:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            
            if unique:
                lines = list(set(lines))
            
            lines.sort(reverse=reverse)
            
            target = output or (input_file if not input_file.startswith(("http://", "https://")) else "sorted_output.txt")
            with open(target, "w", encoding="utf-8") as f:
                f.writelines(lines)
            click.echo(f"Sorted lines written to {target}")

        @util_group.command(name="replace")
        @click.argument("search")
        @click.argument("replacement")
        @click.argument("input_file")
        @click.option("-o", "--output", help="Output file (default: overwrite if local)")
        @click.option("-i", "--ignore-case", is_flag=True, help="Ignore case")
        def replace_text(search, replacement, input_file, output, ignore_case):
            """Find and replace text in a file. Supports local or URL."""
            with get_input_path(input_file) as path:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            
            flags = re.IGNORECASE if ignore_case else 0
            new_content = re.sub(search, replacement, content, flags=flags)
            
            target = output or (input_file if not input_file.startswith(("http://", "https://")) else "replaced_output.txt")
            with open(target, "w", encoding="utf-8") as f:
                f.write(new_content)
            click.echo(f"Replacements done and written to {target}")
