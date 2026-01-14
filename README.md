# 🛠️ ToolBox CLI

A universal, offline-first CLI utility suite for file processing, automation, AI-assisted workflows, and security operations. ToolBox wraps common engines (FFmpeg, Tesseract, LibreOffice, Poppler) behind one consistent command surface.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.1-magenta.svg)](#)

---

## 🌟 What You Get

- **Offline-first processing**: files stay local; no required cloud services.
- **Unified CLI surface**: `toolbox <group> <command>` across domains.
- **Batch + automation**: glob processing, watchers, and YAML workflows.
- **Security utilities**: encryption, vaults, shredding, PII audit.
- **Optional AI assist**: local LLM chat/vision, Whisper STT, document indexing.

---

## 🚀 Key Features

- **High-performance batch execution**: parallel-friendly primitives across plugins.
- **Workflow automation**: `toolbox workflow run/watch/schedule` plus YAML variables and branching.
- **Universal input**: many commands accept local paths or URLs.
- **Engine integration**: FFmpeg / Tesseract / Poppler / LibreOffice.
- **Extensible plugin architecture**: discover, list, scaffold plugins.

---

## 🧩 Command Surface

Global commands:

- `toolbox status` / `toolbox check`
- `toolbox config list/set`
- `toolbox plugin list/search/install/create`
- `toolbox workflow run/init/watch/schedule`

Plugins (group → commands):

- **ai** → download, chat, image-gen, vision, index, agent, bci, singularity
- **ambient** → voice, predict, fleet-health, shadow
- **archive** → compress, extract
- **audio** → convert, trim, merge, normalize, stt
- **data** → convert, inspect, sql-export
- **desktop** → install-context-menu, uninstall-context-menu, notify, daemon, dashboard, register-file-type, ar-overlay
- **doc** → convert, inspect
- **file** → hash, rename, batch-rename, info, encrypt, decrypt, shred, watch, compress-ai, semantic-find
- **image** → convert, resize, crop, metadata, ocr, to-sticker, exif-strip, remove-bg, upscale
- **network** → scan, ping, fleet-worker, fleet-status, fleet-dispatch, fleet-api, fleet-parallel, mycelium, mesh-sync
- **pdf** → merge, split, rotate, metadata, extract-text, ocr, sanitize
- **security** → vault-encrypt, vault-decrypt, steg-hide, steg-extract, audit, hardware-setup, mount, vault-announce, vault-discover, quantum-encrypt, quantum-decrypt, verify
- **util** → qr, base64, url, password, case, count, regex, sort, replace, workflow, evolve

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.10+
- External engines (recommended for full features): FFmpeg, Tesseract, Poppler, LibreOffice

### Quick Install
```bash
pip install toolbox-universal
# or using pipx
pipx install toolbox-universal
```

### First Run
```bash
# Verify system readiness and engines
toolbox check

# List the installed plugins and their commands
toolbox plugin list
```

---

## 📖 Usage Examples

### Workflow automation
```bash
toolbox workflow run examples/universal_demo.yaml
toolbox workflow watch ./incoming examples/sample_workflow.yaml --ext .pdf --ext .png
toolbox workflow schedule examples/sample_workflow.yaml --interval 60 --immediate
```

### Common file operations
```bash
toolbox file hash ./big.iso --algorithm sha256
toolbox file shred ./sensitive.txt
toolbox archive compress ./folder -f zip
```

### Media processing
```bash
toolbox image resize --glob "*.jpg" -w 1280
toolbox pdf merge a.pdf b.pdf -o merged.pdf
toolbox video compress input.mp4 -o out.mp4
```

### Security operations
```bash
toolbox security verify
toolbox security audit ./docs
toolbox security vault-encrypt secret.zip --password "your-password"
```

---

## 🛠️ Configuration
Manage your global settings via the CLI:
```bash
toolbox config list
toolbox config set global_bin_path "D:\\portable_tools\\bin"
```

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
ToolBox is designed to be safe-by-default and predictable: it is best used as a local operator for trusted inputs.
