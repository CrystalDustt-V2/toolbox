# Installation

ToolBox supports a minimal install by default and optional feature sets (extras) for heavy dependencies.

## Recommended: pipx (Global CLI)

```bash
pipx install toolbox-universal
```

Add extras into the same pipx environment:

```bash
pipx inject toolbox-universal "toolbox-universal[ai]"
pipx inject toolbox-universal "toolbox-universal[desktop]"
pipx inject toolbox-universal "toolbox-universal[security]"
pipx inject toolbox-universal "toolbox-universal[all]"
```

## pip (Installs into your current Python environment)

```bash
pip install toolbox-universal
pip install "toolbox-universal[ai]"
pip install "toolbox-universal[all]"
```

## From Source (Development / Editable)

Run these inside a venv if you want isolation:

```bash
git clone https://github.com/CrystalDustt-V2/toolbox.git
cd toolbox
pip install -e .[dev]
pip install -e .[dev,ai]
pip install -e .[dev,all]
```

## Extras Reference

- `ai`: Whisper/LLM/ONNX/embeddings (heavy)
- `desktop`: dashboard/tray/hotkeys
- `security`: PII audit and hardware-key helpers
- `all`: everything
