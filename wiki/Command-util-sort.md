# toolbox util sort

Sort lines in a text file. Supports local or URL.

## Synopsis

```bash
toolbox util sort [INPUT_FILE] [-o TEXT] [-u] [-r] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox util sort <input_file>
toolbox util sort -o <output> -u <input_file>
```

## Help

```text
Usage: toolbox util sort [OPTIONS] [INPUT_FILE]

  Sort lines in a text file. Supports local or URL.

Options:
  -o, --output TEXT  Output file (default: overwrite
                     if local)
  -u, --unique       Remove duplicates
  -r, --reverse      Reverse sort order
  --dry-run          Show what would happen
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox util](Command-util)
Back: [Command Index](Command-Index)
