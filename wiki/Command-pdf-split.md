# toolbox pdf split

Split a PDF into individual pages. Supports local or URL.

## Synopsis

```bash
toolbox pdf split [INPUT_FILE] [-o PATH] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox pdf split <input_file>
toolbox pdf split -o <output_dir> --dry-run <input_file>
```

## Help

```text
Usage: toolbox pdf split [OPTIONS] [INPUT_FILE]

  Split a PDF into individual pages. Supports local
  or URL.

Options:
  -o, --output-dir PATH  Output directory
  --dry-run              Show what would happen
  --glob TEXT            Glob pattern to process
                         multiple files (e.g.
                         '*.jpg')
  --parallel             Enable parallel processing
                         for batch operations
  --workers INTEGER      Number of worker threads
                         (default: CPU count)
  --help                 Show this message and exit.
```

Parent: [toolbox pdf](Command-pdf)
Back: [Command Index](Command-Index)
