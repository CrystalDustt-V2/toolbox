# ToolBox CLI

ToolBox is a universal, offline-first CLI suite for file processing, automation, AI-assisted workflows, and security operations.

## What ToolBox Covers

- File operations (hashing, encryption, shredding, watchers)
- Images (convert/resize/crop/EXIF/OCR/remove-bg/upscale)
- Video/audio (FFmpeg-powered conversions and editing)
- PDFs and documents (merge/split/rotate/sanitize/convert)
- Data conversion (JSON/CSV/YAML, SQLite export)
- Security (vaults, steganography, PII audit, verification)
- Networking (download/serve/scan, fleet primitives)
- Automation (workflows: run/watch/schedule)

## Quick Start

```bash
pipx install toolbox-universal

toolbox status
toolbox check
toolbox plugin list
```

## How To Navigate Commands

ToolBox uses a consistent shape:

```bash
toolbox <group> <command> [args/options]
```

Examples:

```bash
toolbox image resize --glob "*.jpg" -w 1280
toolbox pdf merge a.pdf b.pdf -o merged.pdf
toolbox workflow run examples/universal_demo.yaml
```
