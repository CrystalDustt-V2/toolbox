from __future__ import annotations

import re
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import click

from toolbox.cli import cli as root_cli


@dataclass(frozen=True)
class CommandNode:
    path: tuple[str, ...]
    command: click.Command
    aliases: tuple[str, ...]


def _slug_from_page_name(page_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "-", page_name).strip("-")


def _page_name_for_path(path: tuple[str, ...]) -> str:
    if not path:
        return "Command-Index"
    return "Command-" + "-".join(path)


def _wiki_link(page_name: str, text: str | None = None) -> str:
    slug = _slug_from_page_name(page_name)
    label = text or page_name
    return f"[{label}]({slug})"


def _command_info_name(path: tuple[str, ...]) -> str:
    if not path:
        return "toolbox"
    return "toolbox " + " ".join(path)


def _help_text(command: click.Command, path: tuple[str, ...]) -> str:
    ctx = click.Context(command, info_name=_command_info_name(path))
    return command.get_help(ctx)


def _param_signature(command: click.Command, path: tuple[str, ...]) -> str:
    ctx = click.Context(command, info_name=_command_info_name(path))
    usage = ctx.command_path
    parts: list[str] = [usage]

    for param in command.get_params(ctx):
        if isinstance(param, click.Option) and param.name == "help":
            continue
        if isinstance(param, click.Option):
            if param.is_flag:
                parts.append(f"[{param.opts[0]}]")
            elif param.nargs == 1:
                metavar = (param.make_metavar(ctx) or "VALUE").strip()
                opt = param.opts[0]
                parts.append(f"[{opt} {metavar}]")
            else:
                opt = param.opts[0]
                parts.append(f"[{opt} ...]")
        elif isinstance(param, click.Argument):
            metavar = (param.make_metavar(ctx) or param.name.upper()).strip()
            parts.append(metavar)

    return " ".join(parts)


def _examples(command: click.Command, path: tuple[str, ...]) -> list[str]:
    examples: list[str] = []

    args: list[str] = []
    opts: list[str] = []

    for param in command.params:
        if isinstance(param, click.Argument):
            if param.nargs == -1:
                args.append(f"<{param.name}>...")
            else:
                args.append(f"<{param.name}>")
        elif isinstance(param, click.Option):
            if param.is_flag:
                opts.append(param.opts[0])
            else:
                opts.append(f"{param.opts[0]} <{param.name}>")

    base = "toolbox " + " ".join(path)
    if args:
        examples.append(" ".join([base, *args]))
    if opts:
        examples.append(" ".join([base, *opts[:2], *args][: 1 + min(2, len(opts)) + len(args)]))
    if args and opts:
        examples.append(" ".join([base, *opts[:2], *args]))

    return list(dict.fromkeys(examples))


def _walk_commands(group: click.Group) -> list[CommandNode]:
    nodes: list[CommandNode] = []

    def rec(parent_path: tuple[str, ...], g: click.Group) -> None:
        seen: dict[int, str] = {}
        aliases: dict[str, list[str]] = {}

        for name in sorted(g.commands.keys()):
            cmd = g.commands[name]
            cmd_id = id(cmd)
            if cmd_id in seen:
                canonical = seen[cmd_id]
                aliases.setdefault(canonical, []).append(name)
                continue
            seen[cmd_id] = name

        for name in sorted(seen.values()):
            cmd = g.commands[name]
            path = (*parent_path, name)
            node_aliases = tuple(sorted(set(aliases.get(name, []))))
            nodes.append(CommandNode(path=path, command=cmd, aliases=node_aliases))
            if isinstance(cmd, click.Group):
                rec(path, cmd)

    rec((), group)
    return nodes


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.replace("\r\n", "\n"), encoding="utf-8")


def _render_home(nodes: list[CommandNode]) -> str:
    top_groups = sorted(
        [n for n in nodes if len(n.path) == 1 and isinstance(n.command, click.Group)],
        key=lambda n: n.path[0],
    )
    group_links = "\n".join(f"- {_wiki_link(_page_name_for_path(n.path), f'toolbox {n.path[0]}')}" for n in top_groups)

    return "\n".join(
        [
            "# ToolBox CLI Wiki",
            "",
            "ToolBox is a universal, offline-first CLI utility suite for file processing, automation, AI-assisted workflows, and security operations.",
            "",
            "## Installation",
            "",
            f"- {_wiki_link('Installation', 'Install ToolBox (minimal vs extras)')}",
            "",
            "## Core Concepts",
            "",
            f"- {_wiki_link('Core-Concepts', 'How ToolBox is structured')}",
            "",
            "## Command Shape",
            "",
            "```bash",
            "toolbox [global-options] <group|command> [subcommand] [args/options]",
            "```",
            "",
            "## Start Here",
            "",
            f"- {_wiki_link('Command-Index', 'Command Index')}",
            f"- {_wiki_link('Publishing-to-GitHub-Wiki', 'Publishing this Wiki')}",
            "",
            "## Groups",
            "",
            group_links,
            "",
        ]
    )


def _render_installation() -> str:
    return "\n".join(
        [
            "# Installation",
            "",
            "ToolBox supports a minimal install by default and optional feature sets (extras) for heavy dependencies.",
            "",
            "## Recommended: pipx (Global CLI)",
            "",
            "```bash",
            "pipx install toolbox-universal",
            "```",
            "",
            "Add extras into the same pipx environment:",
            "",
            "```bash",
            "pipx inject toolbox-universal \"toolbox-universal[ai]\"",
            "pipx inject toolbox-universal \"toolbox-universal[desktop]\"",
            "pipx inject toolbox-universal \"toolbox-universal[security]\"",
            "pipx inject toolbox-universal \"toolbox-universal[all]\"",
            "```",
            "",
            "## pip (Installs into your current Python environment)",
            "",
            "```bash",
            "pip install toolbox-universal",
            "pip install \"toolbox-universal[ai]\"",
            "pip install \"toolbox-universal[all]\"",
            "```",
            "",
            "## From Source (Development / Editable)",
            "",
            "Run these inside a venv if you want isolation:",
            "",
            "```bash",
            "git clone https://github.com/CrystalDustt-V2/toolbox.git",
            "cd toolbox",
            "pip install -e .[dev]",
            "pip install -e .[dev,ai]",
            "pip install -e .[dev,all]",
            "```",
            "",
            "## Extras Reference",
            "",
            "- `ai`: Whisper/LLM/ONNX/embeddings (heavy)",
            "- `desktop`: dashboard/tray/hotkeys", 
            "- `security`: PII audit and hardware-key helpers",
            "- `all`: everything",
            "",
        ]
    )


def _github_source_link(command: click.Command) -> str | None:
    callback = getattr(command, "callback", None)
    if callback is None:
        return None
    src = inspect.getsourcefile(callback)
    if src is None:
        return None
    project_root = Path(__file__).resolve().parents[1]
    try:
        rel = Path(src).resolve().relative_to(project_root)
    except ValueError:
        return None
    try:
        line = inspect.getsourcelines(callback)[1]
    except OSError:
        line = 1
    url = f"https://github.com/CrystalDustt-V2/toolbox/blob/master/{rel.as_posix()}#L{line}"
    label = f"{rel.as_posix()}:L{line}"
    return f"[{label}]({url})"


def _render_core_concepts() -> str:
    return "\n".join(
        [
            "# Core Concepts",
            "",
            "## Offline-First",
            "",
            "ToolBox is designed so processing happens locally by default. Many commands wrap local engines (FFmpeg, Tesseract, Poppler, LibreOffice) behind a single CLI surface.",
            "",
            "## Command Model",
            "",
            "ToolBox exposes a single binary (`toolbox`) with:",
            "- Top-level commands (e.g., `toolbox status`, `toolbox check`)",
            "- Command groups (plugins) (e.g., `toolbox image ...`, `toolbox pdf ...`)",
            "",
            "## Plugins",
            "",
            "Most functionality lives in plugins under `src/toolbox/plugins/`. Each plugin registers a top-level group and its subcommands at startup.",
            "",
            "## Engines",
            "",
            "Some commands require external engines. Use:",
            "```bash",
            "toolbox status",
            "toolbox check",
            "```",
            "",
            "## Workflows",
            "",
            "Workflows run multiple ToolBox commands from a YAML file:",
            "```bash",
            "toolbox workflow run examples/universal_demo.yaml",
            "toolbox workflow watch ./incoming examples/sample_workflow.yaml --ext .pdf --ext .png",
            "toolbox workflow schedule examples/sample_workflow.yaml --interval 60 --immediate",
            "```",
            "",
            "## Configuration",
            "",
            "Global configuration is managed via:",
            "```bash",
            "toolbox config list",
            "toolbox config set <key> <value>",
            "```",
            "",
            "## Logging",
            "",
            "Use `--verbose` for debug logs and `--log-file` to persist logs. `--json-log` is intended for machine parsing.",
            "",
        ]
    )


def _render_command_index(nodes: list[CommandNode]) -> str:
    top_level = [n for n in nodes if len(n.path) == 1]
    groups = [n for n in top_level if isinstance(n.command, click.Group)]
    commands = [n for n in top_level if not isinstance(n.command, click.Group)]

    lines: list[str] = [
        "# Command Index",
        "",
        "## Global Options",
        "",
        "```bash",
        "toolbox --help",
        "```",
        "",
        "```text",
        _help_text(root_cli, ()),
        "```",
        "",
        "## Command Groups",
        "",
    ]

    for g in sorted(groups, key=lambda n: n.path[0]):
        lines.append(f"- {_wiki_link(_page_name_for_path(g.path), 'toolbox ' + g.path[0])} — {g.command.help or g.command.short_help or ''}")

    lines.extend(["", "## Top-Level Commands", ""]) 
    for c in sorted(commands, key=lambda n: n.path[0]):
        lines.append(f"- {_wiki_link(_page_name_for_path(c.path), 'toolbox ' + c.path[0])} — {c.command.help or c.command.short_help or ''}")

    lines.append("")
    return "\n".join(lines)


def _render_group_page(node: CommandNode, children: list[CommandNode]) -> str:
    title = "toolbox " + " ".join(node.path)
    page_name = _page_name_for_path(node.path)
    lines: list[str] = [
        f"# {title}",
        "",
        (node.command.help or node.command.short_help or "").strip(),
        "",
    ]

    if node.aliases:
        lines.extend(["Aliases: " + ", ".join(f"`toolbox {' '.join(node.path[:-1] + (a,))}`" for a in node.aliases), ""]) 

    subcommands = [c for c in children if len(c.path) == len(node.path) + 1]
    if subcommands:
        lines.extend(["## Subcommands", ""]) 
        for sc in sorted(subcommands, key=lambda n: n.path[-1]):
            lines.append(
                f"- {_wiki_link(_page_name_for_path(sc.path), 'toolbox ' + ' '.join(sc.path))} — {sc.command.help or sc.command.short_help or ''}"
            )
        lines.append("")

    lines.extend(
        [
            "## Help",
            "",
            "```text",
            _help_text(node.command, node.path),
            "```",
            "",
            f"Back: {_wiki_link('Command-Index', 'Command Index')}",
            "",
        ]
    )

    return "\n".join(lines)


def _render_command_page(node: CommandNode) -> str:
    title = "toolbox " + " ".join(node.path)
    source_link = _github_source_link(node.command)
    lines: list[str] = [
        f"# {title}",
        "",
        (node.command.help or node.command.short_help or "").strip(),
        "",
    ]

    if source_link:
        lines.extend([f"Source: {source_link}", ""]) 

    if node.aliases:
        lines.extend(["Aliases: " + ", ".join(f"`toolbox {' '.join(node.path[:-1] + (a,))}`" for a in node.aliases), ""]) 

    lines.extend(["## Synopsis", "", "```bash", _param_signature(node.command, node.path), "```", ""]) 

    examples = _examples(node.command, node.path)
    if examples:
        lines.extend(["## Examples", "", "```bash", *examples, "```", ""]) 

    lines.extend(["## Help", "", "```text", _help_text(node.command, node.path), "```", ""]) 

    if len(node.path) > 1:
        parent = node.path[:-1]
        lines.append(f"Parent: {_wiki_link(_page_name_for_path(parent), 'toolbox ' + ' '.join(parent))}")
    lines.append(f"Back: {_wiki_link('Command-Index', 'Command Index')}")
    lines.append("")

    return "\n".join(lines)


def _render_sidebar(nodes: list[CommandNode]) -> str:
    top_groups = sorted(
        [n for n in nodes if len(n.path) == 1 and isinstance(n.command, click.Group)],
        key=lambda n: n.path[0],
    )

    lines = [
        "- " + _wiki_link("Home", "Home"),
        "- " + _wiki_link("Installation", "Installation"),
        "- " + _wiki_link("Core-Concepts", "Core Concepts"),
        "- " + _wiki_link("Command-Index", "Command Index"),
        "- " + _wiki_link("Publishing-to-GitHub-Wiki", "Publishing"),
        "",
        "## Groups",
        "",
    ]
    for g in top_groups:
        lines.append("- " + _wiki_link(_page_name_for_path(g.path), f"toolbox {g.path[0]}"))
    lines.append("")
    return "\n".join(lines)


def _render_publishing_page() -> str:
    return "\n".join(
        [
            "# Publishing to GitHub Wiki",
            "",
            "GitHub Wikis are backed by a separate git repository (`<repo>.wiki.git`). This project keeps wiki sources in the `wiki/` folder so you can generate/update pages locally, then push them to the wiki repo.",
            "",
            "## If You See 'Repository not found'",
            "",
            "That usually means one of these is true:",
            "- The wiki feature is disabled in the main repo settings.",
            "- The wiki repo exists, but you don't have access (private repo / auth required).",
            "",
            "Fix:",
            "- Enable Wikis in the repository settings (GitHub UI).",
            "- Create the first wiki page in the GitHub UI (this initializes the wiki git repo).",
            "- Then clone/push again. For private repos, use an authenticated remote (PAT) or SSH.",
            "",
            "## One-Time Setup",
            "",
            "```bash",
            "git clone https://github.com/CrystalDustt-V2/toolbox.wiki.git",
            "```",
            "",
            "## Publish / Update",
            "",
            "```bash",
            "python tools/generate_github_wiki.py --out wiki",
            "cd toolbox.wiki",
            "git rm -r --ignore-unmatch .",
            "cp -r ../wiki/* .",
            "git add -A",
            "git commit -m \"Update wiki\"",
            "git push",
            "```",
            "",
            "## Windows PowerShell Variant",
            "",
            "```powershell",
            "python tools/generate_github_wiki.py --out wiki",
            "cd toolbox.wiki",
            "git rm -r --ignore-unmatch .",
            "Copy-Item -Recurse -Force ..\\wiki\\* .",
            "git add -A",
            "git commit -m \"Update wiki\"",
            "git push",
            "```",
            "",
        ]
    )


def generate(out_dir: Path) -> int:
    nodes = _walk_commands(root_cli)
    by_path = {n.path: n for n in nodes}

    _write(out_dir / "Home.md", _render_home(nodes))
    _write(out_dir / "Installation.md", _render_installation())
    _write(out_dir / "Command-Index.md", _render_command_index(nodes))
    _write(out_dir / "_Sidebar.md", _render_sidebar(nodes))
    _write(out_dir / "Publishing-to-GitHub-Wiki.md", _render_publishing_page())
    _write(out_dir / "Core-Concepts.md", _render_core_concepts())

    children_by_prefix: dict[tuple[str, ...], list[CommandNode]] = {}
    for n in nodes:
        if len(n.path) >= 2:
            prefix = n.path[:-1]
            children_by_prefix.setdefault(prefix, []).append(n)

    for node in nodes:
        page = _page_name_for_path(node.path) + ".md"
        if isinstance(node.command, click.Group):
            children = children_by_prefix.get(node.path, [])
            content = _render_group_page(node, children)
        else:
            content = _render_command_page(node)
        _write(out_dir / page, content)

    return len(nodes) + 6


@click.command()
@click.option("--out", "out", type=click.Path(path_type=Path), default=Path("wiki"), show_default=True)
def main(out: Path) -> None:
    count = generate(out)
    click.echo(f"Generated {count} wiki pages in {out}")


if __name__ == "__main__":
    main()
