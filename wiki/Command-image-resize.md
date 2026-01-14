# toolbox image resize

Resize an image. Supports local or URL.

## Synopsis

```bash
toolbox image resize [INPUT_FILE] [-w INTEGER] [-h INTEGER] [-o PATH] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox image resize <input_file>
toolbox image resize -w <width> -h <height> <input_file>
```

## Help

```text
Usage: toolbox image resize [OPTIONS] [INPUT_FILE]

  Resize an image. Supports local or URL.

Options:
  -w, --width INTEGER   Target width
  -h, --height INTEGER  Target height
  -o, --output PATH     Output filename
  --dry-run             Show what would happen
                        without actual resizing
  --glob TEXT           Glob pattern to process
                        multiple files (e.g.
                        '*.jpg')
  --parallel            Enable parallel processing
                        for batch operations
  --workers INTEGER     Number of worker threads
                        (default: CPU count)
  --help                Show this message and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
