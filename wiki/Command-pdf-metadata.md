# toolbox pdf metadata

View or strip PDF metadata. Supports local or URL.

## Synopsis

```bash
toolbox pdf metadata [INPUT_FILE] [--strip] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox pdf metadata <input_file>
toolbox pdf metadata --strip --dry-run <input_file>
```

## Help

```text
Usage: toolbox pdf metadata [OPTIONS] [INPUT_FILE]

  View or strip PDF metadata. Supports local or URL.

Options:
  --strip            Remove all metadata
  --dry-run          Show what would happen
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox pdf](Command-pdf)
Back: [Command Index](Command-Index)
