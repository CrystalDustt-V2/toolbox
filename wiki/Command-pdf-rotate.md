# toolbox pdf rotate

Rotate all pages in a PDF. Supports local or URL.

## Synopsis

```bash
toolbox pdf rotate [INPUT_FILE] [-r INTEGER] [-o PATH] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox pdf rotate <input_file>
toolbox pdf rotate -r <rotation> -o <output> <input_file>
```

## Help

```text
Usage: toolbox pdf rotate [OPTIONS] [INPUT_FILE]

  Rotate all pages in a PDF. Supports local or URL.

Options:
  -r, --rotation INTEGER  Rotation angle (degrees
                          clockwise)
  -o, --output PATH       Output filename
  --dry-run               Show what would happen
  --glob TEXT             Glob pattern to process
                          multiple files (e.g.
                          '*.jpg')
  --parallel              Enable parallel processing
                          for batch operations
  --workers INTEGER       Number of worker threads
                          (default: CPU count)
  --help                  Show this message and
                          exit.
```

Parent: [toolbox pdf](Command-pdf)
Back: [Command Index](Command-Index)
