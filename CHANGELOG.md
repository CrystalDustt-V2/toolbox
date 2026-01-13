# ToolBox CLI Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-01-13
### Added
- **AI Core Architecture**: Integrated `toolbox.core.ai` for managing local AI models (ONNX, Whisper) and GPU acceleration detection.
- **Image Super-Resolution**: Added `toolbox image upscale` using AI (ESRGAN) with support for 2x and 4x scaling.
- **Speech-to-Text (STT)**: Added `toolbox audio stt` using OpenAI Whisper for offline audio transcription.
- **Advanced Workflow Logic**:
    - Added conditional branching (`if`, `then`, `else`) to YAML workflows.
    - Added variable assignment (`set`) within workflow steps.
    - Enhanced variable substitution with path attributes (e.g., `{file.stem}`, `{file.suffix}`).
- **Security Plugin**:
    - **Steganography**: Added `toolbox security steg-hide` and `steg-extract` to hide/retrieve data in images using LSB.
    - **Secure Vault**: Added `toolbox security vault-encrypt` and `vault-decrypt` for password-protected file containers.
- **GPU Acceleration**: Added global `--gpu` flag to enable hardware acceleration for supported AI tasks.

### Changed
- **Dependency Update**: Added `torch`, `numpy`, `opencv-python`, and `openai-whisper` to core dependencies.
- **Stable Release**: Promotion of `0.3.0-dev` features to stable production status.

## [0.2.1] - 2026-01-13
### Added
- **Module Execution Support**: Added `src/toolbox/__main__.py` allowing the tool to be run via `python -m toolbox`.

### Fixed
- **CLI Entry Point Visibility**: Addressed issues where the `toolbox` command might not be immediately available in the Windows PATH by providing a module-level fallback.

## [0.2.0] - 2026-01-12
### Added
- **High-Performance Concurrency**: Added `--parallel` and `--workers` flags to `batch_process` commands for multi-threaded execution.
- **AI-Powered Image Tools**: Integrated `rembg` for automated background removal (`toolbox image remove-bg`).
- **Security & Privacy Tools**:
    - Added `toolbox file shred` for secure, multi-pass file deletion (DoD 5220.22-M style).
    - Added `toolbox pdf sanitize` to strip metadata and hidden tracking data from PDFs.
    - Added `toolbox file encrypt`/`decrypt` using AES-256-GCM.
- **Advanced Automation**:
    - Added `toolbox workflow watch` for real-time directory monitoring and auto-execution.
    - Added `toolbox workflow schedule` for recurring task execution.
- **Structured Logging**: New logging system with Rich console output and file sinks (`--log-file`).
- **Media Enhancements**: Added `toolbox video watermark` and `toolbox video remove-watermark`.
- **Data Export**: Added `toolbox data sql-export` for converting datasets to SQLite.

### Changed
- **Version Synchronization**: Centralized versioning in `toolbox/__init__.py` and ensured all plugins report the correct version via `PluginMetadata`.
- **Core Refactor**: Standardized all plugins to use Rich console, consistent type hints, and improved error handling.
- **CLI Simplification**: Merged `plugin` and `plugins` command groups and optimized the `status` and `check` commands.
- **File Plugin**: Removed redundant `secure-delete` command in favor of the more robust `shred` (DoD 5220.22-M style).
- **Engine Optimization**: Improved binary path resolution for FFmpeg, Tesseract, and LibreOffice.
- **Input Handling**: Centralized SSRF protection and path resolution in `core/utils.py`.
- **Documentation**: Migrated `changelogs.txt` to `CHANGELOG.md` and updated all repository URLs and PyPI metadata.

### Fixed
- Resolved `NameError` in video/image plugins for `Optional` imports.
- Fixed `KeyError: 'format'` in image sticker generation.
- Corrected test suite assertion failures and permission issues on Windows.

## [0.1.0] - Initial Development
### Added
- Core modular plugin architecture.
- Initial set of plugins: archive, audio, data, doc, file, image, network, pdf, util, video.
- Engine registry system for external tools (FFmpeg, Tesseract, LibreOffice).
- Basic workflow automation (YAML-based).
- Universal URL support for input files.

[0.3.0]: https://github.com/CrystalDustt-V2/toolbox/compare/v0.2.1...master
[0.2.1]: https://github.com/CrystalDustt-V2/toolbox/releases/tag/v0.2.1
[0.2.0]: https://github.com/CrystalDustt-V2/toolbox/releases/tag/v0.2.0
[0.1.0]: https://github.com/CrystalDustt-V2/toolbox/releases/tag/v0.1.0
