# ToolBox CLI Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-14
### Added
- **ToolBox Singularity (Phase 10 - Stable Release)**:
    - **Unified Intelligence Core**: Added `toolbox ai singularity` to orchestrate all Phase 1-9 systems with optional full autonomy.
    - **Hardened Security Audit**: Added `toolbox security verify` to validate all cryptographic primitives and hardware-bound keys.
    - **Omni-Interface Dashboard**: Enhanced `toolbox desktop dashboard` to v1.0.0 with unified fleet and security management.
    - **Production Stability**: Finalized all core engines and dependency paths for stable release.

## [0.9.0-dev] - 2026-01-14
### Added
- **Predictive Pre-Computation & Global Sync (Phase 9)**:
    - **Predictive Pre-Computation**: Added `toolbox ambient shadow` for background "shadow-processing" based on AI heuristics.
    - **Global Mesh Sync**: Added `toolbox network mesh-sync` using DHT-based discovery for global vault synchronization.
    - **Semantic File Discovery**: Added `toolbox file semantic-find` for neural-search based on file content meaning.
    - **Holographic CLI API**: Added `toolbox desktop ar-overlay` hooks for spatial computing and AR HUD integration.

## [0.8.0-dev] - 2026-01-14
### Added
- **Autonomous Self-Evolution & Biological Logic (Phase 8)**:
    - **Self-Optimizing JIT Heuristics**: Added `profile_engine` decorator to `BaseEngine` for performance telemetry and adaptive micro-optimization.
    - **Mycelial Fleet Management**: Added `toolbox network mycelium` with `pulse`, `share`, and `heal` modes for biological-inspired resource distribution.
    - **Genetic Workflow Optimizer**: Added `toolbox util evolve` to benchmark and evolve workflow execution profiles via simulated genetic mutation.
    - **BCI Foundation**: Added `toolbox ai bci` for simulated Brain-Computer Interface intent detection and thought-to-command execution.

## [0.7.0-dev] - 2026-01-14
### Added
- **Quantum-Ready Security & Hyper-Scale Parallelism (Phase 7)**:
    - **Quantum-Resistant Hybrid Encryption**: Added `toolbox security quantum-encrypt` using hardware-bound AES-256-GCM.
    - **Hyper-Scale Parallelism**: Added `toolbox network fleet-parallel` to distribute massive file batches across all active fleet nodes.
    - **Immutable Audit Ledger**: Implemented hash-chained logging in `toolbox.ledger` for tamper-proof activity tracking.
    - **Neural Compression**: Added `toolbox file compress-ai` using multi-stage hybrid delta encoding.

## [0.6.0-dev] - 2026-01-14
### Added
- **Ambient Intelligence & Natural Interface (Phase 6)**:
    - **Voice-to-Fleet**: Added `toolbox ambient voice` for offline voice command execution via Whisper and AI Agents.
    - **Predictive Automation**: Added `toolbox ambient predict` to analyze usage patterns and suggest workflow optimizations.
    - **Self-Healing Fleet**: Added `toolbox ambient fleet-health` with telemetry support in `fleet-worker` for node monitoring and re-routing.
    - **Fleet Visualization**: Enhanced network telemetry with CPU/RAM metrics for distributed nodes.

## [0.5.0-dev] - 2026-01-14
### Added
- **Distributed Edge & Collaborative Intelligence (Phase 5)**:
    - **P2P Task Offloading**: Added `toolbox network fleet-worker` and `fleet-dispatch` to share compute across local nodes.
    - **Mesh Storage Discovery**: Added `toolbox security vault-announce` and `vault-discover` for P2P vault sharing.
    - **Local API Gateway**: Added `toolbox network fleet-api` (FastAPI) for remote control and fleet orchestration.
    - **Fleet Telemetry**: Added `toolbox network fleet-status` for real-time node discovery using UDP broadcasting.
- **Autonomous Agents & Workflow Orchestration (Phase 4)**:
    - **AI Agent Core**: Added `toolbox ai agent` for autonomous command execution based on high-level goals.
    - **Dynamic Workflow Engine**: Added `toolbox util workflow` with support for variables, `if/else` logic, and task registration.
    - **Event-Driven Triggers**: Added `toolbox file watch` using `watchdog` to trigger ToolBox commands automatically on file changes.
- **Fortified Security & Privacy (Phase 3)**:
    - **Privacy Audit Engine**: Added `toolbox security audit` to detect PII (emails, phones, credit cards) in local files using `presidio-analyzer`.
    - **Encrypted Virtual Drives**: Added `toolbox security mount` to securely mount vaults as temporary virtual drives (with `subst` support on Windows).
    - **Hardware-Backed Security**: Added `toolbox security hardware-setup` foundation for FIDO2/YubiKey authentication.
- **Intelligent Edge Computing (Phase 2)**:
    - **Local LLM Integration**: Added `toolbox ai chat` with **RAG (Retrieval-Augmented Generation)** support using `FAISS` and `sentence-transformers`.
    - **Vision LLM support**: Added `toolbox ai vision` using **LLaVA v1.5** for local image description and analysis.
    - **Document Indexing**: Added `toolbox ai index` to create local vector databases from TXT, MD, and PDF files.
    - **Local Image Generation**: Added `toolbox ai image-gen` using **Stable Diffusion ONNX** for offline text-to-image creation.
    - **Intelligent Engine Routing**: Implemented hardware telemetry (CPU/GPU/RAM) to automatically route AI tasks to the most efficient provider.
- **Desktop Experience (Phase 1)**:
    - **System Tray Integration**: Added `toolbox desktop daemon --tray` for quick access and background persistence.
    - **Global Hotkeys**: Added `toolbox desktop daemon --hotkeys` with initial shortcuts for Vault (`Alt+Ctrl+V`) and OCR (`Alt+Ctrl+O`).
    - **Web Dashboard**: Added `toolbox desktop dashboard` to launch a local Tailwind-powered management UI (FastAPI).
    - **File Associations**: Added `toolbox desktop register-file-type` to link extensions (like `.vault`) directly to ToolBox workflows.
- **Video Super-Resolution**: Added `toolbox video upscale` using AI (ESRGAN) to upscale videos frame-by-frame with audio preservation.
- **Encrypted Steganography**: Enhanced `toolbox security steg-hide` and `steg-extract` with optional password-based encryption (PBKDF2/Fernet).
- **Desktop Integration (Initial)**:
    - **Windows Context Menu**: Added `toolbox desktop install-context-menu` to add "Run with ToolBox" to right-click menus for files and folders.
    - **Native Notifications**: Added `toolbox desktop notify` for cross-platform system notifications (Windows/macOS/Linux).
- **Encrypted P2P Transfer**: Added `toolbox network p2p-send` and `p2p-receive` for secure, peer-to-peer file transfers using PBKDF2/Fernet encryption.

## [0.3.1-dev] - 2026-01-14
### Added
- **Automated Model Management**: Added `toolbox ai download` command to pre-cache AI models (upscale, etc.) for offline use.
- **Enhanced Logging**: Added `--json-log` flag to the main CLI for machine-readable output in JSON format.
- **Workflow Debugger**: Added `--debug-workflow` flag to `toolbox workflow run` for detailed execution tracing and variable inspection.

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
