# toolbox image remove-bg

Remove image background using rembg (AI-powered).

## Synopsis

```bash
toolbox image remove-bg [INPUT_FILE] [-o TEXT] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox image remove-bg <input_file>
toolbox image remove-bg -o <output> --dry-run <input_file>
```

## Help

```text
Usage: toolbox image remove-bg [OPTIONS]
                               [INPUT_FILE]

  Remove image background using rembg (AI-powered).

Options:
  -o, --output TEXT  Output filename
  --dry-run          Show what would happen
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
