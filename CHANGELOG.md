# ToolBox CLI Changelog

All notable changes to this project will be documented in this file.

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
