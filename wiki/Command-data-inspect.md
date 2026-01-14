# toolbox data inspect

Inspect data structure and summary. Supports local or URL.

## Synopsis

```bash
toolbox data inspect [INPUT_FILE] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox data inspect <input_file>
toolbox data inspect --glob <glob_pattern> --parallel <input_file>
```

## Help

```text
Usage: toolbox data inspect [OPTIONS] [INPUT_FILE]

  Inspect data structure and summary. Supports local
  or URL.

Options:
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox data](Command-data)
Back: [Command Index](Command-Index)
