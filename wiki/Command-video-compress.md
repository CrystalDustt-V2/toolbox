# toolbox video compress

Compress video using H.264. Supports local or URL.

## Synopsis

```bash
toolbox video compress [INPUT_FILE] [-crf INTEGER] [-o PATH] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox video compress <input_file>
toolbox video compress -crf <crf> -o <output> <input_file>
```

## Help

```text
Usage: toolbox video compress [OPTIONS] [INPUT_FILE]

  Compress video using H.264. Supports local or URL.

Options:
  -crf, --crf INTEGER  Constant Rate Factor (lower
                       is better quality, 0-51)
  -o, --output PATH    Output filename
  --dry-run            Show what would happen
  --glob TEXT          Glob pattern to process
                       multiple files (e.g. '*.jpg')
  --parallel           Enable parallel processing
                       for batch operations
  --workers INTEGER    Number of worker threads
                       (default: CPU count)
  --help               Show this message and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
