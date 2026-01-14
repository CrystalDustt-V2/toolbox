# toolbox pdf extract-text

Extract text content from a PDF. Supports local or URL.

## Synopsis

```bash
toolbox pdf extract-text [INPUT_FILE] [-o PATH] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox pdf extract-text <input_file>
toolbox pdf extract-text -o <output> --dry-run <input_file>
```

## Help

```text
Usage: toolbox pdf extract-text [OPTIONS]
                                [INPUT_FILE]

  Extract text content from a PDF. Supports local or
  URL.

Options:
  -o, --output PATH  Output text file
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
