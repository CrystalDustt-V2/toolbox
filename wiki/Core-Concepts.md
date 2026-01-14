# Core Concepts

## Offline-First

ToolBox is designed so processing happens locally by default. Many commands wrap local engines (FFmpeg, Tesseract, Poppler, LibreOffice) behind a single CLI surface.

## Command Model

ToolBox exposes a single binary (`toolbox`) with:
- Top-level commands (e.g., `toolbox status`, `toolbox check`)
- Command groups (plugins) (e.g., `toolbox image ...`, `toolbox pdf ...`)

## Plugins

Most functionality lives in plugins under `src/toolbox/plugins/`. Each plugin registers a top-level group and its subcommands at startup.

## Engines

Some commands require external engines. Use:
```bash
toolbox status
toolbox check
```

## Workflows

Workflows run multiple ToolBox commands from a YAML file:
```bash
toolbox workflow run examples/universal_demo.yaml
toolbox workflow watch ./incoming examples/sample_workflow.yaml --ext .pdf --ext .png
toolbox workflow schedule examples/sample_workflow.yaml --interval 60 --immediate
```

## Configuration

Global configuration is managed via:
```bash
toolbox config list
toolbox config set <key> <value>
```

## Logging

Use `--verbose` for debug logs and `--log-file` to persist logs. `--json-log` is intended for machine parsing.
