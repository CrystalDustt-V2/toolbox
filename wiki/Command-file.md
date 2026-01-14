# toolbox file

File management utilities.

## Subcommands

- [toolbox file batch-rename](Command-file-batch-rename) — Batch rename files in a directory.
- [toolbox file compress-ai](Command-file-compress-ai) — Neural Compression: Compress text/code using local LLM probability models.
- [toolbox file decrypt](Command-file-decrypt) — Decrypt a file using AES-256-GCM.
- [toolbox file encrypt](Command-file-encrypt) — Encrypt a file using AES-256-GCM.
- [toolbox file hash](Command-file-hash) — Calculate file checksum/hash. Supports local or URL.
- [toolbox file info](Command-file-info) — Get detailed file information.
- [toolbox file rename](Command-file-rename) — Rename or move a file.
- [toolbox file semantic-find](Command-file-semantic-find) — Semantic File Discovery: Search for files by meaning using local embeddings.
- [toolbox file shred](Command-file-shred) — Securely erase a file by overwriting it multiple times (DoD 5220.22-M style).
- [toolbox file watch](Command-file-watch) — Watch a directory for changes and trigger a ToolBox command.

## Help

```text
Usage: toolbox file [OPTIONS] COMMAND [ARGS]...

  File management utilities.

Options:
  --help  Show this message and exit.

Commands:
  batch-rename   Batch rename files in a...
  compress-ai    Neural Compression: Compress...
  decrypt        Decrypt a file using AES-256-GCM.
  encrypt        Encrypt a file using AES-256-GCM.
  hash           Calculate file checksum/hash.
  info           Get detailed file information.
  rename         Rename or move a file.
  semantic-find  Semantic File Discovery:...
  shred          Securely erase a file by...
  watch          Watch a directory for changes...
```

Back: [Command Index](Command-Index)
