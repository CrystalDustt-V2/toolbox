# toolbox util replace

Find and replace text in a file. Supports local or URL.

## Synopsis

```bash
toolbox util replace SEARCH REPLACEMENT [INPUT_FILE] [-o TEXT] [-i] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox util replace <search> <replacement> <input_file>
toolbox util replace -o <output> -i <search> <replacement> <input_file>
```

## Help

```text
Usage: toolbox util replace [OPTIONS] SEARCH
                            REPLACEMENT [INPUT_FILE]

  Find and replace text in a file. Supports local or
  URL.

Options:
  -o, --output TEXT  Output file (default: overwrite
                     if local)
  -i, --ignore-case  Ignore case
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
